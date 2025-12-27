import streamlit as st
import pandas as pd
import gspread
import google.generativeai as genai
from PIL import Image
import json
import time
import io
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
import os

# ==============================================================================
# ==============================================================================
# 1. CONFIGURACIÓN INICIAL DE LA PÁGINA Y EL SISTEMA
# ==============================================================================
# ==============================================================================

st.set_page_config(
    page_title="Asistente Contable Pro | Enterprise",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. GESTIÓN DE CONEXIONES EXTERNAS (BACKEND)
# ==============================================================================

# ------------------------------------------------------------------------------
# A. CONEXIÓN A BASE DE DATOS (GOOGLE SHEETS)
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
# B. CONFIGURACIÓN DE INTELIGENCIA ARTIFICIAL (GEMINI)
# ------------------------------------------------------------------------------
api_key_valida = False
estado_ia = "🔴 Verificando..."

try:
    if "general" in st.secrets:
        # Configuración de la API Key para servicios de IA Generativa
        GOOGLE_API_KEY = st.secrets["general"]["api_key_google"]
        genai.configure(api_key=GOOGLE_API_KEY)
        estado_ia = "🟢 IA Activa (Enterprise)"
        api_key_valida = True
    else:
        estado_ia = "🔴 IA Desconectada (Falta Key)"
        api_key_valida = False
except Exception as e:
    estado_ia = "🔴 Error Configuración IA"
    api_key_valida = False


# ------------------------------------------------------------------------------
# C. GESTIÓN DE ESTADO DE SESIÓN (SESSION STATE)
# ------------------------------------------------------------------------------
# Inicializamos las variables globales que recordarán si el usuario está logueado
if 'user_plan' not in st.session_state:
    st.session_state['user_plan'] = 'FREE'

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if 'username' not in st.session_state:
    st.session_state['username'] = None


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

# Inyección de CSS para el tema "Cyberpunk / High-Tech Corporativo"
st.markdown("""
    <style>
    /* --- IMPORTACIÓN DE FUENTES --- */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800;900&display=swap');
    
    /* --- VARIABLES DE COLOR DEL TEMA --- */
    :root {
        --primary-blue: #0A66C2; 
        --secondary-blue: #004182;
        --neon-cyan: #00f3ff;
        --neon-purple: #bc13fe;
        --tech-bg: #0f172a; 
        --text-light: #e2e8f0;
        --card-bg: rgba(30, 41, 59, 0.4);
    }

    /* --- AJUSTES GLOBALES DE LA APP --- */
    .stApp {
        background-color: var(--tech-bg) !important;
        color: var(--text-light) !important;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: var(--text-light);
    }

    /* --- ANIMACIÓN DE FONDO PARA LOS MÓDULOS --- */
    @keyframes subtle-shift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .animated-module-bg {
        background: linear-gradient(270deg, #0f172a, #1e293b, #0f172a);
        background-size: 400% 400%;
        animation: subtle-shift 30s ease infinite;
        padding: 30px;
        border-radius: 16px;
        box-shadow: inset 0 0 50px rgba(0,0,0,0.5);
        margin-top: 20px;
        border: 1px solid rgba(255,255,255,0.05);
    }

    /* --- HERO HEADER (BANNER PRINCIPAL) --- */
    .hero-impact-container {
        position: relative;
        width: 100%;
        height: 500px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background: radial-gradient(circle at center, #1e293b 0%, #020617 100%);
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 0 80px rgba(10, 102, 194, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.05);
        margin-bottom: 40px;
        text-align: center;
    }

    .hero-impact-bg {
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background-image: 
            radial-gradient(#ffffff 1px, transparent 1px),
            radial-gradient(#ffffff 1px, transparent 1px);
        background-size: 50px 50px;
        background-position: 0 0, 25px 25px;
        opacity: 0.05;
        animation: moveBackground 60s linear infinite;
    }

    @keyframes moveBackground {
        from { background-position: 0 0, 25px 25px; }
        to { background-position: 100px 100px, 125px 125px; }
    }

    .hero-impact-title {
        font-size: 5.5rem;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: -3px;
        margin: 0;
        background: linear-gradient(135deg, #ffffff 0%, #94a3b8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 60px rgba(10, 102, 194, 0.5);
        z-index: 2;
        animation: fadeInUp 1s ease-out;
    }

    .hero-impact-subtitle {
        font-size: 1.8rem;
        color: #60a5fa;
        font-weight: 400;
        margin-top: 20px;
        z-index: 2;
        background: rgba(15, 23, 42, 0.6);
        padding: 10px 30px;
        border-radius: 50px;
        border: 1px solid rgba(96, 165, 250, 0.3);
        backdrop-filter: blur(5px);
        animation: fadeInUp 1.5s ease-out;
    }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .hero-glow-bottom {
        position: absolute;
        bottom: -100px;
        left: 50%;
        transform: translateX(-50%);
        width: 80%;
        height: 200px;
        background: radial-gradient(ellipse at center, rgba(10, 102, 194, 0.4) 0%, transparent 70%);
        z-index: 1;
        filter: blur(50px);
    }

    /* --- TARJETAS INFORMATIVAS (CARDS) --- */
    .info-card {
        background: var(--card-bg);
        border-left: 5px solid var(--primary-blue);
        padding: 25px;
        border-radius: 12px;
        transition: transform 0.3s ease, background 0.3s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .info-card:hover {
        transform: translateY(-5px);
        background: rgba(30, 41, 59, 0.8);
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    .info-icon { font-size: 2rem; margin-bottom: 10px; display: block; }
    .info-title { font-size: 1.2rem; font-weight: 700; color: white !important; margin-bottom: 8px; }
    .info-text { font-size: 0.95rem; color: #cbd5e1 !important; }

    /* --- ENCABEZADOS DE LOS MÓDULOS --- */
    .pro-module-header {
        display: flex;
        align-items: center;
        background: linear-gradient(90deg, rgba(10, 102, 194, 0.2) 0%, rgba(15, 23, 42, 0) 100%);
        padding: 30px;
        border-radius: 12px;
        border-left: 6px solid var(--primary-blue);
        margin-bottom: 25px;
        backdrop-filter: blur(10px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    .pro-module-icon {
        width: 85px; height: auto; margin-right: 30px;
        filter: drop-shadow(0 5px 10px rgba(0,0,0,0.4)); 
        transition: transform 0.4s ease;
    }
    .pro-module-header:hover .pro-module-icon { transform: scale(1.1) rotate(5deg); }
    .pro-module-title h2 { margin: 0; font-size: 2.4rem; font-weight: 800; color: white !important; letter-spacing: -1px; }

    /* --- CAJAS DE DETALLE Y TEXTO --- */
    .detail-box {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        font-size: 0.95rem;
        color: #cbd5e1;
    }
    .detail-box strong { color: #60a5fa; }

    /* --- BARRA LATERAL (SIDEBAR) --- */
    [data-testid="stSidebar"] {
        background-color: #0b0f19 !important;
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    
    .stRadio > div[role="radiogroup"] > label {
        background: transparent !important; border: none; padding: 12px 5px !important;
        color: #94a3b8 !important; font-weight: 500 !important; font-size: 0.95rem !important;
        transition: all 0.2s;
        border-bottom: 1px solid rgba(255,255,255,0.02);
    }
    .stRadio > div[role="radiogroup"] > label:hover { 
        color: #ffffff !important; padding-left: 10px !important; 
    }
    .stRadio > div[role="radiogroup"] > label[data-checked="true"] {
        color: var(--primary-blue) !important; font-weight: 700 !important;
        background: linear-gradient(90deg, rgba(10, 102, 194, 0.1) 0%, transparent 100%) !important;
        border-left: 3px solid var(--primary-blue);
    }

    /* --- BOTONES PERSONALIZADOS --- */
    .stButton>button {
        background: linear-gradient(135deg, var(--primary-blue) 0%, var(--secondary-blue) 100%) !important;
        color: white !important; border-radius: 8px; font-weight: 700; border: none;
        padding: 15px 30px; height: auto; width: 100%;
        box-shadow: 0 4px 15px rgba(10, 102, 194, 0.3);
        transition: all 0.3s ease;
        text-transform: uppercase; letter-spacing: 1px; font-size: 0.9rem;
    }
    .stButton>button:hover {
        box-shadow: 0 8px 25px rgba(10, 102, 194, 0.6); transform: translateY(-2px);
    }
    
    /* --- SCROLLBAR --- */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #0f172a; }
    ::-webkit-scrollbar-thumb { background: #334155; border-radius: 4px; }
    </style>
    """, unsafe_allow_html=True)

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
# CONEXIÓN CON IA (GEMINI)
# ------------------------------------------------------------------------------
def consultar_ia_gemini(prompt):
    try:
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error de conexión IA: {str(e)}"

# ------------------------------------------------------------------------------
# OCR DE FACTURAS (IA)
# ------------------------------------------------------------------------------
def ocr_factura(imagen):
    try:
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        prompt = """Extrae datos JSON estricto: {"fecha": "YYYY-MM-DD", "nit": "num", "proveedor": "txt", "concepto": "txt", "base": num, "iva": num, "total": num}"""
        response = model.generate_content([prompt, imagen])
        return json.loads(response.text.replace("```json", "").replace("```", "").strip())
    except:
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
    st.markdown("### 💼 Suite Financiera")
    
    # --- LOGICA DE LOGIN Y REGISTRO ---
    if not st.session_state.get('logged_in', False):
        st.warning("🔒 Modo Invitado")
        with st.expander("Ingresar a tu Cuenta", expanded=True):
            u = st.text_input("Usuario (Prueba: admin)")
            p = st.text_input("Contraseña (Prueba: admin)", type="password")
            if st.button("Entrar"):
                # VALIDACIÓN DE CREDENCIALES (SIMULADA + DB)
                if u == "admin" and p == "admin": 
                    st.session_state['user_plan'] = 'PRO'
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = 'Admin'
                    registrar_log("Admin", "Login", "Ingreso exitoso al sistema")
                    st.rerun()
                elif u == "cliente":
                    st.session_state['user_plan'] = 'FREE'
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = 'Cliente'
                    registrar_log("Cliente", "Login", "Ingreso modo Free")
                    st.rerun()
                else:
                    st.error("❌ Acceso Denegado")
                    registrar_log(u, "Login Fallido", "Contraseña incorrecta")
    
    # --- PANEL DE USUARIO LOGUEADO ---
    else:
        plan_bg = "#FFD700" if st.session_state['user_plan'] == 'PRO' else "#A9A9A9"
        status_db = "🟢 DB Online" if db_conectada else "🔴 DB Offline"
        
        st.markdown(f"""
        <div style='background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; border-left: 5px solid {plan_bg}; margin-bottom: 20px;'>
            <small style='color: #cbd5e1;'>Bienvenido,</small><br>
            <strong style='font-size: 1.1rem;'>Usuario {st.session_state['user_plan']}</strong><br>
            <small>{estado_ia}</small><br>
            <small style='color: {'#22c55e' if db_conectada else '#ef4444'}; font-weight:bold;'>{status_db}</small>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state['user_plan'] == 'FREE':
            st.markdown("---")
            st.write("🔓 Desbloquea todo el potencial")
            # Enlace de pago WOMPI
            st.link_button(
                "💎 COMPRAR PLAN PRO", 
                "https://checkout.wompi.co/l/TU_LINK_AQUI" 
            )
            st.caption("Una vez pagues, envía el comprobante.")

        if st.button("Cerrar Sesión"):
            registrar_log(st.session_state['username'], "Logout", "Salida del sistema")
            st.session_state['logged_in'] = False
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
    
    if not st.session_state.get('logged_in', False):
        menu = "Inicio / Dashboard"
    else:
        menu = st.radio("Módulos Operativos:", opciones_menu)
    
    st.markdown("<br><center><small style='color: #64748b;'>v14.5 Enterprise</small></center>", unsafe_allow_html=True)

# ==============================================================================
# ==============================================================================
# 6. CONTENIDO PRINCIPAL (DASHBOARD Y MÓDULOS)
# ==============================================================================
# ==============================================================================

if menu == "Inicio / Dashboard":
    # HERO HEADER NUEVO (High-Tech)
    st.markdown(f"""
    <div class='hero-impact-container'>
        <div class='hero-impact-bg'></div>
        <div class='hero-glow-bottom'></div>
        <div style="z-index: 2; padding: 20px;">
            <h1 class='hero-impact-title'>ASISTENTE CONTABLE PRO</h1>
            <div class='hero-impact-subtitle'>{saludo}. Plataforma de Inteligencia Financiera Corporativa.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # SECCIÓN DE BIENVENIDA
    st.markdown("""
    <div style='text-align: center; margin-bottom: 40px;'>
        <h3 style='color: #fff; font-size: 2rem; margin-bottom: 10px;'>🚀 La Evolución de la Contabilidad</h3>
        <p style='font-size: 1.1rem; color: #94a3b8; max-width: 800px; margin: 0 auto;'>
            Esta suite Enterprise ha sido diseñada para automatizar lo operativo y dejarte tiempo para lo estratégico. 
            <strong>Precisión algorítmica, velocidad de procesamiento y análisis profundo con IA.</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # GRID DE HERRAMIENTAS
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown("""<div class='info-card'><span class='info-icon'>⚖️</span><div class='info-title'>Auditoría Fiscal</div><div class='info-text'>Cruces automáticos DIAN vs Contabilidad para evitar sanciones.</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class='info-card'><span class='info-icon'>📧</span><div class='info-title'>Minería XML</div><div class='info-text'>Extracción masiva de datos fiscales directamente de la fuente.</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""<div class='info-card'><span class='info-icon'>🤝</span><div class='info-title'>Conciliación IA</div><div class='info-text'>Matching bancario inteligente con lógica difusa.</div></div>""", unsafe_allow_html=True)
    with c4:
        st.markdown("""<div class='info-card'><span class='info-icon'>📈</span><div class='info-title'>Reportes NIIF</div><div class='info-text'>Redacción automática experta de notas a estados financieros.</div></div>""", unsafe_allow_html=True)

    st.markdown("---")
    
    st.subheader("Protocolo de Activación IA")
    col_a, col_b, col_c = st.columns(3)
    with col_a: st.info("1. Acceso Seguro: Entra a Google AI Studio con credenciales corporativas.")
    with col_b: st.info("2. Generación: Crea tu API Key y configúrala en el sistema.")
    with col_c: st.info("3. Vinculación: El sistema desbloqueará automáticamente los módulos predictivos.")

    if not db_conectada:
        st.warning("⚠️ La base de datos no está conectada. Asegúrate de compartir el Google Sheet 'DB_Alcontador' con el email del Service Account.")

# ------------------------------------------------------------------------------
# CONTENIDO DE MÓDULOS DETALLADOS
# ------------------------------------------------------------------------------
else:
    st.markdown('<div class="animated-module-bg">', unsafe_allow_html=True)

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
            df_dian = pd.read_excel(file_dian); df_conta = pd.read_excel(file_conta)
            st.divider(); st.info("⚙️ Configuración del Mapeo (Selecciona las columnas)")
            c1, c2, c3, c4 = st.columns(4)
            nit_dian = c1.selectbox("NIT (Archivo DIAN):", df_dian.columns)
            val_dian = c2.selectbox("Valor (Archivo DIAN):", df_dian.columns)
            nit_conta = c3.selectbox("NIT (Tu Contabilidad):", df_conta.columns)
            val_conta = c4.selectbox("Saldo (Tu Contabilidad):", df_conta.columns)
            if st.button("▶️ EJECUTAR AUDITORÍA BLINDADA"):
                registrar_log(st.session_state['username'], "Auditoria", "Ejecución cruce DIAN")
                dian_grouped = df_dian.groupby(nit_dian)[val_dian].sum().reset_index(name='Valor_DIAN').rename(columns={nit_dian: 'NIT'})
                conta_grouped = df_conta.groupby(nit_conta)[val_conta].sum().reset_index(name='Valor_Conta').rename(columns={nit_conta: 'NIT'})
                cruce = pd.merge(dian_grouped, conta_grouped, on='NIT', how='outer').fillna(0)
                cruce['Diferencia'] = cruce['Valor_DIAN'] - cruce['Valor_Conta']
                diferencias = cruce[abs(cruce['Diferencia']) > 1000].sort_values(by="Diferencia", ascending=False)
                total_riesgo = diferencias['Diferencia'].abs().sum(); num_hallazgos = len(diferencias)
                st.divider(); st.markdown(f"### 🔍 Resultados del Escáner")
                if num_hallazgos == 0:
                    st.success("✅ ¡Felicidades! Tu contabilidad es perfecta. No hay diferencias materiales.")
                else:
                    st.error(f"⚠️ ¡ALERTA! Se detectaron {num_hallazgos} inconsistencias graves.")
                    col_met1, col_met2 = st.columns(2)
                    col_met1.metric("Riesgo Financiero Total", f"${total_riesgo:,.0f}"); col_met2.metric("Terceros con Error", num_hallazgos)
                    if st.session_state.get('user_plan') == 'FREE':
                        st.markdown("#### 👁️ Vista Previa (Modo Gratuito)")
                        st.dataframe(diferencias.head(2).style.format("{:,.0f}"), use_container_width=True)
                        st.markdown(f"""<div style="margin-top: 20px; padding: 30px; border-radius: 15px; border: 1px solid #334155; background: radial-gradient(circle, rgba(15,23,42,1) 0%, rgba(30,41,59,1) 100%); text-align: center; position: relative; overflow: hidden;"><div style="filter: blur(6px); opacity: 0.3; user-select: none;"><p>NIT: 900.123.456 | Diferencia: $45.000.000 | ESTADO: CRÍTICO</p><p>NIT: 890.987.654 | Diferencia: $12.500.000 | ESTADO: CRÍTICO</p></div><div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center; background: rgba(0,0,0,0.4); backdrop-filter: blur(2px);"><h2 style="color: #fff; text-shadow: 0 0 10px #0A66C2;">🔒 REPORTE BLOQUEADO</h2><p style="color: #cbd5e1; font-size: 1.1rem;">Riesgo oculto: <strong>${total_riesgo:,.0f}</strong></p><a href="#" style="background: linear-gradient(90deg, #0A66C2 0%, #00d4ff 100%); color: white; padding: 15px 30px; border-radius: 30px; text-decoration: none; font-weight: bold;">🔓 DESBLOQUEAR TODO POR $59.000</a></div></div>""", unsafe_allow_html=True)
                    else:
                        st.success("💎 ACCESO VIP: Mostrando auditoría completa.")
                        st.dataframe(diferencias.style.format("{:,.0f}"), use_container_width=True)
                        out = io.BytesIO()
                        with pd.ExcelWriter(out, engine='xlsxwriter') as w: diferencias.to_excel(w, index=False)
                        st.download_button("📥 Descargar Reporte Oficial (.xlsx)", out.getvalue(), f"Auditoria_DIAN_{datetime.now().date()}.xlsx")

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
        st.markdown("""<div class='detail-box'><strong>Objetivo:</strong> Automatizar el emparejamiento de transacciones entre el Extracto Bancario y el Libro Auxiliar de Bancos usando lógica difusa.</div>""", unsafe_allow_html=True)
        col_banco, col_libro = st.columns(2)
        with col_banco: st.subheader("🏦 Extracto Bancario"); file_banco = st.file_uploader("Subir Excel Banco", type=['xlsx'])
        with col_libro: st.subheader("📒 Libro Auxiliar"); file_libro = st.file_uploader("Subir Excel Contabilidad", type=['xlsx'])
        if file_banco and file_libro:
            df_banco = pd.read_excel(file_banco); df_libro = pd.read_excel(file_libro)
            st.divider(); c1, c2, c3, c4 = st.columns(4)
            col_fecha_b = c1.selectbox("Fecha Banco:", df_banco.columns, key="fb"); col_valor_b = c2.selectbox("Valor Banco:", df_banco.columns, key="vb")
            col_fecha_l = c3.selectbox("Fecha Libro:", df_libro.columns, key="fl"); col_valor_l = c4.selectbox("Valor Libro:", df_libro.columns, key="vl")
            col_desc_b = st.selectbox("Descripción Banco:", df_banco.columns, key="db")
            if st.button("▶️ EJECUTAR CONCILIACIÓN"):
                registrar_log(st.session_state['username'], "Conciliacion", "Inicio matching bancario")
                df_banco['Fecha_Dt'] = pd.to_datetime(df_banco[col_fecha_b]); df_libro['Fecha_Dt'] = pd.to_datetime(df_libro[col_fecha_l])
                df_banco['Conciliado'] = False; df_libro['Conciliado'] = False; matches = []
                bar = st.progress(0)
                for idx_b, row_b in df_banco.iterrows():
                    bar.progress((idx_b+1)/len(df_banco)); vb = row_b[col_valor_b]; fb = row_b['Fecha_Dt']
                    cands = df_libro[(df_libro[col_valor_l] == vb) & (~df_libro['Conciliado']) & (df_libro['Fecha_Dt'].between(fb-timedelta(days=3), fb+timedelta(days=3)))]
                    if not cands.empty:
                        df_banco.at[idx_b, 'Conciliado']=True; df_libro.at[cands.index[0], 'Conciliado']=True
                        matches.append({"Fecha": row_b[col_fecha_b], "Desc": row_b[col_desc_b], "Valor": vb, "Estado": "✅ OK"})
                st.success(f"Proceso finalizado. {len(matches)} partidas conciliadas automáticamente.")
                t1, t2, t3 = st.tabs(["✅ Partidas Cruzadas", "⚠️ Pendientes en Banco", "⚠️ Pendientes en Libros"])
                with t1: st.dataframe(pd.DataFrame(matches), use_container_width=True)
                with t2: st.dataframe(df_banco[~df_banco['Conciliado']], use_container_width=True)
                with t3: st.dataframe(df_libro[~df_libro['Conciliado']], use_container_width=True)

    elif menu == "Auditoría Fiscal de Gastos":
        st.markdown("""<div class='pro-module-header'><img src='https://cdn-icons-png.flaticon.com/512/1642/1642346.png' class='pro-module-icon'><div class='pro-module-title'><h2>Auditoría Fiscal Masiva (Art. 771-5)</h2></div></div>""", unsafe_allow_html=True)
        st.markdown("""<div class='detail-box'><strong>Objetivo:</strong> Verificar el cumplimiento de los requisitos de deducibilidad (Bancarización, Retención).</div>""", unsafe_allow_html=True)
        ar = st.file_uploader("Cargar Auxiliar de Gastos (.xlsx)", type=['xlsx'])
        if ar:
            df = pd.read_excel(ar)
            c1, c2, c3, c4 = st.columns(4)
            cf = c1.selectbox("Fecha", df.columns); ct = c2.selectbox("Tercero", df.columns); cv = c3.selectbox("Valor", df.columns); cm = c4.selectbox("Método de Pago", ["No disponible"]+list(df.columns))
            cc = st.selectbox("Concepto (Opcional)", df.columns)
            if st.button("▶️ ANALIZAR RIESGOS"):
                res = []
                for r in df.to_dict('records'):
                    h, rs = analizar_gasto_fila(r, cv, cm, cc)
                    if rs != "BAJO": res.append({"Fecha": r[cf], "Tercero": r[ct], "Valor": r[cv], "Riesgo": rs, "Hallazgo": h})
                if res: st.warning(f"Se encontraron {len(res)} operaciones con riesgo fiscal."); st.dataframe(pd.DataFrame(res), use_container_width=True)
                else: st.success("No se encontraron riesgos fiscales evidentes.")

    elif menu == "Escáner de Nómina (UGPP)":
        st.markdown("""<div class='pro-module-header'><img src='https://cdn-icons-png.flaticon.com/512/3135/3135817.png' class='pro-module-icon'><div class='pro-module-title'><h2>Escáner de Riesgo UGPP (Ley 1393)</h2></div></div>""", unsafe_allow_html=True)
        st.markdown("""<div class='detail-box'><strong>Objetivo:</strong> Auditar los pagos laborales para evitar sanciones. Verifica la regla del 40% (Art. 30 Ley 1393).</div>""", unsafe_allow_html=True)
        an = st.file_uploader("Cargar Nómina (.xlsx)", type=['xlsx'])
        if an:
            dn = pd.read_excel(an)
            c1, c2, c3 = st.columns(3)
            cn = c1.selectbox("Empleado", dn.columns); cs = c2.selectbox("Salario Básico", dn.columns); cns = c3.selectbox("Pagos No Salariales", dn.columns)
            if st.button("▶️ ESCANEAR NÓMINA"):
                res = []
                for r in dn.to_dict('records'):
                    ibc, exc, est, msg = calcular_ugpp_fila(r, cs, cns)
                    res.append({"Empleado": r[cn], "IBC Ajustado": ibc, "Exceso": exc, "Estado": est, "Detalle": msg})
                st.dataframe(pd.DataFrame(res), use_container_width=True)

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
                        c, cr = calcular_costo_empresa_fila(r, cs, ca, col_arl, ce)
                        
                        rc.append({
                            "Empleado": str(r[cn]),
                            "Salario Base": f"${val_salario:,.0f}",
                            "Prestaciones y Aportes": f"${cr:,.0f}",
                            "Costo Total Mensual": f"${c:,.0f}"
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
st.markdown("<center><strong>Asistente Contable Pro</strong> | Enterprise Financial Suite</center>", unsafe_allow_html=True)