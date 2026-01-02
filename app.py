import streamlit as st
import pandas as pd
import numpy as np
import gspread
import google.generativeai as genai
from PIL import Image
import json
import time
import io
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
import os
import html
import google_auth_oauthlib.flow
from googleapiclient.discovery import build

# --- CONFIGURACIÓN DE ESTILO GLOBAL (ULTRA-TECH THEME) ---
st.markdown("""
    <style>
        /* --- FONTS --- */
        @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Inter:wght@300;400;600&family=Orbitron:wght@900&display=swap');

        /* --- VARIABLES --- */
        :root {
            --bg-void: #020617;
            --bg-deep: #0f172a;
            --bg-night: #1e1b4b;
            --neon-cyan: #06b6d4;
            --neon-purple: #8b5cf6;
            --glass-heavy: rgba(17, 24, 39, 0.7);
            --border-tech: rgba(56, 189, 248, 0.3);
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --shadow-glow: 0 0 15px rgba(6, 182, 212, 0.3);
        }

        /* --- LIVING BACKGROUND --- */
        .stApp {
            background: linear-gradient(-45deg, #020617, #0f172a, #1e1b4b, #0f172a) !important;
            background-size: 400% 400% !important;
            animation: gradientBG 15s ease infinite;
            font-family: 'Inter', sans-serif;
            color: var(--text-secondary);
        }

        @keyframes gradientBG {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* Tech Grid Overlay */
        .stApp::before {
            content: "";
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background-image:
                linear-gradient(rgba(56, 189, 248, 0.05) 1px, transparent 1px),
                linear-gradient(90deg, rgba(56, 189, 248, 0.05) 1px, transparent 1px);
            background-size: 40px 40px;
            pointer-events: none;
            z-index: -1;
            mask-image: radial-gradient(circle at center, black 40%, transparent 80%);
        }

        /* --- TYPOGRAPHY --- */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Rajdhani', sans-serif !important;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: white !important;
        }

        /* --- GLASSMORPHISM 2.0 --- */
        div[data-testid="stExpander"], .glass-card, .pricing-card, .pro-module-header {
            background: var(--glass-heavy) !important;
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid var(--border-tech) !important;
            border-radius: 4px !important; /* Tech look is sharper */
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        div[data-testid="stExpander"]:hover, .glass-card:hover, .pricing-card:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-glow);
            border-color: var(--neon-cyan) !important;
        }

        /* --- WIDGET STYLING --- */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stSelectbox > div > div > div {
            background-color: rgba(255, 255, 255, 0.05) !important;
            color: white !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 4px;
            font-family: 'Rajdhani', sans-serif;
        }

        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus,
        .stSelectbox > div > div > div:focus {
            border-color: var(--neon-cyan) !important;
            box-shadow: 0 0 10px rgba(6, 182, 212, 0.2);
        }

        /* --- DATAFRAMES - TERMINAL STYLE --- */
        [data-testid="stDataFrame"] {
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid var(--border-tech);
            font-family: 'Courier New', monospace;
            border-radius: 4px;
        }

        [data-testid="stDataFrame"] table {
            color: var(--neon-cyan) !important;
        }

        [data-testid="stDataFrame"] thead tr th {
             background-color: rgba(6, 182, 212, 0.1) !important;
             color: white !important;
             font-family: 'Rajdhani', sans-serif !important;
             text-transform: uppercase;
        }

        /* --- SIDEBAR - CONTROL DOCK --- */
        [data-testid="stSidebar"] {
            background: rgba(2, 6, 23, 0.95) !important;
            border-right: 1px solid var(--border-tech);
        }

        .stRadio > div[role="radiogroup"] > label {
            background: transparent !important;
            border: none;
            padding: 10px 15px !important;
            color: #64748b !important;
            border-left: 2px solid transparent;
            font-family: 'Rajdhani', sans-serif;
            letter-spacing: 0.5px;
            transition: all 0.2s ease;
        }

        .stRadio > div[role="radiogroup"] > label:hover {
             color: white !important;
             background: rgba(6, 182, 212, 0.05) !important;
             text-shadow: 0 0 5px rgba(6, 182, 212, 0.5);
        }

        .stRadio > div[role="radiogroup"] > label[data-checked="true"] {
            background: linear-gradient(90deg, rgba(6, 182, 212, 0.1), transparent) !important;
            border-left: 2px solid var(--neon-cyan);
            color: white !important;
            font-weight: 700;
            text-shadow: 0 0 8px var(--neon-cyan);
        }

        /* --- BUTTONS --- */
        .stButton > button {
            background: linear-gradient(90deg, var(--neon-cyan), var(--neon-purple)) !important;
            border: none !important;
            color: white !important;
            font-family: 'Rajdhani', sans-serif !important;
            font-weight: 700 !important;
            text-transform: uppercase;
            letter-spacing: 1px;
            border-radius: 2px !important;
            /* Tech Shape */
            clip-path: polygon(10px 0, 100% 0, 100% calc(100% - 10px), calc(100% - 10px) 100%, 0 100%, 0 10px);
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }

        .stButton > button:hover {
            filter: brightness(1.2);
            text-shadow: 0 0 8px white;
            transform: translateY(-2px);
        }

        /* Hide Streamlit Defaults */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* --- METRICS --- */
        [data-testid="stMetricValue"] {
             font-family: 'Orbitron', sans-serif;
             font-weight: 900;
             color: #f8fafc !important;
             text-shadow: 0 0 15px rgba(6, 182, 212, 0.4);
        }
        [data-testid="stMetricLabel"] {
             color: var(--neon-cyan) !important;
             font-family: 'Rajdhani', sans-serif;
             font-size: 0.9rem;
             letter-spacing: 1px;
             text-transform: uppercase;
        }

        /* --- HELPERS --- */
        .pro-module-icon {
            width: 40px; height: 40px; margin-right: 15px;
            filter: drop-shadow(0 0 5px var(--neon-cyan));
        }

        .detail-box {
            background: rgba(6, 182, 212, 0.05);
            border-left: 2px solid var(--neon-cyan);
            padding: 15px;
            margin-bottom: 20px;
            color: var(--text-secondary);
            font-family: 'Rajdhani', sans-serif;
            font-size: 1.1rem;
        }

        .detail-box strong { color: white; }

        /* Scrollbar */
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: #020617; }
        ::-webkit-scrollbar-thumb { background: #1e293b; border-radius: 0px; }
        ::-webkit-scrollbar-thumb:hover { background: var(--neon-cyan); }

    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. GESTIÓN DE CONEXIONES EXTERNAS (BACKEND) Y SEGURIDAD (OAUTH2)
# ==============================================================================

# ------------------------------------------------------------------------------
# A. AUTENTICACIÓN GOOGLE OAUTH2 (THE GATEKEEPER)
# ------------------------------------------------------------------------------

def login_section():
    # Load secrets
    if "google" not in st.secrets:
        st.error("Missing Google Secrets configuration.")
        st.stop()

    client_config = {
        "web": {
            "client_id": st.secrets["google"]["client_id"],
            "client_secret": st.secrets["google"]["client_secret"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [st.secrets["google"]["redirect_uri"]],
        }
    }

    # Initialize Flow
    flow = google_auth_oauthlib.flow.Flow.from_client_config(
        client_config,
        scopes=['openid', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile'],
        redirect_uri=st.secrets["google"]["redirect_uri"]
    )

    # Check for authorization code in URL
    if "code" in st.query_params:
        try:
            code = st.query_params["code"]
            flow.fetch_token(code=code)
            credentials = flow.credentials

            # Fetch User Info
            user_info_service = build('oauth2', 'v2', credentials=credentials)
            user_info = user_info_service.userinfo().get().execute()

            # Store in Session State
            st.session_state['logged_in'] = True
            st.session_state['user_info'] = user_info
            st.session_state['username'] = user_info.get('name')
            st.session_state['user_email'] = user_info.get('email')
            st.session_state['user_picture'] = user_info.get('picture')
            st.session_state['user_plan'] = 'PRO' # Default to PRO for authorized users for now

            # Clear query params to prevent re-execution
            st.query_params.clear()
            st.rerun()

        except Exception as e:
            st.error(f"Authentication Failed: {e}")
    else:
        # Show Login Screen
        auth_url, _ = flow.authorization_url(prompt='consent')

        st.markdown(f"""
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 80vh;">
            <h1 style="font-family: 'Orbitron'; font-size: 3rem; margin-bottom: 1rem; text-align: center;">SYSTEM ACCESS</h1>
            <p style="color: var(--text-secondary); margin-bottom: 2rem; font-family: 'Rajdhani'; font-size: 1.2rem;">AUTHENTICATION REQUIRED FOR ENTERPRISE SUITE</p>
            <a href="{auth_url}" target="_self">
                <button style="
                    background: linear-gradient(90deg, var(--neon-cyan), var(--neon-purple));
                    border: none;
                    color: white;
                    padding: 1rem 2rem;
                    font-size: 1.2rem;
                    font-family: 'Rajdhani';
                    font-weight: 700;
                    text-transform: uppercase;
                    cursor: pointer;
                    clip-path: polygon(10px 0, 100% 0, 100% calc(100% - 10px), calc(100% - 10px) 100%, 0 100%, 0 10px);
                    box-shadow: 0 0 20px rgba(6, 182, 212, 0.4);
                    transition: all 0.3s ease;
                ">
                    🔐 INICIAR SESIÓN CON GOOGLE
                </button>
            </a>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

# --- CHECK LOGIN STATUS ---
if not st.session_state.get('logged_in', False):
    login_section()

# ------------------------------------------------------------------------------
# B. CONEXIÓN A BASE DE DATOS (GOOGLE SHEETS)
# ------------------------------------------------------------------------------
# Esta sección maneja la conexión silenciosa para registrar logs de auditoría
# sin que el usuario tenga que ver procesos técnicos en pantalla.
db_conectada = False
sheet_logs = None

try:
    if "gcp_service_account" in st.secrets:
        # Intentamos conectar con las credenciales del archivo secrets.toml
        gc = gspread.service_account_from_dict(st.secrets["gcp_service_account"])
        
        # Intentar abrir la hoja de cálculo maestra 'DB_Alcontador'
        sh = gc.open("DB_Alcontador")
        sheet_logs = sh.sheet1
        db_conectada = True
    else:
        # Si no hay secretos configurados, marcamos como desconectado
        db_conectada = False
except Exception as e:
    # Manejo de errores silencioso para no interrumpir la experiencia del usuario
    # si falla la conexión a internet o la API de Google.
    db_conectada = False


def registrar_log(usuario, accion, detalle):
    """
    Función de Auditoría:
    Guarda un registro de actividad en Google Sheets si la DB está conectada.
    Campos: Fecha y Hora, Usuario, Acción realizada, Detalle técnico.
    """
    if db_conectada and sheet_logs:
        try:
            fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sheet_logs.append_row([fecha_hora, usuario, accion, detalle])
        except:
            # Si falla el registro del log, no detenemos la aplicación
            pass 


# ------------------------------------------------------------------------------
# C. CONFIGURACIÓN DE INTELIGENCIA ARTIFICIAL (GEMINI)
# ------------------------------------------------------------------------------
api_key_valida = False
estado_ia = "🔴 Verificando..."

try:
    if "general" in st.secrets:
        # Configuración de la API Key para servicios de IA Generativa
        GOOGLE_API_KEY = st.secrets["general"]["api_key_google"]
        genai.configure(api_key=GOOGLE_API_KEY)
        estado_ia = "🟢 IA Activa (System Online)"
        api_key_valida = True
    else:
        estado_ia = "🔴 IA Desconectada (Offline)"
        api_key_valida = False
except Exception as e:
    estado_ia = "🔴 Error Configuración IA"
    api_key_valida = False


# ==============================================================================
# ==============================================================================
# 3. INTERFAZ GRÁFICA Y DISEÑO (CSS AVANZADO)
# ==============================================================================
# ==============================================================================

# Determinamos el saludo según la hora del servidor
hora_actual = datetime.now().hour
if 5 <= hora_actual < 12:
    saludo = "Buenos días"
elif 12 <= hora_actual < 18:
    saludo = "Buenas tardes"
else:
    saludo = "Buenas noches"

# Styles consolidated in the global block above
pass

# ==============================================================================
# ==============================================================================
# 4. FUNCIONES DE LÓGICA DE NEGOCIO Y CÁLCULOS FISCALES
# ==============================================================================
# ==============================================================================

# CONSTANTES FISCALES COLOMBIA (AÑO GRAVABLE 2025)
SMMLV_2025 = 1430000
AUX_TRANS_2025 = 175000
UVT_2025 = 49799
TOPE_EFECTIVO = 100 * UVT_2025
BASE_RET_SERVICIOS = 4 * UVT_2025
BASE_RET_COMPRAS = 27 * UVT_2025

# ------------------------------------------------------------------------------
# CALCULAR DÍGITO DE VERIFICACIÓN (RUT)
# ------------------------------------------------------------------------------
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

# ------------------------------------------------------------------------------
# ANÁLISIS DE RIESGO TRIBUTARIO (GASTOS)
# ------------------------------------------------------------------------------
def analizar_gasto_fila(row, col_valor, col_metodo, col_concepto):
    """
    Evalúa una fila de gastos contables para detectar incumplimientos del Art 771-5
    y bases de retención en la fuente.
    """
    hallazgos = []
    riesgo = "BAJO"
    
    # Extracción segura de valores
    valor = float(row[col_valor]) if pd.notnull(row[col_valor]) else 0
    metodo = str(row[col_metodo]) if pd.notnull(row[col_metodo]) else ""
    
    # 1. Validación de Bancarización
    if 'efectivo' in metodo.lower() and valor > TOPE_EFECTIVO:
        hallazgos.append(f"⛔ RECHAZO FISCAL: Pago en efectivo (${valor:,.0f}) supera tope Art 771-5.")
        riesgo = "ALTO"
    
    # 2. Validación de Bases de Retención
    if valor >= BASE_RET_SERVICIOS and valor < BASE_RET_COMPRAS:
        hallazgos.append("⚠️ ALERTA: Verificar Retención (Base Servicios).")
        if riesgo == "BAJO": riesgo = "MEDIO"
    elif valor >= BASE_RET_COMPRAS:
        hallazgos.append("⚠️ ALERTA: Verificar Retención (Base Compras).")
        if riesgo == "BAJO": riesgo = "MEDIO"
        
    return " | ".join(hallazgos) if hallazgos else "OK", riesgo

# ------------------------------------------------------------------------------
# ANÁLISIS DE RIESGO UGPP (LEY 1393)
# ------------------------------------------------------------------------------
def calcular_ugpp_fila(row, col_salario, col_no_salarial):
    """
    Verifica que los pagos no salariales no excedan el 40% del total de la remuneración.
    """
    salario = float(row[col_salario]) if pd.notnull(row[col_salario]) else 0
    no_salarial = float(row[col_no_salarial]) if pd.notnull(row[col_no_salarial]) else 0
    
    total = salario + no_salarial
    limite = total * 0.40
    
    if no_salarial > limite:
        exceso = no_salarial - limite
        return salario + exceso, exceso, "RIESGO ALTO", f"Excede límite Ley 1393 por ${exceso:,.0f}"
    return salario, 0, "OK", "Cumple norma"

# ------------------------------------------------------------------------------
# CALCULADORA DE COSTO DE NÓMINA (LÓGICA BLINDADA)
# ------------------------------------------------------------------------------
def calcular_costo_empresa_fila(row, col_salario, col_aux, col_arl, col_exo):
    """Calculadora de Nómina Real - VERSIÓN DETALLADA"""
    try:
        salario = float(row[col_salario]) if pd.notnull(row[col_salario]) else 0
    except:
        salario = 0

    tiene_aux = str(row[col_aux]).strip().lower() in ['si', 's', 'true', '1', 'yes']
    
    # ARL
    if col_arl and col_arl in row and pd.notnull(row[col_arl]):
        try: nivel_arl = int(row[col_arl])
        except: nivel_arl = 1
    else: nivel_arl = 1 
        
    es_exonerado = str(row[col_exo]).strip().lower() in ['si', 's', 'true', '1', 'yes']
    
    # --- CÁLCULOS DETALLADOS ---
    aux_trans = AUX_TRANS_2025 if tiene_aux else 0
    ibc = salario
    base_prest = salario + aux_trans
    
    # 1. SEGURIDAD SOCIAL (Empleador)
    salud = 0 if es_exonerado else ibc * 0.085
    pension = ibc * 0.12
    arl_t = {1:0.00522, 2:0.01044, 3:0.02436, 4:0.0435, 5:0.0696}
    arl_val = ibc * arl_t.get(nivel_arl, 0.00522)
    
    total_seg_social = salud + pension + arl_val
    
    # 2. PARAFISCALES
    paraf = ibc * 0.04 # Caja
    if not es_exonerado: paraf += ibc * 0.05 # SENA + ICBF
    
    # 3. PRESTACIONES SOCIALES (Prima, Cesantías, Int, Vacaciones)
    # Factor 21.83% sobre salario + auxilio
    total_prestaciones = base_prest * 0.2183 
    
    # TOTAL COSTO
    costo_total = base_prest + total_seg_social + paraf + total_prestaciones
    
    # Retornamos los valores separados
    return costo_total, total_seg_social, total_prestaciones, paraf

# ------------------------------------------------------------------------------
# CONEXIÓN CON IA (CEREBRO HÍBRIDO)
# ------------------------------------------------------------------------------
def consultar_ia_gemini(prompt):
    """
    Usa el modelo PRO (Más inteligente y razonador)
    Ideal para: Narrador Financiero, Análisis de Tesorería y Auditoría NIIF.
    """
    try:
        # Intentamos usar la versión '2.5-flash' disponible
        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            # Fallback o diagnóstico
            try:
                available_models = [m.name for m in genai.list_models()]
                return f"Error IA: {str(e)}. Modelos disponibles: {available_models}"
            except:
                return f"Error de conexión IA: {str(e)}"
    except Exception as e:
        return f"Error crítico IA: {str(e)}"

# ------------------------------------------------------------------------------
# OCR DE FACTURAS (VELOCIDAD)
# ------------------------------------------------------------------------------
def ocr_factura(imagen):
    """
    Usa el modelo FLASH (Más rápido y ligero)
    Ideal para: Procesar imágenes masivas sin hacer esperar al usuario.
    """
    try:
        # Usamos versión estable
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = """Extrae datos JSON estricto: {"fecha": "YYYY-MM-DD", "nit": "num", "proveedor": "txt", "concepto": "txt", "base": num, "iva": num, "total": num}"""
        response = model.generate_content([prompt, imagen])
        return json.loads(response.text.replace("```json", "").replace("```", "").strip())
    except Exception as e:
        # En OCR fallamos silenciosamente o retornamos None como antes,
        # pero podríamos loguear el error si tuviéramos un sistema de logs.
        print(f"Error OCR: {e}")
        return None

# ------------------------------------------------------------------------------
# PARSEADOR DE XML (FACTURACIÓN ELECTRÓNICA DIAN)
# ------------------------------------------------------------------------------
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
        data['Archivo'] = archivo_xml.name
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
            data['Total a Pagar'] = float(get_text('cbc:PayableAmount', monetary) or 0)
            data['Base Imponible'] = float(get_text('cbc:LineExtensionAmount', monetary) or 0)
            data['Total Impuestos'] = float(get_text('cbc:TaxInclusiveAmount', monetary) or 0) - data['Base Imponible']
            
        return data
    except:
        return {"Archivo": archivo_xml.name, "Error": "Error XML"}

# ==============================================================================
# ==============================================================================
# 5. BARRA LATERAL (SIDEBAR) - NAVEGACIÓN Y LOGIN
# ==============================================================================
# ==============================================================================

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2830/2830303.png", width=80)
    st.markdown("### 💼 Suite Financiera", unsafe_allow_html=True)
    
    # --- PANEL DE USUARIO LOGUEADO (SIDEBAR) ---
    plan_bg = "#FFD700" if st.session_state['user_plan'] == 'PRO' else "#A9A9A9"
    status_db = "🟢 DB Online" if db_conectada else "🔴 DB Offline"
    
    # Security: Escape variables injected into HTML
    user_plan_safe = html.escape(str(st.session_state.get('user_plan', 'FREE')))
    estado_ia_safe = html.escape(str(estado_ia))
    status_db_safe = html.escape(str(status_db))

    # User Info from Google
    user_name = html.escape(str(st.session_state.get('username', 'Commander')))
    user_pic = st.session_state.get('user_picture', '')

    # Show User Profile
    if user_pic:
        st.markdown(f"<img src='{user_pic}' style='width: 50px; height: 50px; border-radius: 50%; margin-bottom: 10px; border: 2px solid var(--neon-cyan);'>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style='background: rgba(255,255,255,0.05); padding: 15px; border-radius: 4px; border-left: 3px solid {plan_bg}; margin-bottom: 20px;'>
        <small style='color: #94a3b8; text-transform:uppercase;'>OPERATOR:</small><br>
        <strong style='font-size: 1.1rem; color:white; font-family: "Rajdhani";'>{user_name}</strong><br>
        <span style="font-size: 0.8rem; color: var(--neon-cyan);">{user_plan_safe} ACCESS</span><br>
        <small style='color: #64748b;'>{estado_ia_safe}</small><br>
        <small style='color: {'#06b6d4' if db_conectada else '#ef4444'}; font-weight:bold;'>{status_db_safe}</small>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state['user_plan'] == 'FREE':
        st.markdown("---")
        st.write("🔓 UNLOCK FULL SYSTEM")
        # Enlace de pago WOMPI
        st.link_button(
            "💎 UPGRADE TO PRO",
            "https://checkout.wompi.co/l/TU_LINK_AQUI"
        )
        st.caption("Access all enterprise modules.")

    if st.button("TERMINATE SESSION"):
        registrar_log(st.session_state.get('username', 'Unknown'), "Logout", "Salida del sistema")
        st.session_state.clear()
        st.rerun()

    st.markdown("---")
    
    opciones_menu = [
        "Inicio / Dashboard",
        "Auditoría Cruce DIAN",
        "Minería de XML (Facturación)",
        "Conciliación Bancaria IA",
        "Auditoría Fiscal de Gastos",
        "Escáner de Nómina (UGPP)",
        "Proyección de Tesorería",
        "Costeo de Nómina Real",
        "Analítica Financiera Inteligente",
        "Narrador Financiero & NIIF",
        "Validador de RUT Oficial",
        "Digitalización OCR"
    ]
    
    menu = st.radio("SYSTEM MODULES:", opciones_menu)
    
    st.markdown("<br><center><small style='color: #64748b;'>v14.5 ENTERPRISE</small></center>", unsafe_allow_html=True)

# ==============================================================================
# ==============================================================================
# 6. CONTENIDO PRINCIPAL (DASHBOARD Y MÓDULOS)
# ==============================================================================
# ==============================================================================

if menu == "Inicio / Dashboard":
    # 1. HEADER EJECUTIVO (HERO SECTION - ULTRA TECH)
    st.markdown("""
    <div class="hero-container">
        <div class="hero-content">
            <h1 class="hero-title">ASISTENTE CONTABLE <span style="color: var(--neon-cyan)">PRO</span></h1>
            <div class="hero-subtitle">SYSTEM ONLINE • v14.5 ENTERPRISE • <span style="color: var(--neon-purple)">AI CORE ACTIVE</span></div>
        </div>
        <div class="hero-decoration"></div>
    </div>
    <style>
        .hero-container {
            position: relative;
            padding: 3rem 2rem;
            margin-bottom: 2rem;
            background: linear-gradient(90deg, rgba(6, 182, 212, 0.1), transparent);
            border-left: 4px solid var(--neon-cyan);
            border-radius: 4px;
            overflow: hidden;
            backdrop-filter: blur(10px);
        }
        .hero-title {
            font-family: 'Orbitron', sans-serif !important;
            font-size: 3.5rem !important;
            margin: 0;
            letter-spacing: 2px;
            text-shadow: 0 0 20px rgba(6, 182, 212, 0.5);
        }
        .hero-subtitle {
            font-family: 'Rajdhani', sans-serif;
            font-size: 1.2rem;
            color: var(--text-secondary);
            margin-top: 0.5rem;
            letter-spacing: 3px;
            text-transform: uppercase;
        }
    </style>
    """, unsafe_allow_html=True)

    # 2. BENTO GRID DASHBOARD (Métricas y Gráficos)

    def metric_card(label, value, delta, is_positive=True):
        color = "#10b981" if is_positive else "#f43f5e"
        arrow = "↑" if is_positive else "↓"
        st.markdown(f"""
        <div class="glass-card" style="height: 100%; display: flex; flex-direction: column; justify-content: center; padding: 20px;">
            <div style="color: var(--neon-cyan); font-family: 'Rajdhani'; font-size: 0.9rem; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 8px;">{label}</div>
            <div style="font-family: 'Orbitron'; font-size: 1.8rem; font-weight: 900; color: white; margin-bottom: 5px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; text-shadow: 0 0 10px rgba(255,255,255,0.3);">{value}</div>
            <div style="color: {color}; font-size: 1rem; font-weight: 600; font-family: 'Rajdhani';">
                {arrow} {delta} <span style="color: var(--text-secondary); font-weight: 400;">vs last cycle</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 📊 LIVE METRICS STREAM")
    col1, col2, col3, col4 = st.columns(4)
    with col1: metric_card("TOTAL INCOME", "$124,500", "12%", True)
    with col2: metric_card("OP. EXPENSES", "$42,300", "5%", False)
    with col3: metric_card("NET PROFIT", "$82,200", "18%", True)
    with col4: metric_card("EBITDA MARGIN", "34%", "2%", True)

    st.markdown("---")

    c_chart_1, c_chart_2 = st.columns([2, 1])
    with c_chart_1:
        st.markdown("#### 📈 CASH FLOW TREND")
        chart_data = pd.DataFrame(np.random.randn(20, 3) + [10, 10, 10], columns=['Income', 'Expenses', 'Profit'])
        st.area_chart(chart_data, color=["#06b6d4", "#ef4444", "#10b981"])
    with c_chart_2:
        st.markdown("#### 📉 EXPENSE BREAKDOWN")
        gastos_data = pd.DataFrame({'Category': ['Payroll', 'Software', 'Office', 'Ads'], 'Amount': [5000, 2000, 1500, 3000]})
        st.bar_chart(gastos_data.set_index('Category'), color="#8b5cf6")

    st.markdown("### 📝 LATEST TRANSACTIONS LOG")
    df_transacciones = pd.DataFrame({
        "ID": ["TRX-001", "TRX-002", "TRX-003", "TRX-004", "TRX-005"],
        "DATE": ["2024-05-01", "2024-05-02", "2024-05-02", "2024-05-03", "2024-05-03"],
        "CONCEPT": ["Payment Client A", "AWS Subscription", "Payment Client B", "Office Licenses", "Consulting"],
        "STATUS": ["COMPLETED", "PENDING", "COMPLETED", "COMPLETED", "REVIEW"],
        "AMOUNT": ["+$1,200", "-$300", "+$4,500", "-$150", "+$2,000"]
    })
    st.dataframe(df_transacciones, use_container_width=True, hide_index=True)

    # 3. SECCIÓN PLANES Y PRECIOS
    st.markdown("---")
    st.markdown("### 💎 UPGRADE ACCESS LEVEL")
    
    st.markdown("""
    <style>
        .pricing-card {
            background: var(--glass-heavy);
            backdrop-filter: blur(16px);
            border: 1px solid var(--border-tech);
            border-radius: 4px;
            padding: 2.5rem;
            height: 100%;
            display: flex; flex-direction: column;
            transition: all 0.3s ease;
        }
        .pricing-card:hover { transform: translateY(-5px); border-color: var(--neon-cyan); box-shadow: 0 0 20px rgba(6, 182, 212, 0.2); }
        .pricing-card.pro {
            background: linear-gradient(145deg, rgba(15, 23, 42, 0.9) 0%, rgba(6, 182, 212, 0.1) 100%);
            border: 1px solid var(--neon-cyan);
            box-shadow: 0 0 30px rgba(6, 182, 212, 0.1);
            position: relative;
        }
        .pro-badge {
            position: absolute; top: -12px; right: 24px;
            background: var(--neon-cyan);
            color: black; padding: 4px 12px; border-radius: 2px;
            font-size: 0.75rem; font-weight: 800; letter-spacing: 1px; font-family: 'Rajdhani';
        }
        .price-tag { font-family: 'Orbitron'; font-size: 3rem; font-weight: 800; color: white; margin: 10px 0; text-shadow: 0 0 10px rgba(255,255,255,0.5); }
        .price-tag span { font-size: 1rem; color: var(--text-secondary); font-weight: 500; font-family: 'Rajdhani'; }
        .price-old { font-size: 1.1rem; color: #64748b; text-decoration: line-through; margin-top: 10px; font-family: 'Rajdhani'; }
        .features-ul { list-style: none; padding: 0; margin: 24px 0; color: var(--text-secondary); flex-grow: 1; font-family: 'Rajdhani'; font-size: 1.1rem; }
        .features-ul li { margin-bottom: 12px; display: flex; align-items: center; }
        .check { color: var(--neon-cyan); margin-right: 12px; font-weight: bold; text-shadow: 0 0 5px var(--neon-cyan); }
        .cross { color: #ef4444; margin-right: 12px; opacity: 0.7; }
        .dimmed { color: #475569; }
    </style>
    """, unsafe_allow_html=True)

    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.markdown("""
        <div class="pricing-card">
            <h3 style="color:white; margin:0; font-size: 1.4rem;">STARTER LEVEL</h3>
            <div class="price-tag">$0 <span>COP/mo</span></div>
            <ul class="features-ul">
                <li><span class="check">✓</span> Dashboard Access</li>
                <li><span class="check">✓</span> 5 AI Queries/day</li>
                <li class="dimmed"><span class="cross">✕</span> Tax Agent</li>
                <li class="dimmed"><span class="cross">✕</span> Bank Connection</li>
            </ul>
        </div>""", unsafe_allow_html=True)
        st.button("CONTINUE FREE", key="btn_free", use_container_width=True)

    with col_p2:
        st.markdown("""
        <div class="pricing-card pro">
            <div class="pro-badge">RECOMMENDED</div>
            <h3 style="color:white; margin:0; font-size: 1.4rem;">PRO AGENT</h3>
            <div class="price-old">$120.000</div> <div class="price-tag">$49.900 <span>COP/mo</span></div>
            <ul class="features-ul">
                <li><span class="check">✓</span> <strong>Everything in Starter</strong></li>
                <li><span class="check">✓</span> Unlimited AI Queries</li>
                <li><span class="check">✓</span> Tax Prediction Model</li>
                <li><span class="check">✓</span> 24/7 Priority Uplink</li>
            </ul>
        </div>""", unsafe_allow_html=True)
        st.button("⚡ UPGRADE TO PRO", key="btn_pro", type="primary", use_container_width=True)

    if not db_conectada:
        st.warning("⚠️ DATABASE OFFLINE. Check 'DB_Alcontador' connection.")

# ---------------------------------------------------------
# ELSE: CAMBIO DE MENÚ (ESTE SÍ TOCA EL BORDE IZQUIERDO)
# ---------------------------------------------------------
else:
    # 1. AUDITORÍA
    if menu == "Auditoría Cruce DIAN":
        st.markdown("""<div class='pro-module-header'><img src='https://cdn-icons-png.flaticon.com/512/921/921591.png' class='pro-module-icon'><div class='pro-module-title'><h2>Auditor de Exógena (Cruce DIAN)</h2></div></div>""", unsafe_allow_html=True)
        st.markdown("""<div class='detail-box'><strong>Objetivo:</strong> Detectar discrepancias entre lo que reportaste y lo que la DIAN sabe de ti.<br><strong>Estrategia:</strong> Cruce matricial de NITs para evitar sanciones por inexactitud (Art. 651 ET).</div>""", unsafe_allow_html=True)
        
        col_dian, col_conta = st.columns(2)
        with col_dian:
            st.subheader("🏛️ 1. Archivo DIAN")
            file_dian = st.file_uploader("Subir 'Reporte Terceros DIAN' (.xlsx)", type=['xlsx'])
        with col_conta:
            st.subheader("📒 2. Contabilidad")
            file_conta = st.file_uploader("Subir Auxiliar por Tercero (.xlsx)", type=['xlsx'])
            
        if file_dian and file_conta:
            df_dian = pd.read_excel(file_dian)
            df_conta = pd.read_excel(file_conta)
            
            # Cerebro de Auto-Detección
            def detectar_idx(columnas, keywords):
                cols_str = [str(c).lower().strip() for c in columnas]
                for i, col in enumerate(cols_str):
                    for kw in keywords:
                        if kw in col: return i
                return 0
            
            kw_nit = ['nit', 'n.i.t', 'cedula', 'documento', 'id', 'tercero']
            kw_valor = ['valor', 'saldo', 'total', 'monto', 'pago', 'cuantia']
            
            idx_nit_d = detectar_idx(df_dian.columns, kw_nit)
            idx_val_d = detectar_idx(df_dian.columns, kw_valor)
            idx_nit_c = detectar_idx(df_conta.columns, kw_nit)
            idx_val_c = detectar_idx(df_conta.columns, kw_valor)
            
            st.divider()
            st.success(f"✅ Sistema Autoconfigurado: Se usarán las columnas '{df_dian.columns[idx_nit_d]}' y '{df_dian.columns[idx_val_d]}' automáticamente.")
            
            with st.expander("🛠️ (Opcional) Ver o cambiar columnas seleccionadas manualmente"):
                c1, c2, c3, c4 = st.columns(4)
                nit_dian = c1.selectbox("NIT (DIAN)", df_dian.columns, index=idx_nit_d)
                val_dian = c2.selectbox("Valor (DIAN)", df_dian.columns, index=idx_val_d)
                nit_conta = c3.selectbox("NIT (Conta)", df_conta.columns, index=idx_nit_c)
                val_conta = c4.selectbox("Valor (Conta)", df_conta.columns, index=idx_val_c)

            if st.button("▶️ EJECUTAR AUDITORÍA AHORA", type="primary"):
                try:
                    # registrar_log(st.session_state['username'], "Auditoria", "Ejecución cruce DIAN") # Comentado por seguridad si falta la funcion
                    dian_grouped = df_dian.groupby(nit_dian)[val_dian].sum().reset_index(name='Valor_DIAN').rename(columns={nit_dian: 'NIT'})
                    conta_grouped = df_conta.groupby(nit_conta)[val_conta].sum().reset_index(name='Valor_Conta').rename(columns={nit_conta: 'NIT'})
                    
                    dian_grouped['NIT'] = dian_grouped['NIT'].astype(str).str.strip()
                    conta_grouped['NIT'] = conta_grouped['NIT'].astype(str).str.strip()

                    cruce = pd.merge(dian_grouped, conta_grouped, on='NIT', how='outer').fillna(0)
                    cruce['Diferencia'] = cruce['Valor_DIAN'] - cruce['Valor_Conta']
                    diferencias = cruce[abs(cruce['Diferencia']) > 1000].sort_values(by="Diferencia", ascending=False)
                    
                    num_hallazgos = len(diferencias)
                    total_riesgo = diferencias['Diferencia'].abs().sum()
                    
                    st.divider()
                    if num_hallazgos == 0:
                        st.balloons()
                        st.success("✅ ¡Perfecto! No hay diferencias entre la DIAN y tu Contabilidad.")
                    else:
                        st.error(f"⚠️ Se encontraron {num_hallazgos} inconsistencias.")
                        col_met1, col_met2 = st.columns(2)
                        col_met1.metric("Riesgo Total", f"${total_riesgo:,.0f}")
                        col_met2.metric("Terceros con Error", num_hallazgos)
                        
                        if st.session_state.get('user_plan') == 'FREE':
                            st.warning("🔒 Versión GRATUITA: Solo se muestran los primeros 3 errores.")
                            st.dataframe(diferencias.head(3), use_container_width=True)
                        else:
                            st.success("💎 REPORTE COMPLETO (PRO)")
                            st.dataframe(diferencias, use_container_width=True)
                            # Exportación a Excel simplificada
                            # out = io.BytesIO() ... (Código de descarga aquí)
                
                except Exception as e:
                    st.error(f"Algo salió mal: {e}. Revisa 'Configuración manual' arriba.")

    # 2. MINERÍA XML (Continúa con ELIF)
    elif menu == "Minería de XML (Facturación)":
        st.markdown("""<div class='pro-module-header'><img src='https://cdn-icons-png.flaticon.com/512/2823/2823523.png' class='pro-module-icon'><div class='pro-module-title'><h2>Minería de Datos XML (Facturación)</h2></div></div>""", unsafe_allow_html=True)
        st.markdown("""<div class='detail-box'><strong>Objetivo:</strong> Extraer información estructurada directamente de los archivos XML de Facturación Electrónica validados por la DIAN.</div>""", unsafe_allow_html=True)
        archivos_xml = st.file_uploader("Cargar XMLs (Lote)", type=['xml'], accept_multiple_files=True)
        if archivos_xml and st.button("▶️ INICIAR PROCESAMIENTO"):
            st.toast("Procesando lote de archivos...")
            datos_xml = []; barra = st.progress(0)
            for i, f in enumerate(archivos_xml): barra.progress((i+1)/len(archivos_xml)); datos_xml.append(parsear_xml_dian(f))
            df_xml = pd.DataFrame(datos_xml)
            st.success("Extracción completada."); st.dataframe(df_xml, use_container_width=True)
            out = io.BytesIO(); 
            with pd.ExcelWriter(out, engine='xlsxwriter') as w: df_xml.to_excel(w, index=False)
            st.download_button("📥 Descargar Reporte Maestro (.xlsx)", out.getvalue(), "Resumen_XML.xlsx")
            registrar_log(st.session_state['username'], "Mineria XML", f"Procesados {len(archivos_xml)} archivos")

    elif menu == "Conciliación Bancaria IA":
        st.markdown("""<div class='pro-module-header'><img src='https://cdn-icons-png.flaticon.com/512/2489/2489756.png' class='pro-module-icon'><div class='pro-module-title'><h2>Conciliación Bancaria Inteligente</h2></div></div>""", unsafe_allow_html=True)
        st.markdown("""<div class='detail-box'><strong>Objetivo:</strong> Automatizar el emparejamiento de transacciones entre el Extracto Bancario y el Libro Auxiliar de Bancos usando lógica difusa (Fechas cercanas).</div>""", unsafe_allow_html=True)
        
        col_banco, col_libro = st.columns(2)
        with col_banco: st.subheader("🏦 Extracto Bancario"); file_banco = st.file_uploader("Subir Excel Banco", type=['xlsx'])
        with col_libro: st.subheader("📒 Libro Auxiliar"); file_libro = st.file_uploader("Subir Excel Contabilidad", type=['xlsx'])
        
        if file_banco and file_libro:
            # Lectura
            df_banco = pd.read_excel(file_banco)
            df_libro = pd.read_excel(file_libro)
            
            # --- CEREBRO DE AUTO-DETECCIÓN ---
            def detectar_idx(columnas, keywords):
                cols_str = [str(c).lower().strip() for c in columnas]
                for i, col in enumerate(cols_str):
                    for kw in keywords:
                        if kw in col: return i
                return 0
            
            kw_fecha = ['fecha', 'date', 'dia', 'fec']
            kw_valor = ['valor', 'monto', 'importe', 'saldo', 'debito', 'credito', 'total']
            kw_desc = ['desc', 'detalle', 'concepto', 'tercero', 'referencia']
            
            idx_fb = detectar_idx(df_banco.columns, kw_fecha)
            idx_vb = detectar_idx(df_banco.columns, kw_valor)
            idx_db = detectar_idx(df_banco.columns, kw_desc)
            
            idx_fl = detectar_idx(df_libro.columns, kw_fecha)
            idx_vl = detectar_idx(df_libro.columns, kw_valor)
            
            st.divider()
            st.success(f"✅ Configuración Automática: Se comparará '{df_banco.columns[idx_vb]}' del Banco vs '{df_libro.columns[idx_vl]}' del Libro.")

            with st.expander("🛠️ Ver/Editar Columnas Seleccionadas"):
                c1, c2, c3, c4 = st.columns(4)
                col_fecha_b = c1.selectbox("Fecha Banco:", df_banco.columns, index=idx_fb, key="fb")
                col_valor_b = c2.selectbox("Valor Banco:", df_banco.columns, index=idx_vb, key="vb")
                col_fecha_l = c3.selectbox("Fecha Libro:", df_libro.columns, index=idx_fl, key="fl")
                col_valor_l = c4.selectbox("Valor Libro:", df_libro.columns, index=idx_vl, key="vl")
                col_desc_b = st.selectbox("Descripción Banco:", df_banco.columns, index=idx_db, key="db")

            if st.button("▶️ EJECUTAR CONCILIACIÓN AHORA", type="primary"):
                registrar_log(st.session_state['username'], "Conciliacion", "Inicio matching bancario")
                
                # Normalización de Fechas
                try:
                    df_banco['Fecha_Dt'] = pd.to_datetime(df_banco[col_fecha_b])
                    df_libro['Fecha_Dt'] = pd.to_datetime(df_libro[col_fecha_l])
                except:
                    st.error("Error en formato de fechas. Asegúrate que las columnas de fecha sean correctas.")
                    st.stop()

                df_banco['Conciliado'] = False
                df_libro['Conciliado'] = False
                matches = []
                
                bar = st.progress(0)
                total_rows = len(df_banco)
                
                # ALGORITMO DE MATCHING INTELIGENTE
                # Optimización: Usamos zip para iterar más rápido que iterrows
                # Extraemos las columnas necesarias a listas/arrays para velocidad
                # Nota: Necesitamos el índice original (idx_b) para actualizar 'Conciliado'
                for i, (idx_b, vb, fb, fecha_b_orig, desc_b) in enumerate(zip(df_banco.index, df_banco[col_valor_b], df_banco['Fecha_Dt'], df_banco[col_fecha_b], df_banco[col_desc_b])):
                    bar.progress((i+1)/total_rows)
                    
                    # Busca coincidencias: Mismo valor, no conciliado aun, y fecha +/- 3 días
                    # Nota: df_libro se filtra repetidamente. Para grandes volúmenes esto debería ser vectorizado,
                    # pero dada la lógica 'first match consumes', la iteración es necesaria para mantener estado.
                    cands = df_libro[
                        (df_libro[col_valor_l] == vb) & 
                        (~df_libro['Conciliado']) & 
                        (df_libro['Fecha_Dt'].between(fb - timedelta(days=3), fb + timedelta(days=3)))
                    ]
                    
                    if not cands.empty:
                        # Si encuentra match, marca ambos como conciliados
                        match_idx = cands.index[0]
                        df_banco.at[idx_b, 'Conciliado'] = True
                        df_libro.at[match_idx, 'Conciliado'] = True
                        
                        f_libro_str = df_libro.at[match_idx, col_fecha_l]
                        matches.append({
                            "Fecha Banco": str(fecha_b_orig),
                            "Fecha Libro": str(f_libro_str),
                            "Descripción": str(desc_b),
                            "Valor Cruzado": f"${vb:,.2f}",
                            "Estado": "✅ AUTOMÁTICO"
                        })
                
                st.divider()
                st.balloons()
                st.success(f"🚀 ¡Proceso Terminado! {len(matches)} partidas conciliadas automáticamente.")
                
                # PREPARAR ARCHIVO PARA DESCARGA
                df_matches = pd.DataFrame(matches)
                df_pend_banco = df_banco[~df_banco['Conciliado']]
                df_pend_libro = df_libro[~df_libro['Conciliado']]
                
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                    df_matches.to_excel(writer, sheet_name='1. Cruzados', index=False)
                    df_pend_banco.to_excel(writer, sheet_name='2. Pendientes Banco', index=False)
                    df_pend_libro.to_excel(writer, sheet_name='3. Pendientes Libros', index=False)
                    
                st.download_button(
                    label="📥 DESCARGAR CONCILIACIÓN (.xlsx)",
                    data=buffer.getvalue(),
                    file_name=f"Conciliacion_{datetime.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.ms-excel"
                )
                
                t1, t2, t3 = st.tabs(["✅ Partidas Cruzadas", "⚠️ Pendientes en Banco", "⚠️ Pendientes en Libros"])
                
                with t1: 
                    st.dataframe(df_matches, use_container_width=True)
                with t2: 
                    st.warning("Estas partidas están en el Banco pero NO en tu contabilidad:")
                    st.dataframe(df_pend_banco, use_container_width=True)
                with t3: 
                    st.warning("Estos registros están en Contabilidad pero NO han salido del Banco:")
                    st.dataframe(df_pend_libro, use_container_width=True)

    elif menu == "Auditoría Fiscal de Gastos":
        st.markdown("""<div class='pro-module-header'><img src='https://cdn-icons-png.flaticon.com/512/1642/1642346.png' class='pro-module-icon'><div class='pro-module-title'><h2>Auditoría Fiscal Masiva (Art. 771-5)</h2></div></div>""", unsafe_allow_html=True)
        st.markdown("""<div class='detail-box'><strong>Objetivo:</strong> Verificar el cumplimiento de los requisitos de deducibilidad (Bancarización y Retenciones).<br>Detecta pagos en efectivo superiores a 100 UVT y bases de retención omitidas.</div>""", unsafe_allow_html=True)
        
        ar = st.file_uploader("Cargar Auxiliar de Gastos (.xlsx)", type=['xlsx'])
        
        if ar:
            df = pd.read_excel(ar)
            
            # --- CEREBRO DE AUTO-DETECCIÓN ---
            def detectar_idx(columnas, keywords):
                cols_str = [str(c).lower().strip() for c in columnas]
                for i, col in enumerate(cols_str):
                    for kw in keywords:
                        if kw in col: return i
                return 0

            # Palabras clave
            kw_fecha = ['fecha', 'date', 'dia']
            kw_tercero = ['tercero', 'beneficiario', 'nombre', 'proveedor']
            kw_valor = ['valor', 'monto', 'importe', 'saldo', 'debito', 'total']
            kw_metodo = ['metodo', 'forma', 'pago', 'medio', 'banco', 'caja']
            kw_concepto = ['concepto', 'detalle', 'descripcion', 'nota']

            # Detección
            idx_f = detectar_idx(df.columns, kw_fecha)
            idx_t = detectar_idx(df.columns, kw_tercero)
            idx_v = detectar_idx(df.columns, kw_valor)
            idx_m = detectar_idx(df.columns, kw_metodo)
            idx_c = detectar_idx(df.columns, kw_concepto)

            st.divider()
            st.success(f"✅ Configuración Automática: Analizando columna '{df.columns[idx_v]}' según método '{df.columns[idx_m]}'.")

            with st.expander("🛠️ Ver/Editar Columnas Seleccionadas"):
                c1, c2, c3, c4 = st.columns(4)
                cf = c1.selectbox("Fecha", df.columns, index=idx_f)
                ct = c2.selectbox("Tercero", df.columns, index=idx_t)
                cv = c3.selectbox("Valor", df.columns, index=idx_v)
                cm = c4.selectbox("Método de Pago", df.columns, index=idx_m)
                cc = st.selectbox("Concepto (Opcional)", df.columns, index=idx_c)

            if st.button("▶️ ANALIZAR RIESGOS FISCALES", type="primary"):
                registrar_log(st.session_state['username'], "Auditoria Gastos", "Inicio escaneo 771-5")
                
                # Optimización: Uso de apply en lugar de iterar con to_dict('records')
                # Pre-calculamos valores seguros numéricos
                df['val_check_safe'] = pd.to_numeric(df[cv], errors='coerce').fillna(0)

                # Definimos una función wrapper para usar en apply
                def wrapper_analisis(row):
                    return analizar_gasto_fila(row, cv, cm, cc)

                # Ejecutamos análisis vectorizado (row-wise pero optimizado por pandas)
                analisis_result = df.apply(wrapper_analisis, axis=1)

                # Expandimos los resultados
                df['Hallazgo_Temp'] = analisis_result.apply(lambda x: x[0])
                df['Riesgo_Temp'] = analisis_result.apply(lambda x: x[1])

                # Filtramos resultados
                df_riesgos = df[df['Riesgo_Temp'] != "BAJO"].copy()
                
                st.divider()
                if df_riesgos.empty:
                    st.balloons()
                    st.success("✅ ¡Excelente! No se encontraron riesgos fiscales evidentes en los gastos analizados.")
                else:
                    st.warning(f"⚠️ Se encontraron {len(df_riesgos)} operaciones con riesgo fiscal.")
                    
                    # Construimos DataFrame de reporte
                    df_res = pd.DataFrame({
                        "Fecha": df_riesgos[cf].astype(str),
                        "Tercero": df_riesgos[ct].astype(str),
                        "Valor": df_riesgos['val_check_safe'].apply(lambda x: f"${x:,.0f}"),
                        "Método Pago": df_riesgos[cm].astype(str),
                        "Riesgo": df_riesgos['Riesgo_Temp'],
                        "Hallazgo": df_riesgos['Hallazgo_Temp']
                    })
                    
                    # Métricas rápidas
                    col_a, col_b = st.columns(2)
                    riesgo_alto = len(df_res[df_res['Riesgo'] == 'ALTO'])
                    col_a.metric("Rechazos Fiscales (Efectivo)", riesgo_alto)
                    col_b.metric("Alertas de Retención", len(df_res) - riesgo_alto)

                    st.dataframe(df_res, use_container_width=True)
                    
                    # Botón Descarga
                    buffer = io.BytesIO()
                    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                        df_res.to_excel(writer, index=False)
                    
                    st.download_button(
                        label="📥 DESCARGAR REPORTE DE HALLAZGOS",
                        data=buffer.getvalue(),
                        file_name="Auditoria_Fiscal_Gastos.xlsx",
                        mime="application/vnd.ms-excel"
                    )

    # --------------------------------------------------------------------------
    # MÓDULO 1: ESCÁNER UGPP (LEY 1393 - REGLA DEL 40%)
    # --------------------------------------------------------------------------
    elif menu == "Escáner de Nómina (UGPP)":
        st.markdown("""<div class='pro-module-header'><img src='https://cdn-icons-png.flaticon.com/512/3135/3135817.png' class='pro-module-icon'><div class='pro-module-title'><h2>Escáner de Riesgo UGPP (Ley 1393)</h2></div></div>""", unsafe_allow_html=True)
        st.markdown("""<div class='detail-box'><strong>Objetivo:</strong> Auditar pagos laborales. Verifica si los pagos NO salariales exceden el 40% del total (Art. 30 Ley 1393).</div>""", unsafe_allow_html=True)
        
        an = st.file_uploader("Cargar Nómina UGPP (.xlsx)", type=['xlsx'], key="upl_ugpp")
        if an:
            dn = pd.read_excel(an)
            
            # FILTRO INTELIGENTE: Solo columnas numéricas
            cols_todas = dn.columns.tolist()
            cols_numericas = dn.select_dtypes(include=['float64', 'int64']).columns.tolist()
            if not cols_numericas: cols_numericas = cols_todas

            # Auto-detección
            def detectar_idx(columnas, keywords):
                cols_str = [str(c).lower().strip() for c in columnas]
                for i, col in enumerate(cols_str):
                    for kw in keywords:
                        if kw in col: return i
                return 0

            idx_e = detectar_idx(cols_todas, ['nombre', 'empleado', 'tercero'])
            idx_s = detectar_idx(cols_numericas, ['salario', 'sueldo', 'basico'])
            
            st.divider()
            with st.expander("🛠️ Configuración de Columnas", expanded=True):
                c1, c2, c3 = st.columns(3)
                cn = c1.selectbox("Empleado", cols_todas, index=idx_e, key="ugpp_n")
                cs = c2.selectbox("Salario Básico", cols_numericas, index=idx_s, key="ugpp_s")
                
                # Opción "Ninguno" por si no hay bonos
                opciones_ns = ["< No Aplica / Es $0 >"] + cols_numericas
                cns = c3.selectbox("Pagos No Salariales (Bonos/Auxilios)", opciones_ns, index=0, key="ugpp_ns")

            if st.button("▶️ ESCANEAR RIESGO UGPP", type="primary"):
                # Optimización: Vectorización con Pandas

                # Conversión numérica segura
                dn['salario_safe'] = pd.to_numeric(dn[cs], errors='coerce').fillna(0)
                if cns == "< No Aplica / Es $0 >":
                    dn['no_salarial_safe'] = 0.0
                else:
                    dn['no_salarial_safe'] = pd.to_numeric(dn[cns], errors='coerce').fillna(0)

                # Cálculos vectorizados
                dn['total_rem'] = dn['salario_safe'] + dn['no_salarial_safe']
                dn['limite_40'] = dn['total_rem'] * 0.40
                dn['exceso'] = dn['no_salarial_safe'] - dn['limite_40']
                # Si no hay exceso (negativo), ponemos 0
                dn['exceso'] = dn['exceso'].clip(lower=0)

                dn['estado'] = dn['exceso'].apply(lambda x: "RIESGO ALTO" if x > 0 else "OK")

                # Construcción del DataFrame de resultados
                df_res = pd.DataFrame({
                    "Empleado": dn[cn].astype(str),
                    "Salario": dn['salario_safe'].apply(lambda x: f"${x:,.0f}"),
                    "No Salarial": dn['no_salarial_safe'].apply(lambda x: f"${x:,.0f}"),
                    "Límite 40%": dn['limite_40'].apply(lambda x: f"${x:,.0f}"),
                    "Exceso IBC": dn['exceso'].apply(lambda x: f"${x:,.0f}"),
                    "Estado": dn['estado']
                })
                
                riesgos = df_res[df_res['Estado'] == "RIESGO ALTO"]
                
                st.divider()
                if riesgos.empty:
                    st.success("✅ ¡Perfecto! Cumples con la norma del 40%.")
                    st.dataframe(df_res, use_container_width=True)
                else:
                    st.error(f"⚠️ {len(riesgos)} empleados exceden el límite del 40%.")
                    st.dataframe(riesgos, use_container_width=True)

    # --------------------------------------------------------------------------
    # MÓDULO: COSTEO DE NÓMINA REAL (EL QUE TÚ BUSCAS 💰)
    # --------------------------------------------------------------------------
    
    elif menu == "Proyección de Tesorería":
        st.markdown("""<div class='pro-module-header'><img src='https://cdn-icons-png.flaticon.com/512/5806/5806289.png' class='pro-module-icon'><div class='pro-module-title'><h2>Radar de Liquidez & Flujo de Caja</h2></div></div>""", unsafe_allow_html=True)
        st.markdown("""<div class='detail-box'><strong>Objetivo:</strong> Visualizar la salud financiera futura cruzando CxC y CxP.</div>""", unsafe_allow_html=True)
        saldo_hoy = st.number_input("💵 Saldo Disponible Hoy ($):", min_value=0.0, format="%.2f")
        c1, c2 = st.columns(2); fcxc = c1.file_uploader("Cartera (CxC)", type=['xlsx']); fcxp = c2.file_uploader("Proveedores (CxP)", type=['xlsx'])
        if fcxc and fcxp:
            dcxc = pd.read_excel(fcxc); dcxp = pd.read_excel(fcxp)
            c1, c2, c3, c4 = st.columns(4)
            cfc = c1.selectbox("Fecha Vencimiento CxC:", dcxc.columns); cvc = c2.selectbox("Valor CxC:", dcxc.columns)
            cfp = c3.selectbox("Fecha Vencimiento CxP:", dcxp.columns); cvp = c4.selectbox("Valor CxP:", dcxp.columns)
            if st.button("▶️ GENERAR PROYECCIÓN"):
                try:
                    dcxc['Fecha'] = pd.to_datetime(dcxc[cfc]); dcxp['Fecha'] = pd.to_datetime(dcxp[cfp])
                    fi = dcxc.groupby('Fecha')[cvc].sum().reset_index(); fe = dcxp.groupby('Fecha')[cvp].sum().reset_index()
                    cal = pd.merge(fi, fe, on='Fecha', how='outer').fillna(0); cal.columns = ['Fecha', 'Ingresos', 'Egresos']; cal = cal.sort_values('Fecha')
                    cal['Saldo Proyectado'] = saldo_hoy + (cal['Ingresos'] - cal['Egresos']).cumsum()
                    st.area_chart(cal.set_index('Fecha')['Saldo Proyectado']); st.dataframe(cal, use_container_width=True)
                    if api_key_valida:
                        with st.spinner("🤖 La IA está analizando tu flujo de caja..."):
                            st.markdown(consultar_ia_gemini(f"Analiza este flujo de caja. Saldo inicial: {saldo_hoy}. Datos: {cal.head(10).to_string()}"))
                except: st.error("Error en el formato de fechas.")

    # ==============================================================================
    # 🚨 MÓDULO DE NÓMINA (CORREGIDO: Auto-Detección y Protección de Errores)
    # ==============================================================================
    elif menu == "Costeo de Nómina Real":
        st.markdown("""<div class='pro-module-header'><img src='https://cdn-icons-png.flaticon.com/512/2328/2328761.png' class='pro-module-icon'><div class='pro-module-title'><h2>Calculadora de Costo Real de Nómina</h2></div></div>""", unsafe_allow_html=True)
        st.markdown("""
        <div class='detail-box'>
            <strong>Objetivo:</strong> Ver el desglose exacto de cuánto le cuesta un empleado a la empresa.<br>
            <strong>Incluye:</strong> Salud, Pensión, ARL, Parafiscales, Primas, Cesantías, Intereses y Vacaciones.
        </div>
        """, unsafe_allow_html=True)
        
        ac = st.file_uploader("Cargar Listado Personal (.xlsx)", type=['xlsx'])
        if ac:
            try:
                dc = pd.read_excel(ac)
                st.info("Configura las columnas (El sistema intenta detectarlas automáticamente):")
                
                # INTENTO DE AUTO-SELECCIÓN (Busca palabras clave en tus títulos)
                cols = list(dc.columns)
                idx_nom = next((i for i, c in enumerate(cols) if "nombre" in c.lower()), 0)
                idx_sal = next((i for i, c in enumerate(cols) if "salario" in c.lower() or "sueldo" in c.lower() or "base" in c.lower()), 0 if len(cols) < 2 else 1)
                idx_aux = next((i for i, c in enumerate(cols) if "aux" in c.lower() or "transporte" in c.lower()), 0 if len(cols) < 3 else 2)
                idx_exo = next((i for i, c in enumerate(cols) if "exo" in c.lower()), 0 if len(cols) < 4 else 3)

                c1, c2, c3, c4 = st.columns(4)
                cn = c1.selectbox("1. Columna Nombre", cols, index=idx_nom)
                cs = c2.selectbox("2. Columna Salario", cols, index=idx_sal)
                ca = c3.selectbox("3. Auxilio Trans (SI/NO)", cols, index=idx_aux)
                ce = c4.selectbox("4. Exonerada (SI/NO)", cols, index=idx_exo)
                
                # Selector opcional de ARL
                c_arl = st.selectbox("5. Nivel ARL (Opcional - Si no seleccionas, asume Nivel 1)", ["No Aplica"] + cols)
                col_arl = c_arl if c_arl != "No Aplica" else None

                if st.button("▶️ CALCULAR DESGLOSE"):
                    rc = []
                    errores = 0
                    for r in dc.to_dict('records'):
                        # PROTECCIÓN: Si el salario no es un número, lo convierte a 0 y avisa
                        try:
                            val_salario = float(r[cs])
                        except:
                            val_salario = 0
                            errores += 1

                        # Calculamos
                        # CORRECCIÓN BUG: La función retorna 4 valores, no 2. Desempaquetamos correctamente.
                        costo_total, total_seg, total_prest, paraf = calcular_costo_empresa_fila(r, cs, ca, col_arl, ce)

                        # Agrupamos para visualización
                        total_aportes_prestaciones = total_seg + total_prest + paraf
                        
                        rc.append({
                            "Empleado": str(r[cn]),
                            "Salario Base": f"${val_salario:,.0f}",
                            "Prestaciones y Aportes": f"${total_aportes_prestaciones:,.0f}",
                            "Costo Total Mensual": f"${costo_total:,.0f}"
                        })
                    
                    if errores > 0:
                        st.warning(f"⚠️ OJO: En {errores} filas el salario no era un número válido (quizás seleccionaste la columna equivocada). Revisa los resultados.")
                    else:
                        st.success("✅ Cálculo exitoso.")
                    
                    st.markdown("### 📊 Resultado del Análisis")
                    st.dataframe(pd.DataFrame(rc), use_container_width=True)

            except Exception as e:
                st.error(f"Error leyendo el archivo: {str(e)}. Revisa que el Excel no tenga filas vacías al inicio.")
    
    # ==============================================================================
    # FIN DE LA CORRECCIÓN DE NÓMINA - CONTINÚAN LOS OTROS MÓDULOS
    # ==============================================================================

    elif menu == "Analítica Financiera Inteligente":
        st.markdown("""<div class='pro-module-header'><img src='https://cdn-icons-png.flaticon.com/512/10041/10041467.png' class='pro-module-icon'><div class='pro-module-title'><h2>Inteligencia Financiera (IA)</h2></div></div>""", unsafe_allow_html=True)
        st.markdown("""<div class='detail-box'><strong>Objetivo:</strong> Detectar patrones de gasto y anomalías en cuentas contables usando IA.</div>""", unsafe_allow_html=True)
        fi = st.file_uploader("Cargar Datos Financieros (.xlsx/.csv)", type=['xlsx', 'csv'])
        if fi and api_key_valida:
            df = pd.read_csv(fi) if fi.name.endswith('.csv') else pd.read_excel(fi)
            c1, c2 = st.columns(2); cd = c1.selectbox("Columna Descripción", df.columns); cv = c2.selectbox("Columna Valor", df.columns)
            if st.button("▶️ INICIAR ANÁLISIS IA"):
                res = df.groupby(cd)[cv].sum().sort_values(ascending=False).head(10); st.bar_chart(res)
                st.markdown(consultar_ia_gemini(f"Actúa como auditor financiero. Analiza estos saldos principales y da recomendaciones: {res.to_string()}"))

    elif menu == "Narrador Financiero & NIIF":
        st.markdown("""<div class='pro-module-header'><img src='https://cdn-icons-png.flaticon.com/512/3208/3208727.png' class='pro-module-icon'><div class='pro-module-title'><h2>Narrador Financiero & Notas NIIF</h2></div></div>""", unsafe_allow_html=True)
        st.markdown("""<div class='detail-box'><strong>Objetivo:</strong> Automatizar la redacción de informes gerenciales y Notas a Estados Financieros.</div>""", unsafe_allow_html=True)
        c1, c2 = st.columns(2); f1 = c1.file_uploader("Año Actual", type=['xlsx']); f2 = c2.file_uploader("Año Anterior", type=['xlsx'])
        if f1 and f2 and api_key_valida:
            d1 = pd.read_excel(f1); d2 = pd.read_excel(f2)
            st.divider(); c1, c2, c3 = st.columns(3); cta = c1.selectbox("Cuenta Contable", d1.columns); v1 = c2.selectbox("Valor Año Actual", d1.columns); v2 = c3.selectbox("Valor Año Anterior", d2.columns)
            if st.button("✨ GENERAR INFORME ESTRATÉGICO"):
                g1 = d1.groupby(cta)[v1].sum().reset_index(name='V_Act'); g2 = d2.groupby(cta)[v2].sum().reset_index(name='V_Ant')
                merged = pd.merge(g1, g2, on=cta, how='inner').fillna(0); merged['Variacion'] = merged['V_Act'] - merged['V_Ant']
                top = merged.reindex(merged.Variacion.abs().sort_values(ascending=False).index).head(10)
                st.markdown("### 📊 Tablero de Control Gerencial"); st.bar_chart(top.set_index(cta)['Variacion'])
                with st.spinner("🤖 El Consultor IA está redactando el informe..."):
                    prompt = f"""Actúa como un CFO experto. Analiza la siguiente tabla de variaciones contables:{top.to_string()} GENERA: 1. Un Informe Gerencial Ejecutivo. 2. Un borrador de Nota a los Estados Financieros bajo NIIF."""
                    st.markdown(consultar_ia_gemini(prompt))

    elif menu == "Validador de RUT Oficial":
        st.markdown("""<div class='pro-module-header'><img src='https://cdn-icons-png.flaticon.com/512/9422/9422888.png' class='pro-module-icon'><div class='pro-module-title'><h2>Validador Oficial de RUT</h2></div></div>""", unsafe_allow_html=True)
        st.markdown("""<div class='detail-box'><strong>Objetivo:</strong> Asegurar la integridad de datos de terceros. Aplica algoritmo de Módulo 11.</div>""", unsafe_allow_html=True)
        nit = st.text_input("Ingrese NIT o Cédula (Sin DV):", max_chars=15)
        if st.button("🔢 VERIFICAR"):
            dv = calcular_dv_colombia(nit); st.metric("Dígito de Verificación (DV)", dv); st.link_button("🔗 Consulta Estado en Muisca (DIAN)", "https://muisca.dian.gov.co/WebRutMuisca/DefConsultaEstadoRUT.faces")

    elif menu == "Digitalización OCR":
        st.markdown("""<div class='pro-module-header'><img src='https://cdn-icons-png.flaticon.com/512/3588/3588241.png' class='pro-module-icon'><div class='pro-module-title'><h2>Digitalización Inteligente (OCR)</h2></div></div>""", unsafe_allow_html=True)
        st.markdown("""<div class='detail-box'><strong>Objetivo:</strong> Eliminar la digitación manual. Usa IA para leer imágenes de facturas.</div>""", unsafe_allow_html=True)
        af = st.file_uploader("Cargar Imágenes", type=["jpg", "png"], accept_multiple_files=True)
        if af and st.button("🧠 PROCESAR IMÁGENES") and api_key_valida:
            do = []; bar = st.progress(0)
            for i, f in enumerate(af): bar.progress((i+1)/len(af)); info = ocr_factura(Image.open(f)); 
            if info: do.append(info)
            st.dataframe(pd.DataFrame(do), use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# PIE DE PÁGINA
# ==============================================================================
st.markdown("---")
st.markdown("<center><strong>Asistente Contable Pro</strong> | v14.5 Enterprise</center>", unsafe_allow_html=True)
