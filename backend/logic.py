import pandas as pd
import numpy as np
import gspread
import google.generativeai as genai
from PIL import Image
import json
import time
import random
import io
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
import os
import html
import requests
from fpdf import FPDF
import threading
import gc
import uuid
import firebase_admin
from firebase_admin import credentials, firestore
import toml

# --- SECRETS MANAGEMENT ADAPTER ---
def load_secrets():
    """Adapts Streamlit secrets to Python dict for backend"""
    secrets_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".streamlit", "secrets.toml")
    # Also check the original path if we are in a subdir
    original_secrets_path = os.path.join("d:\\OneDrive\\Desktop\\proyecto contador\\.streamlit\\secrets.toml")
    
    if os.path.exists(secrets_path):
        return toml.load(secrets_path)
    if os.path.exists(original_secrets_path):
        return toml.load(original_secrets_path)
    return {}

SECRETS = load_secrets()

# --- CONFIGURACIÓN DE PLANES Y FIRESTORE ---

PLAN_CONFIG = {
    'FREE': {
        'limit': 5,
        'model': 'gemini-flash-latest',
        'price_display': 'GRATIS',
        'badge': 'Prueba',
        'name': 'Free'
    },
    'PRO': {
        'limit': 500,
        'model': 'gemini-flash-latest',
        'price_display': '$70.000 COP',
        'badge': '⭐ Más Popular',
        'name': 'Pro'
    },
    'PREMIUM': {
        'limit': 2000,
        'model': 'gemini-flash-latest',
        'price_display': '$120.000 COP',
        'badge': '🧠 Inteligencia Superior',
        'name': 'Premium'
    }
}

# Variable global para cliente Firestore
db_client = None

def init_firestore():
    """Inicializa la app de Firebase Admin una sola vez."""
    global db_client
    if db_client: return db_client

    try:
        if not firebase_admin._apps:
            # Usamos las credenciales extraídas de SECRETS
            if "gcp_service_account" in SECRETS:
                cred = credentials.Certificate(dict(SECRETS["gcp_service_account"]))
                firebase_admin.initialize_app(cred)
            else:
                return None
        db_client = firestore.client()
        return db_client
    except Exception as e:
        print(f"Firestore Init Error: {e}")
        return None

def get_firestore_db():
    return init_firestore()

def update_session_token(email):
    """Genera un nuevo token de sesión y lo guarda en Firestore."""
    db = get_firestore_db()
    if not db: return str(uuid.uuid4()) # Fallback sin persistencia

    new_token = str(uuid.uuid4())
    try:
        user_ref = db.collection('users').document(email)
        user_ref.set({
            'session_token': new_token,
            'last_login': firestore.SERVER_TIMESTAMP
        }, merge=True)
    except Exception:
        pass
    return new_token

def verify_session(email, token):
    """Verifica si el token local coincide con el de Firestore."""
    db = get_firestore_db()
    if not db: return True # Si no hay DB, asumimos válido (modo offline/dev)

    try:
        doc = db.collection('users').document(email).get()
        if doc.exists:
            remote_token = doc.to_dict().get('session_token')
            return remote_token == token
    except Exception:
        pass
    return True

def get_user_credits(email):
    """Obtiene los créditos usados del usuario."""
    db = get_firestore_db()
    if not db: return 0

    try:
        doc = db.collection('users').document(email).get()
        if doc.exists:
            return doc.to_dict().get('credits_used', 0)
    except Exception:
        pass
    return 0

def consume_credit(email):
    """Incrementa el contador de créditos usados."""
    db = get_firestore_db()
    if not db: return

    try:
        user_ref = db.collection('users').document(email)
        # Incremento atómico
        user_ref.update({'credits_used': firestore.Increment(1)})
    except Exception:
        pass

# --- CONSTANTES FISCALES COLOMBIA (AÑO GRAVABLE 2026) ---
SMMLV_2026 = 1750905
AUX_TRANS_2026 = 249095
UVT_2026 = 52374
TOPE_EFECTIVO = 100 * UVT_2026
BASE_RET_SERVICIOS = 4 * UVT_2026
BASE_RET_COMPRAS = 27 * UVT_2026

# --- FUNCIONES DE CÁLCULO ---

def calcular_dv_colombia(nit_sin_dv):
    """
    Aplica el algoritmo de Módulo 11 para calcular el DV de un NIT colombiano.
    """
    try:
        nit_str = str(nit_sin_dv).strip()
        if not nit_str.isdigit(): return "Error"
        
        primos = [3, 7, 13, 17, 19, 23, 29, 37, 41, 43, 47, 53, 59, 67, 71]
        suma = sum(int(digito) * primos[i] for i, digito in enumerate(reversed(nit_str)) if i < len(primos))
        resto = suma % 11
        return str(resto) if resto <= 1 else str(11 - resto)
    except:
        return "?"

def analizar_gasto_fila(row, col_valor, col_metodo, col_concepto):
    """
    Evalúa una fila de gastos contables para detectar incumplimientos del Art 771-5
    y bases de retención en la fuente.
    """
    hallazgos = []
    riesgo = "BAJO"
    
    try:
        raw_val = str(row[col_valor]) if pd.notnull(row[col_valor]) else "0"
        clean_val = raw_val.replace('$', '').replace(' ', '').replace(',', '')
        valor = float(clean_val)
    except (ValueError, TypeError):
        valor = 0.0
    metodo = str(row[col_metodo]) if pd.notnull(row[col_metodo]) else ""
    
    if 'efectivo' in metodo.lower() and valor > TOPE_EFECTIVO:
        hallazgos.append(f"⛔ RECHAZO FISCAL: Pago en efectivo (${valor:,.0f}) supera tope Art 771-5.")
        riesgo = "ALTO"
    
    if valor >= BASE_RET_SERVICIOS and valor < BASE_RET_COMPRAS:
        hallazgos.append("⚠️ ALERTA: Verificar Retención (Base Servicios).")
        if riesgo == "BAJO": riesgo = "MEDIO"
    elif valor >= BASE_RET_COMPRAS:
        hallazgos.append("⚠️ ALERTA: Verificar Retención (Base Compras).")
        if riesgo == "BAJO": riesgo = "MEDIO"
        
    return " | ".join(hallazgos) if hallazgos else "OK", riesgo

def calcular_ugpp_fila(row, col_salario, col_no_salarial):
    """
    Verifica que los pagos no salariales no excedan el 40% del total de la remuneración.
    """
    try:
        salario = float(row[col_salario]) if pd.notnull(row[col_salario]) else 0
        no_salarial = float(row[col_no_salarial]) if pd.notnull(row[col_no_salarial]) else 0
    except:
        return 0, 0, "ERROR DATOS", "Error en números"
    
    total = salario + no_salarial
    limite = total * 0.40
    
    if no_salarial > limite:
        exceso = no_salarial - limite
        return salario + exceso, exceso, "RIESGO ALTO", f"Excede límite Ley 1393 por ${exceso:,.0f}"
    return salario, 0, "OK", "Cumple norma"

def calcular_costo_empresa_fila(row, col_salario, col_aux, col_arl, col_exo):
    """Calculadora de Nómina Real - VERSIÓN DETALLADA"""
    try:
        salario = float(row[col_salario]) if pd.notnull(row[col_salario]) else 0
    except:
        salario = 0

    tiene_aux = str(row[col_aux]).strip().lower() in ['si', 's', 'true', '1', 'yes']
    
    if col_arl and col_arl in row and pd.notnull(row[col_arl]):
        try: nivel_arl = int(row[col_arl])
        except: nivel_arl = 1
    else: nivel_arl = 1 
        
    es_exonerado = str(row[col_exo]).strip().lower() in ['si', 's', 'true', '1', 'yes']
    
    aux_trans = AUX_TRANS_2026 if tiene_aux else 0
    ibc = salario
    base_prest = salario + aux_trans
    
    salud = 0 if es_exonerado else ibc * 0.085
    pension = ibc * 0.12
    arl_t = {1:0.00522, 2:0.01044, 3:0.02436, 4:0.0435, 5:0.0696}
    arl_val = ibc * arl_t.get(nivel_arl, 0.00522)
    
    total_seg_social = salud + pension + arl_val
    
    paraf = ibc * 0.04 # Caja
    if not es_exonerado: paraf += ibc * 0.05 # SENA + ICBF
    
    total_prestaciones = base_prest * 0.2183
    
    costo_total = base_prest + total_seg_social + paraf + total_prestaciones
    
    return costo_total, total_seg_social, total_prestaciones, paraf

# --- LOGICA IA ---

def consultar_ia_gemini(prompt, user_plan='FREE', credits=0, email=''):
    """
    Usa el modelo definido por el plan del usuario.
    Incluye lógica de consumo de créditos.
    """
    config = PLAN_CONFIG.get(user_plan, PLAN_CONFIG['FREE'])
    
    # Init API
    if "general" in SECRETS:
        GOOGLE_API_KEY = SECRETS["general"]["api_key_google"]
        genai.configure(api_key=GOOGLE_API_KEY)
    else:
        return "Error: API Key de Google no configurada."

    if credits >= config['limit']:
        return "⚠️ HAS ALCANZADO EL LÍMITE DE CRÉDITOS DE TU PLAN."

    try:
        model_name = config['model']
        intentos = [model_name, 'gemini-flash-latest', 'gemini-2.5-flash', 'gemini-2.0-flash']
        last_error = ""

        for m in intentos:
            try:
                model = genai.GenerativeModel(m)
                response = model.generate_content(prompt)
                
                # Consumir Crédito
                if email: consume_credit(email)
                return response.text
                
            except Exception as e:
                last_error = str(e)
                continue

        return f"Error IA [v2]: {last_error}"
    except Exception as e:
        return f"Error Crítico IA [v2]: {str(e)}"

def ocr_factura(imagen_bytes, user_plan='FREE', credits=0, email=''):
    config = PLAN_CONFIG.get(user_plan, PLAN_CONFIG['FREE'])

    if "general" in SECRETS:
        GOOGLE_API_KEY = SECRETS["general"]["api_key_google"]
        genai.configure(api_key=GOOGLE_API_KEY)

    if credits >= config['limit']:
        return None

    try:
        # Convert bytes to PIL Image
        image = Image.open(io.BytesIO(imagen_bytes))

        model = genai.GenerativeModel('gemini-flash-latest')
        prompt = """Extrae datos JSON estricto: {"fecha": "YYYY-MM-DD", "nit": "num", "proveedor": "txt", "concepto": "txt", "base": num, "iva": num, "total": num}"""
        response = model.generate_content([prompt, image])

        if email: consume_credit(email)

        return json.loads(response.text.replace("```json", "").replace("```", "").strip())
    except Exception as e:
        print(f"OCR Error: {e}")
        return None

def parsear_xml_dian(archivo_xml):
    try:
        tree = ET.parse(archivo_xml)
        root = tree.getroot()
        ns = {'cac': 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2',
              'cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2'}
        def get_text(path, root_elem=root):
            elem = root_elem.find(path, ns)
            return elem.text if elem is not None else ""
        
        data = {}
        # Assuming archivo_xml is a file object with a .name attribute
        # If it's a file-like object from FastAPI, we might need to handle name differently
        data['Archivo'] = getattr(archivo_xml, 'name', 'unknown.xml')
        data['Prefijo'] = get_text('.//cbc:ID')
        data['Fecha Emision'] = get_text('.//cbc:IssueDate')
        
        emisor = root.find('.//cac:AccountingSupplierParty', ns)
        if emisor:
            data['NIT Emisor'] = get_text('.//cbc:CompanyID', emisor.find('.//cac:PartyTaxScheme', ns))
            data['Emisor'] = get_text('.//cbc:RegistrationName', emisor.find('.//cac:PartyTaxScheme', ns))
            
        receptor = root.find('.//cac:AccountingCustomerParty', ns)
        if receptor:
            data['NIT Receptor'] = get_text('.//cbc:CompanyID', receptor.find('.//cac:PartyTaxScheme', ns))
            data['Receptor'] = get_text('.//cbc:RegistrationName', receptor.find('.//cac:PartyTaxScheme', ns))
            
        monetary = root.find('.//cac:LegalMonetaryTotal', ns)
        if monetary:
            try: data['Total a Pagar'] = float(get_text('cbc:PayableAmount', monetary) or 0)
            except: data['Total a Pagar'] = 0
            try: data['Base Imponible'] = float(get_text('cbc:LineExtensionAmount', monetary) or 0)
            except: data['Base Imponible'] = 0
            try: data['Total Impuestos'] = float(get_text('cbc:TaxInclusiveAmount', monetary) or 0) - data['Base Imponible']
            except: data['Total Impuestos'] = 0
            
        return data
    except Exception as e:
        return {"Archivo": getattr(archivo_xml, 'name', 'unknown'), "Error": f"Error XML: {str(e)}"}

# --- PDF GENERATOR ---
def create_pdf_bytes(df, title, filename_suffix):
    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 14)
            self.cell(0, 10, title[:50], 0, 1, 'C')
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, f"Generado por Asistente Contable Pro - {datetime.now().strftime('%Y-%m-%d %H:%M')}", 0, 1, 'C')
            self.ln(5)

    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 9)

    cols = df.columns.tolist()
    if len(cols) > 0:
        eff_width = 190 / len(cols)
        
        # Header
        pdf.set_fill_color(220, 220, 220)
        pdf.set_font('Arial', 'B', 8)
        for col in cols:
            pdf.cell(eff_width, 8, str(col)[:15], 1, 0, 'C', 1)
        pdf.ln()

        # Rows
        pdf.set_font('Arial', '', 8)
        for _, row in df.iterrows():
            for col in cols:
                txt = str(row[col])[:20] 
                pdf.cell(eff_width, 6, txt, 1, 0, 'L')
            pdf.ln()
    
    return pdf.output(dest='S').encode('latin-1')
