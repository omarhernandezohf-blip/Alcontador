import textwrap
import streamlit as st
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
import io
import threading
import gc
import plotly.express as px

try:
    from streamlit_oauth import OAuth2Component
    OAUTH_OK = True
except ImportError:
    OAUTH_OK = False
    OAuth2Component = None
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
import uuid
import firebase_admin
from firebase_admin import credentials, firestore

# --- CONFIGURACIÓN DE PÁGINA (PRIMERO QUE TODO) ---
st.set_page_config(
    page_title="Asistente Contable Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)
# Force Reload: 2026-01-06 13:50:00

# --- MENÚ LATERAL (MOVIDO AL INICIO PARA GARANTIZAR VISIBILIDAD) ---
with st.sidebar:
    # Idioma fijado en Español por defecto, eliminamos el selector para evitar confusión.
    
    st.markdown("---")
    
    # ⚖️ LEGAL Y CORPORATIVO (BLINDAJE JURÍDICO)
    # ==============================================================================
    with st.expander("⚖️ LEGAL Y CORPORATIVO"):
        st.markdown("""
        **(1) TÉRMINOS DE USO**
        **Obligación de Medio:** Este software actúa como herramienta de asistencia tecnológica y NO sustituye el criterio profesional del Contador Público.
        **Responsabilidad:** No asumimos responsabilidad por sanciones de la DIAN/UGPP derivadas del uso de esta plataforma.
        **Pagos:** El usuario acepta el cobro anticipado por servicios SaaS.

        **(2) POLÍTICA DE PRIVACIDAD (Habeas Data)**
        Cumplimiento Ley 1581/2012. Sus datos financieros se procesan con cifrado y confidencialidad. 
        **Derechos:** Solicite la supresión de datos vía soporte cuando lo desee.

        **(3) QUIÉNES SOMOS**
        Proveedor de Tecnología SaaS enfocado en la automatización contable inteligente.
        """)
        
    st.markdown("---")
    
    # --- MENÚ PRINCIPAL ---
    try:
        from streamlit_option_menu import option_menu
        # Usamos la lista COMPLETA de módulos para no romper la navegación
        menu = option_menu(
            menu_title="Navegación",
            options=[
                "Inicio / Dashboard",
                "🏢 Quiénes Somos / Historia",
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
                "Digitalización OCR",
                "Generador de Cotizaciones",
                "Generador Logístico",
                "👑 Consola Administrativa"
            ],
            icons=[
                "house", "building", "shield-check", "file-earmark-code", "bank", "graph-up",
                "people", "cash-coin", "calculator", "cpu", "book", "check-circle", "camera",
                "file-earmark-pdf",
                "airplane-engines",
                "key"
            ],
            menu_icon="cast",
            default_index=0,
        )
    except ImportError:
        # Fallback seguro si la librería no está instalada
        st.warning("Librería 'streamlit-option-menu' no detectada. Usando selector estándar.")
        menu = st.radio(
            "Navegación",
            [
                "Inicio / Dashboard",
                "🏢 Quiénes Somos / Historia",
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
                "Digitalización OCR",
                "Generador de Cotizaciones",
                "Generador Logístico",
                "👑 Consola Administrativa"
            ]
        )



# --- CONFIGURACIÓN DE ESTILO GLOBAL (SIDEBAR CLÁSICO MEJORADO) ---
# --- CONFIGURACIÓN DE ESTILO GLOBAL (SIDEBAR CLÁSICO MEJORADO) ---
# La normativa se movió al final de la barra lateral (después del chat)

st.markdown("""
    <style>
        /* 1. FONDO UNIVERSO ANIMADO MEJORADO */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@400;600;700&display=swap');
        
        .stApp {
            background: radial-gradient(ellipse at top, #0f0c29 0%, #302b63 50%, #24243e 100%) !important;
            background-attachment: fixed !important;
            font-family: 'Inter', sans-serif !important;
        }
        
        /* 3. SIDEBAR GLASSMORPHISM */
        [data-testid="stSidebar"] {
            background: rgba(15, 23, 42, 0.85) !important;
            backdrop-filter: blur(20px) saturate(180%) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
            box-shadow: 10px 0 30px rgba(0, 0, 0, 0.3) !important;
        }
        
        /* 4. TARJETAS NEOMORFISMO + GLASS */
        .glass-card, div[data-testid="stExpander"] {
            background: rgba(255, 255, 255, 0.05) !important;
            backdrop-filter: blur(15px) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 20px !important;
            box-shadow: 
                0 8px 32px rgba(0, 0, 0, 0.2),
                inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
            padding: 24px !important;
            margin-bottom: 24px !important;
            transition: all 0.3s ease !important;
        }
        
        .glass-card:hover {
            border-color: rgba(102, 126, 234, 0.4) !important;
            box-shadow: 
                0 15px 40px rgba(102, 126, 234, 0.25),
                inset 0 1px 0 rgba(255, 255, 255, 0.15) !important;
            transform: translateY(-5px) !important;
        }
        
        /* 5. BOTONES MODERNOS */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            border: none !important;
            border-radius: 12px !important;
            color: white !important;
            font-weight: 600 !important;
            padding: 12px 24px !important;
            font-family: 'Inter', sans-serif !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5) !important;
        }
        
        /* 6. INPUTS Y SELECT ESTILIZADOS */
        .stTextInput > div > div > input,
        .stSelectbox > div > div > select {
            background: rgba(255, 255, 255, 0.08) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px !important;
            color: white !important;
            padding: 12px 16px !important;
            font-family: 'Inter', sans-serif !important;
            backdrop-filter: blur(10px) !important;
        }
        
        .stTextInput > div > div > input:focus,
        .stSelectbox > div > div > select:focus {
            border-color: #667eea !important;
            box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2) !important;
        }
        
        /* 7. TABLAS MODERNAS */
        .dataframe {
            background: rgba(255, 255, 255, 0.05) !important;
            border-radius: 12px !important;
            overflow: hidden !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
        }
        
        .dataframe th {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%) !important;
            color: white !important;
            font-weight: 700 !important;
            border: none !important;
        }
        
        .dataframe td {
            border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
            color: #e2e8f0 !important;
        }
        
        /* 8. PROGRESS BAR ANIMADO */
        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, #667eea, #764ba2, #f093fb) !important;
            background-size: 200% 100% !important;
            animation: gradientShift 2s ease infinite !important;
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        /* 9. HEADERS CON GRADIENTE */
        h1, h2, h3 {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            background-clip: text !important;
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 800 !important;
            letter-spacing: -0.5px !important;
        }
        
        /* 10. METRIC CARDS GLOW */
        [data-testid="stMetricValue"] {
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 800 !important;
            font-size: 2.2rem !important;
            background: linear-gradient(135deg, white 0%, #a5b4fc 100%) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            background-clip: text !important;
        }
        
        /* 11. SCROLLBAR PERSONALIZADO */
        ::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px;
        }
        
        /* 12. CHART CONTAINERS */
        .stPlotlyChart, .stPydeckChart, .stGraphvizChart {
            border-radius: 20px !important;
            overflow: hidden !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            background: rgba(255, 255, 255, 0.05) !important;
            padding: 15px !important;
        }
        
        /* 13. EXPANDER MODERNO */
        .stExpander {
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px !important;
            margin-bottom: 16px !important;
        }
        
        /* 14. NOTIFICACIONES Y TOAST */
        .stAlert {
            border-radius: 12px !important;
            border: none !important;
            background: rgba(255, 255, 255, 0.08) !important;
            backdrop-filter: blur(10px) !important;
        }
        
        /* 15. LOGIN SECTION ENHANCED */
        .login-container {
            background: rgba(15, 23, 42, 0.8) !important;
            backdrop-filter: blur(30px) !important;
            border-radius: 30px !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            padding: 40px !important;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4) !important;
        }
        
        /* 16. DIVIDER GLOW */
        hr {
            border: none !important;
            height: 2px !important;
            background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.5), transparent) !important;
            margin: 40px 0 !important;
        }
        
        /* 17. MENU OPTION HOVER */
        [data-testid="stSidebar"] .st-emotion-cache-16txtl3 {
            padding: 12px 20px !important;
            margin: 4px 0 !important;
            border-radius: 12px !important;
            transition: all 0.3s ease !important;
        }
        
        [data-testid="stSidebar"] .st-emotion-cache-16txtl3:hover {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%) !important;
            transform: translateX(5px) !important;
        }
        
        /* 18. PULSING ANIMATION */
        @keyframes pulse-glow {
            0% { box-shadow: 0 0 0 0 rgba(102, 126, 234, 0.7); }
            70% { box-shadow: 0 0 0 10px rgba(102, 126, 234, 0); }
            100% { box-shadow: 0 0 0 0 rgba(102, 126, 234, 0); }
        }
        
        .pulse {
            animation: pulse-glow 2s infinite;
        }
        
        /* 19. SPINNER CUSTOM */
        .stSpinner > div {
            border-color: #667eea transparent transparent transparent !important;
        }
        
        /* 20. FOOTER STYLING */
        footer {
            color: rgba(255, 255, 255, 0.5) !important;
            font-size: 0.9rem !important;
            text-align: center !important;
            padding: 20px !important;
            margin-top: 40px !important;
            border-top: 1px solid rgba(255, 255, 255, 0.1) !important;
        }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 0. CONFIGURACIÓN DE PLANES Y FIRESTORE
# ==============================================================================

@st.cache_resource
def get_star_css():
    """Generates the CSS for the moving universe background (cached)."""
    def get_star_shadows(n):
        return ", ".join([f"{random.randint(0, 4000)}px {random.randint(0, 4000)}px #FFF" for _ in range(n)])

    shadows_small = get_star_shadows(400)
    shadows_medium = get_star_shadows(100)
    shadows_big = get_star_shadows(50)

    return f"""
    <style>
        /* Universe Animation Keyframes */
        @keyframes animStar {{
            from {{ transform: translateY(0px); }}
            to {{ transform: translateY(-4000px); }}
        }}

        /* Background Container */
        .universe-bg {{
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: radial-gradient(ellipse at bottom, #1B2735 0%, #090A0F 100%);
            z-index: 0;
            overflow: hidden;
            pointer-events: none; /* Allows clicking through to form */
        }}

        .star-layer {{
            background: transparent;
            position: absolute;
            top: 0; left: 0;
        }}

        /* Layer 1: Small Stars */
        .layer-1 {{ width: 1px; height: 1px; box-shadow: {shadows_small}; animation: animStar 150s linear infinite; }}
        .layer-1:after {{ content: " "; position: absolute; top: 4000px; width: 1px; height: 1px; box-shadow: {shadows_small}; }}

        /* Layer 2: Medium Stars */
        .layer-2 {{ width: 2px; height: 2px; box-shadow: {shadows_medium}; animation: animStar 100s linear infinite; }}
        .layer-2:after {{ content: " "; position: absolute; top: 4000px; width: 2px; height: 2px; box-shadow: {shadows_medium}; }}

        /* Layer 3: Large Stars */
        .layer-3 {{ width: 3px; height: 3px; box-shadow: {shadows_big}; animation: animStar 150s linear infinite; }}
        .layer-3:after {{ content: " "; position: absolute; top: 4000px; width: 3px; height: 3px; box-shadow: {shadows_big}; }}
    </style>

    <div class="universe-bg">
        <div class="star-layer layer-1"></div>
        <div class="star-layer layer-2"></div>
        <div class="star-layer layer-3"></div>
    </div>
    """

def render_universe_background():
    """Injects the universe background CSS/HTML."""
    st.markdown(get_star_css(), unsafe_allow_html=True)

# Render background immediately
render_universe_background()

PLAN_CONFIG = {
    'FREE': {
        'limit': 5,
        'model': 'gemini-1.5-flash',
        'price_display': 'GRATIS',
        'badge': 'Prueba',
        'name': 'Free'
    },
    'PRO': {
        'limit': 500,
        'model': 'gemini-1.5-flash',
        'price_display': '$70.000 COP',
        'badge': '⭐ Más Popular',
        'name': 'Pro'
    },
    'PREMIUM': {
        'limit': 2000,
        'model': 'gemini-1.5-flash',
        'price_display': '$120.000 COP',
        'badge': '🧠 Inteligencia Superior',
        'name': 'Premium'
    }
}

@st.cache_resource
def init_firestore():
    """Inicializa la app de Firebase Admin una sola vez."""
    try:
        if not firebase_admin._apps:
            # Usamos las credenciales de GCP Service Account que ya existen
            cred = credentials.Certificate(dict(st.secrets["gcp_service_account"]))
            firebase_admin.initialize_app(cred)
        return firestore.client()
    except Exception as e:
        # En caso de error (ej. falta de secretos), retornamos None para manejarlo gracefully
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

def log_user_action(email, action_text):
    """Guarda un registro de actividad del usuario en Firestore."""
    if not email: return
    db = get_firestore_db()
    if not db: return
    try:
        hist_ref = db.collection('users').document(email).collection('history')
        hist_ref.add({
            'action': action_text,
            'timestamp': firestore.SERVER_TIMESTAMP
        })
    except Exception as e:
        pass

def get_user_history(email, limit=4):
    """Obtiene los últimos N registros de actividad del usuario."""
    if not email: return []
    db = get_firestore_db()
    if not db: return []
    try:
        hist_ref = db.collection('users').document(email).collection('history')
        query = hist_ref.order_by('timestamp', direction=firestore.Query.DESCENDING).limit(limit)
        docs = query.stream()
        history = []
        for doc in docs:
            data = doc.to_dict()
            history.append(data)
        return history
    except Exception as e:
        return []

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

def check_single_session():
    """Verifica la sesión al inicio de cada ejecución."""
    if st.session_state.get('logged_in'):
        email = st.session_state.get('user_email')
        token = st.session_state.get('session_token')

        if email and token:
            if not verify_session(email, token):
                st.session_state.clear()
                st.error("⚠️ Tu sesión se ha abierto en otro dispositivo. Por seguridad, se ha cerrado aquí.")
                st.stop()

# Ejecutar verificación de sesión inmediatamente
check_single_session()

# Lógica de registro de historial (Firestore)
if 'last_menu' not in st.session_state:
    st.session_state['last_menu'] = menu
    # No registramos el primer render
elif st.session_state['last_menu'] != menu:
    st.session_state['last_menu'] = menu
    if st.session_state.get('logged_in'):
        email = st.session_state.get('user_email')
        if email:
            log_user_action(email, f"Consultó el módulo: {menu}")

# ==============================================================================
# 0.1 INTERNATIONALIZATION & HELPERS (NEW & RESTORED)
# ==============================================================================

TRANSLATIONS = {
    'Español': {
        'menu_dash': "Inicio / Dashboard",
        'menu_dian': "Auditoría Cruce DIAN",
        'menu_xml': "Minería de XML (Facturación)",
        'menu_bank': "Conciliación Bancaria IA",
        'menu_fiscal': "Auditoría Fiscal de Gastos",
        'menu_ugpp': "Escáner de Nómina (UGPP)",
        'menu_treasury': "Proyección de Tesorería",
        'menu_payroll': "Costeo de Nómina Real",
        'menu_fin_ai': "Analítica Financiera Inteligente",
        'menu_narrator': "Narrador Financiero & NIIF",
        'menu_rut': "Validador de RUT Oficial",
        'menu_ocr': "Digitalización OCR",

        # --- UI LABELS (Sidebar & Login) ---
        'lbl_operator': "OPERADOR:",
        'lbl_access': "ACCESO",
        'lbl_modules': "MÓDULOS DEL SISTEMA:",
        'lbl_logout': "CERRAR SESIÓN",
        'lbl_unlock': "DESBLOQUEAR SISTEMA",
        'lbl_go_pro': "💎 PASAR A PRO ($70k)",
        'lbl_go_prem': "🧠 PASAR A PREMIUM ($120k)",
        'lbl_credits': "Créditos:",

        'login_title': "Asistente Contable <span style='color: var(--primary)'>PRO</span>",
        'login_subtitle': "v14.5 Suite Empresarial • Sistema En Línea",
        'login_btn_google': "🔐 Iniciar sesión con Google",
        'login_error_config': "Error de configuración de Google Auth.",
        'login_no_auth': "⚠️ AUTENTICACIÓN GOOGLE NO DISPONIBLE",
        'login_privacy_title': "Privacidad y Seguridad:",
        'login_privacy_desc': "Tus datos son procesados en tiempo real y no se almacenan permanentemente en nuestros servidores.",
        'login_manual_header': "⚠️ ACCESO DE EMERGENCIA",
        'login_manual_help': "Use este canal si Google Auth falla (Error 403/500).",
        'login_input_id': "ID Operador",
        'login_input_pass': "Clave de Acceso",
        'login_btn_manual': "INICIAR ACCESO MANUAL",
        'login_error_creds': "❌ CREDENCIALES INVÁLIDAS",

        # Guide Content
        'title_treasury': "Radar de Liquidez & Flujo de Caja",
        'desc_treasury': "Gestión estratégica de tesorería que permite visualizar la salud financiera futura cruzando en tiempo real las Cuentas por Cobrar (Ingresos proyectados) contra las Cuentas por Pagar (Compromisos). Fundamental para evitar brechas de liquidez.",
        'ben_treasury': ["Proyección de saldo disponible", "Alerta de déficit de caja", "Visualización gráfica de brechas"],

        'title_fin_ai': "Inteligencia Financiera (IA)",
        'desc_fin_ai': "Potente motor de análisis que utiliza algoritmos de Inteligencia Artificial para auditar el 100% de sus movimientos contables, detectando anomalías, patrones de gasto inusuales y desviaciones presupuestales que pasarían desapercibidas al ojo humano.",
        'ben_fin_ai': ["Detección de anomalías en gastos", "Auditoría preventiva automática", "Identificación de patrones ocultos"],

        'title_narrator': "Narrador Financiero & Notas NIIF",
        'desc_narrator': "Transforma datos numéricos complejos en narrativa de negocios clara y concisa. Automatiza la redacción de informes gerenciales y las revelaciones (Notas) requeridas por las Normas Internacionales de Información Financiera (NIIF).",
        'ben_narrator': ["Redacción automática de notas NIIF", "Informes gerenciales en segundos", "Interpretación cualitativa de cifras"],

        'title_rut': "Validador Oficial de RUT",
        'desc_rut': "Herramienta de cumplimiento tributario que verifica la integridad de los Números de Identificación Tributaria (NIT) utilizando el algoritmo oficial de 'Módulo 11' de la DIAN, asegurando que sus terceros estén correctamente registrados.",
        'ben_rut': ["Validación de Dígito de Verificación", "Prevención de errores en exógena", "Algoritmo oficial DIAN"],

        'title_ocr': "Digitalización Inteligente (OCR)",
        'desc_ocr': "Sistema de Reconocimiento Óptico de Caracteres que extrae automáticamente la información clave de facturas físicas o imágenes, eliminando la digitación manual, reduciendo errores humanos y acelerando el procesamiento contable.",
        'ben_ocr': ["Cero digitación manual", "Procesamiento masivo de facturas", "Ahorro de tiempo administrativo"],

        'title_dian': "Auditor de Exógena (Cruce DIAN)",
        'desc_dian': "Detectar discrepancias entre lo que reportaste y lo que la DIAN sabe de ti. Cruce matricial de NITs para evitar sanciones por inexactitud (Art. 651 ET).",
        'ben_dian': ["Evita sanciones del Art. 651", "Cruce automático de NITs", "Reporte detallado de diferencias"],

        'title_xml': "Minería de Datos XML (Facturación)",
        'desc_xml': "Extraer información estructurada directamente de los archivos XML de Facturación Electrónica validados por la DIAN.",
        'ben_xml': ["Lectura masiva de XML", "Exportación a Excel", "Validación de metadatos"],

        'title_bank': "Conciliación Bancaria Inteligente",
        'desc_bank': "Automatizar el emparejamiento de transacciones entre el Extracto Bancario y el Libro Auxiliar de Bancos usando lógica difusa.",
        'ben_bank': ["Algoritmo de Fecha Flexible (+/- 3 días)", "Detecta partidas pendientes", "Ahorra 90% de tiempo manual"],

        'title_ugpp': "Escáner de Riesgo UGPP (Ley 1393)",
        'desc_ugpp': "Auditoría de Pagos Laborales. Verifica si los pagos NO salariales exceden el 40% del total de la remuneración (Art. 30 Ley 1393).",
        'ben_ugpp': ["Cálculo automático de exceso", "Alerta de riesgo alto", "Soporte para fiscalización"],

        'title_fiscal': "Auditoría Fiscal Masiva (Art. 771-5)",
        'desc_fiscal': "Verificar el cumplimiento de los requisitos de deducibilidad (Bancarización y Retenciones). Detecta pagos en efectivo superiores a 100 UVT y bases de retención omitidas.",
        'ben_fiscal': ["Detección de pagos en efectivo", "Validación de topes 100 UVT", "Prevención de rechazo de costos"],

        'title_payroll': "Calculadora de Costo Real de Nómina",
        'desc_payroll': "Ver el desglose exacto de cuánto le cuesta un empleado a la empresa. Incluye Salud, Pensión, ARL, Parafiscales, Primas, Cesantías, Intereses y Vacaciones.",
        'ben_payroll': ["Desglose parafiscal exacto", "Cálculo de provisiones", "Proyección anualizada"],
    },
    'English': {
        'menu_dash': "Home / Dashboard",
        'menu_dian': "Tax Audit (DIAN Cross-check)",
        'menu_xml': "XML Data Mining (Invoicing)",
        'menu_bank': "AI Bank Reconciliation",
        'menu_fiscal': "Fiscal Expense Audit",
        'menu_ugpp': "Payroll Scanner (UGPP)",
        'menu_treasury': "Treasury Projection",
        'menu_payroll': "Real Payroll Costing",
        'menu_fin_ai': "Smart Financial Analytics",
        'menu_narrator': "Financial Narrator & IFRS",
        'menu_rut': "Official RUT Validator",
        'menu_ocr': "OCR Digitization",

        'title_fiscal': "Massive Fiscal Audit (Art. 771-5)",
        'desc_fiscal': "Verify compliance with deductibility requirements (Bankization and Withholdings). Detects cash payments over 100 UVT.",
        'ben_fiscal': ["Cash payment detection", "100 UVT limit validation", "Cost rejection prevention"],

        # --- UI LABELS (Sidebar & Login) ---
        'lbl_operator': "OPERATOR:",
        'lbl_access': "ACCESS",
        'lbl_modules': "SYSTEM MODULES:",
        'lbl_logout': "TERMINATE SESSION",
        'lbl_unlock': "UNLOCK SYSTEM",
        'lbl_go_pro': "💎 GO PRO ($70k)",
        'lbl_go_prem': "🧠 GO PREMIUM ($120k)",
        'lbl_credits': "Credits:",

        'login_title': "Accounting Assistant <span style='color: var(--primary)'>PRO</span>",
        'login_subtitle': "v14.5 Enterprise Suite • Online System",
        'login_btn_google': "🔐 Sign in with Google",
        'login_error_config': "Google Auth configuration error.",
        'login_no_auth': "⚠️ GOOGLE AUTH UNAVAILABLE",
        'login_privacy_title': "Privacy & Security:",
        'login_privacy_desc': "Your data is processed in real-time and not stored permanently on our servers.",
        'login_manual_header': "⚠️ EMERGENCY ACCESS",
        'login_manual_help': "Use this channel if Google Auth fails (Error 403/500).",
        'login_input_id': "Operator ID",
        'login_input_pass': "Access Key",
        'login_btn_manual': "MANUAL LOGIN",
        'login_error_creds': "❌ INVALID CREDENTIALS",

        # Guide Content
        'title_treasury': "Liquidity Radar & Cash Flow",
        'desc_treasury': "Strategic treasury management to visualize future financial health by crossing Accounts Receivable (Projected Income) against Accounts Payable (Commitments) in real time.",
        'ben_treasury': ["Available balance projection", "Cash deficit alert", "Gap visualization"],

        'title_fin_ai': "Financial Intelligence (AI)",
        'desc_fin_ai': "Powerful analysis engine using AI to audit 100% of accounting movements, detecting anomalies, unusual spending patterns, and budget deviations.",
        'ben_fin_ai': ["Expense anomaly detection", "Automatic preventive audit", "Hidden pattern identification"],

        'title_narrator': "Financial Narrator & IFRS Notes",
        'desc_narrator': "Transforms complex numeric data into clear business narrative. Automates drafting of management reports and IFRS disclosures.",
        'ben_narrator': ["Auto-drafting of IFRS notes", "Instant management reports", "Qualitative interpretation"],

        'title_rut': "Official RUT Validator",
        'desc_rut': "Tax compliance tool verifying Tax ID (NIT) integrity using the official DIAN 'Module 11' algorithm.",
        'ben_rut': ["Verification Digit validation", "Exogenous error prevention", "Official DIAN algorithm"],

        'title_ocr': "Smart Digitization (OCR)",
        'desc_ocr': "Optical Character Recognition system extracting key info from physical invoices or images, eliminating manual entry.",
        'ben_ocr': ["Zero manual entry", "Massive invoice processing", "Time saving"],

        'title_dian': "Exogenous Auditor (DIAN Cross-check)",
        'desc_dian': "Detect discrepancies between your reports and DIAN's fiscal data. Matrix matching of Tax IDs to avoid inaccuracy penalties (Art. 651 ET).",
        'ben_dian': ["Avoid Art. 651 penalties", "Automatic Tax ID matching", "Detailed discrepancy report"],

        'title_xml': "XML Data Mining (Invoicing)",
        'desc_xml': "Extract structured information directly from Electronic Invoicing XML files validated by DIAN.",
        'ben_xml': ["Massive XML reading", "Export to Excel", "Metadata validation"],

        'title_bank': "Smart Bank Reconciliation",
        'desc_bank': "Automate transaction matching between Bank Statements and Ledger Books using fuzzy logic.",
        'ben_bank': ["Flexible Date Algorithm (+/- 3 days)", "Detects pending items", "Saves 90% of manual time"],

        'title_ugpp': "UGPP Risk Scanner (Law 1393)",
        'desc_ugpp': "Audit labor payments. Verifies if NON-salary payments exceed 40% of the total (Art. 30 Law 1393).",
        'ben_ugpp': ["Automatic excess calculation", "High risk alert", "Audit support"],

        'title_payroll': "Real Payroll Cost Calculator",
        'desc_payroll': "See the exact breakdown of how much an employee costs the company. Includes Health, Pension, ARL, Parafiscals, Bonuses, Severance, Interests, and Vacations.",
        'ben_payroll': ["Exact parafiscal breakdown", "Provision calculation", "Annualized projection"],
    }
}

def get_text(key):
    lang = st.session_state.get('lang', 'Español')
    return TRANSLATIONS.get(lang, TRANSLATIONS['Español']).get(key, key)

def render_module_guide(title, icon_url, description, benefits=None):
    """
    Renders a rich content 'Glass Card' with icon, title, description and benefits.
    Uses textwrap.dedent to prevent Markdown code block rendering issues.
    """
    if benefits is None: benefits = []

    # Generate benefits list HTML
    benefits_html = "".join([f"<li style='margin-bottom: 5px;'>{b}</li>" for b in benefits])

    # Construct the HTML structure
    html_content = f"""
    <div class="glass-card" style="padding: 24px; margin-bottom: 24px; border-left: 4px solid var(--primary);">
        <div style="display: flex; align-items: flex-start; margin-bottom: 16px;">
            <img src="{icon_url}" style="width: 48px; height: 48px; margin-right: 16px; opacity: 0.9; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.2));">
            <div>
                <h2 style="margin: 0 0 8px 0; font-size: 1.6rem; color: white;">{title}</h2>
                <p style="margin: 0; font-size: 1rem; color: #cbd5e1; line-height: 1.5;">{description}</p>
            </div>
        </div>
        <div style="background: rgba(99, 102, 241, 0.08); border-radius: 8px; padding: 16px;">
            <strong style="color: #818cf8; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px; display: block; margin-bottom: 8px;">KEY BENEFITS / BENEFICIOS CLAVE</strong>
            <ul style="margin: 0; padding-left: 20px; color: #94a3b8; font-size: 0.95rem;">
                {benefits_html}
            </ul>
        </div>
    </div>
    """

    # Dedent and render
    st.markdown(textwrap.dedent(html_content), unsafe_allow_html=True)

def render_smart_advisor(content):
    """
    Renders the AI Advisor response in a special glowing container.
    """
    html_content = f"""
    <div class="glass-card" style="padding: 24px; margin-top: 30px; border: 1px solid rgba(16, 185, 129, 0.3); background: linear-gradient(145deg, rgba(16, 185, 129, 0.05) 0%, rgba(2, 6, 23, 0.8) 100%);">
        <div style="display: flex; align-items: center; margin-bottom: 16px;">
            <span style="font-size: 1.5rem; margin-right: 12px;">🧠</span>
            <h3 style="margin: 0; color: #34d399;">Smart Advisor / Resumen Inteligente</h3>
        </div>
        <div style="color: #e2e8f0; font-size: 1rem; line-height: 1.6; font-family: 'Inter', sans-serif;">
            {content}
        </div>
    </div>
    """
    st.markdown(textwrap.dedent(html_content), unsafe_allow_html=True)


# ==============================================================================
# HELPER: UNIVERSAL DOWNLOADS (EXCEL + PDF)
# ==============================================================================
def create_pdf(df, title, filename):
    class PDF(FPDF):
        def header(self):
            # Logo placeholder or simple text
            self.set_font('Arial', 'B', 14)
            self.cell(0, 10, title[:50], 0, 1, 'C')
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, f"Generado por Asistente Contable Pro - {datetime.now().strftime('%Y-%m-%d %H:%M')}", 0, 1, 'C')
            self.ln(5)

    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 9)

    # Column Widths (Dynamic)
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
                txt = str(row[col])[:20] # Truncate for table safety
                # Evitar errores de latin-1 con emojis u otros caracteres especiales
                txt = txt.encode('latin-1', 'replace').decode('latin-1')
                pdf.cell(eff_width, 6, txt, 1, 0, 'L')
            pdf.ln()
    
    return pdf.output(dest='S').encode('latin-1')


def extract_md_table_to_df(text):
    import pandas as pd
    lines = text.split('\n')
    tables = []
    current_table = []
    for line in lines:
        if '|' in line and not line.strip().startswith('#'): # ignore headers that might have a pipe
            current_table.append(line.strip(' |'))
        else:
            if len(current_table) > 2:
                tables.append(current_table)
            current_table = []
    if len(current_table) > 2:
         tables.append(current_table)
         
    if not tables: return pd.DataFrame()
    
    # Process the first table found
    t = tables[0]
    headers = [x.strip() for x in t[0].split('|')]
    data = []
    for row in t[2:]:
        row_data = [x.strip() for x in row.split('|')]
        # Make sure row has same length as headers by padding or truncating
        if len(row_data) > len(headers): row_data = row_data[:len(headers)]
        while len(row_data) < len(headers): row_data.append("")
        data.append(row_data)
        
    try:
        return pd.DataFrame(data, columns=headers)
    except:
        return pd.DataFrame()

def download_section(df, file_label, title="Reporte Corporativo"):
    """
    Renders two buttons: Download Excel and Download PDF.
    """
    st.markdown("### 📥 Descargar Resultados")
    c1, c2 = st.columns(2)
    
    # EXCEL
    buffer_xls = io.BytesIO()
    with pd.ExcelWriter(buffer_xls, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Reporte')
    
    c1.download_button(
        label="📊 Descargar Excel (.xlsx)",
        data=buffer_xls.getvalue(),
        file_name=f"{file_label}.xlsx",
        mime="application/vnd.ms-excel",
        use_container_width=True
    )

    # PDF
    try:
        pdf_bytes = create_pdf(df, title, file_label)
        c2.download_button(
            label="📄 Descargar PDF (.pdf)",
            data=pdf_bytes,
            file_name=f"{file_label}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    except Exception as e:
        c2.warning(f"PDF no disponible: {e}")

def render_upload_example(data_dict, title="👉 IMPORTANTE: ¿Qué archivo debo subir?", help_text=""):
    """
    Shows optional help text to guide file uploads. Rigid examples are removed since AI is flexible.
    """
    if help_text:
        st.info(help_text)
    st.caption("✨ Sube tu archivo con la estructura que tengas. La Inteligencia Artificial se encargará de procesarlo automáticamente.")

# ==============================================================================
# 2. GESTIÓN DE CONEXIONES EXTERNAS (BACKEND) Y SEGURIDAD (OAUTH2)
# ==============================================================================

# ------------------------------------------------------------------------------
# UI DE AUTO-DIAGNÓSTICO (DEFENSA EN PROFUNDIDAD)
# ------------------------------------------------------------------------------
def render_panic_ui(e):
    """
    Renderiza una interfaz amigable cuando ocurre un error técnico.
    Ofrece la opción de usar IA para explicar el problema en lenguaje sencillo.
    """
    st.toast("⚠️ Problema detectado con el archivo", icon="🤧")
    
    # 1. Contenedor Visual de Error (Glassmorphism Red)
    st.markdown(f"""
    <div style="
        background: rgba(220, 38, 38, 0.1); 
        border-left: 4px solid #ef4444;
        padding: 16px;
        border-radius: 8px;
        margin: 10px 0;
        backdrop-filter: blur(5px);
    ">
        <h4 style="margin: 0; color: #fca5a5; display: flex; align-items: center;">
            <span style="font-size: 1.5rem; margin-right: 10px;">🛡️</span> 
            Sistema de Auto-Defensa Activado
        </h4>
        <p style="margin: 8px 0 0 0; color: #e2e8f0; font-size: 0.95rem;">
            No pudimos procesar tu archivo correctamente. El sistema ha interceptado el error para proteger tus datos.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 2. Botón de Pánico (Acción IA)
    # Usamos un key único basado en el timestamp o algo aleatorio si fuera necesario, 
    # pero aquí confiamos en el flujo inmediato.
    if st.button("🆘 ¿Por qué falló? Explicar con IA", key="btn_panic_ai", type="primary"):
        if 'api_key_valida' in globals() and api_key_valida: # Check global availability
             with st.spinner("🔍 Analizando estructura del archivo y el error..."):
                prompt_soporte = f"""
                ACTÚA COMO: Agente de Soporte Técnico Experto (Nivel 2) para la App 'Asistente Contable'.
                
                SITUACIÓN: El usuario intentó subir un archivo y falló.
                ERROR TÉCNICO REGISTRADO: "{str(e)}"
                
                TU TAREA:
                1.  Explica en ESPAÑOL SENCILLO y AMIGABLE qué pudo haber pasado.
                2.  Usa analogías si es necesario (ej: "Es como intentar meter una pieza cuadrada en un agujero redondo").
                3.  NO MENCIONES código Python, Tracebacks ni clases (ValueError, TypeError).
                4.  Da 3 pasos accionables para que el usuario arregle su Excel.
                
                FORMATO DE RESPUESTA: Markdown limpio con bullets.
                """
                # Llamada directa a la función de IA (que ya maneja créditos)
                response = consultar_ia_gemini(prompt_soporte)
                
                st.markdown(f"""
                <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid #10b981; padding: 20px; border-radius: 12px; margin-top: 15px;">
                    <h3 style="color: #34d399; margin-top: 0;">🤖 Diagnóstico Inteligente</h3>
                    <div style="color: #e2e8f0; line-height: 1.6;">{response}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.error("Servicio de IA no disponible para diagnóstico.")
    
    with st.expander("Ver detalle técnico (Para desarrolladores)"):
        st.code(str(e), language="python")

# ------------------------------------------------------------------------------
# SANITIZACIÓN INTELIGENTE DE DATOS (DATA INTELLIGENCE LAYER)
# ------------------------------------------------------------------------------

PLAN_LIMITS = {
    "Gratis": 2 * 1024 * 1024,   # 2MB
    "Pro": 10 * 1024 * 1024,     # 10MB
    "Premium": 50 * 1024 * 1024  # 50MB
}

def safe_read_excel(file_upl):
    """
    Lee archivos Excel/CSV con validación de Plan (Fair Use) y limpieza automática.
    """
    try:
        # DETERMINAR PLAN REAL DEL USUARIO DESDE LA SESIÓN
        raw_plan = st.session_state.get('user_plan', 'FREE').upper()
        plan_mapping = {"FREE": "Gratis", "PRO": "Pro", "PREMIUM": "Premium"}
        user_plan = plan_mapping.get(raw_plan, "Gratis")
        
        limit = PLAN_LIMITS.get(user_plan, 2 * 1024 * 1024) # Default 2MB
        
        # 1. Validación de PESO (Fair Use)
        if file_upl.size > limit:
            limit_mb = int(limit / (1024 * 1024))
            st.error(f"⚠️ **Archivo Bloqueado**: Tu plan actual ({user_plan}) solo permite subir archivos de hasta {limit_mb} MB.")
            st.info("💡 Sube al plan Pro o Premium para desbloquear archivos grandes.")
            return pd.DataFrame()

        # 2. Carga cruda del archivo
        if file_upl.name.endswith('.csv'):
             df = pd.read_csv(file_upl)
        else:
             df = pd.read_excel(file_upl)
        
        # 3. Inteligencia de Datos: Sanitización Automática
        for col in df.columns:
            if df[col].dtype == 'object': 
                # A. Limpieza Agresiva
                clean_col = df[col].astype(str).str.replace(r'[$,\s]|COP|USD|EUR', '', regex=True)
                # B. Intentar conversión
                converted = pd.to_numeric(clean_col, errors='coerce')
                # C. Decisión Inteligente
                valid_count = converted.notna().sum()
                total_count = df[col].notna().sum()
                
                if total_count > 0 and (valid_count / total_count) > 0.5:
                    df[col] = converted.fillna(0) 
                    
        return df
    except Exception as e:
        # CAPTURA SILENCIOSA Y DELEGACIÓN A UI DE PÁNICO
        st.session_state['last_error'] = str(e)
        render_panic_ui(e)
        return pd.DataFrame()

# ------------------------------------------------------------------------------
# A. AUTENTICACIÓN GOOGLE OAUTH2 (THE GATEKEEPER)
# ------------------------------------------------------------------------------

def login_section():
    # Load secrets safely
    try:
        google_secrets_ok = "google" in st.secrets
    except Exception:
        google_secrets_ok = False

    auth_url = None

    # --- UI RENDER (Header + Background) ---
    # Centering container with flexbox for vertical and horizontal alignment
    st.markdown(f"""
<div style="
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 40vh;
    width: 100%;
    margin-top: 5vh;
    position: relative;
    z-index: 10;
">
    <div style="text-align: center;">
        <h1 style="font-family: 'Inter', sans-serif; font-size: 3rem; font-weight: 800; margin-bottom: 0.5rem; letter-spacing: -1px;">{get_text('login_title')}</h1>
        <p style="color: var(--text-body); font-family: 'Inter', sans-serif; font-size: 1.2rem; font-weight: 500;">{get_text('login_subtitle')}</p>
    </div>
</div>
""", unsafe_allow_html=True)

    # --- GOOGLE AUTH LOGIC (STREAMLIT-OAUTH) ---
    if google_secrets_ok and OAUTH_OK:
        try:
            oauth2 = OAuth2Component(
                client_id=st.secrets["google"]["client_id"],
                client_secret=st.secrets["google"]["client_secret"],
                authorize_endpoint="https://accounts.google.com/o/oauth2/v2/auth",
                token_endpoint="https://oauth2.googleapis.com/token",
                refresh_token_endpoint="https://oauth2.googleapis.com/token",
                revoke_token_endpoint="https://oauth2.googleapis.com/revoke",
            )

            # --- CENTRADO DEL BOTÓN (MODO LIMPIO) ---
            # Usamos columnas equilibradas [1, 1, 1] para que el botón no se deforme
            left_col, center_col, right_col = st.columns([1, 1, 1])

            with center_col:
                result = oauth2.authorize_button(
                    name=get_text('login_btn_google'),
                    icon="https://www.google.com.tw/favicon.ico",
                    redirect_uri=st.secrets["google"]["redirect_uri"],
                    scope="openid email profile",
                    key="google_auth",
                    extras_params={"prompt": "consent", "access_type": "offline"}
                )

            if result:
                # Decode access token or fetch user info
                try:
                    access_token = result.get("access_token") or result.get("token", {}).get("access_token")
                    if access_token:
                        # Fetch User Info manually to be safe
                        user_info = requests.get(
                            "https://www.googleapis.com/oauth2/v1/userinfo",
                            headers={"Authorization": f"Bearer {access_token}"}
                        ).json()

                        email = user_info.get('email')

                        st.session_state['logged_in'] = True
                        st.session_state['user_info'] = user_info
                        st.session_state['username'] = user_info.get('name')
                        st.session_state['user_email'] = email
                        st.session_state['user_picture'] = user_info.get('picture')

                        # --- SESSION ENFORCEMENT & CREDIT INIT ---
                        new_token = update_session_token(email)
                        st.session_state['session_token'] = new_token
                        st.session_state['credits_used'] = get_user_credits(email)

                        # Default Plan (Can be upgraded in DB later, defaulting to FREE/PRO for logic)
                        # For now, we default to FREE unless admin
                        st.session_state['user_plan'] = 'FREE'
                        if email == 'admin@internal.system': st.session_state['user_plan'] = 'PREMIUM'

                        st.rerun()
                except Exception as e:
                    st.error(f"Error procesando login: {e}")

        except Exception as e:
            st.warning(get_text('login_error_config'))
    else:
         st.markdown(f'<div style="text-align:center; color:#ef4444; border:1px solid #ef4444; padding:10px; border-radius: 8px; margin: 20px auto; max-width: 400px;">{get_text("login_no_auth")}</div>', unsafe_allow_html=True)

    st.markdown(f"""
<div style="display: flex; flex-direction: column; align-items: center; justify-content: center; position: relative; z-index: 10;">
    <div style="max-width: 400px; text-align: center; color: #64748b; font-size: 0.8rem; margin-top: 2rem; padding: 1rem; border-top: 1px solid rgba(255,255,255,0.1);">
        🔒 <strong>{get_text('login_privacy_title')}</strong><br>
        {get_text('login_privacy_desc')}
    </div>
</div>
""", unsafe_allow_html=True)

    # --- FALLBACK LOGIN (Manual Override) ---
    c1, c2, c3 = st.columns([1,1,1])
    with c2:
        with st.expander(get_text('login_manual_header')):
            st.markdown(f"<small style='color: #94a3b8;'>{get_text('login_manual_help')}</small>", unsafe_allow_html=True)
            u = st.text_input(get_text('login_input_id'), key="login_u")
            p = st.text_input(get_text('login_input_pass'), type="password", key="login_p")

            if st.button(get_text('login_btn_manual'), type="primary"):
                if u == "admin" and p == "admin":
                    st.session_state['user_plan'] = 'PREMIUM'
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = 'Admin (Manual)'
                    st.session_state['user_email'] = 'admin@internal.system'
                    st.session_state['user_picture'] = ''

                    # Session Token & Credits
                    st.session_state['session_token'] = update_session_token('admin@internal.system')
                    st.session_state['credits_used'] = 0

                    registrar_log("Admin", "Login Manual", "Acceso de emergencia usado")
                    st.rerun()
                elif u == "cliente" and p == "cliente":
                    st.session_state['user_plan'] = 'FREE'
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = 'Cliente (Manual)'
                    st.session_state['user_email'] = 'client@internal.system'
                    st.session_state['user_picture'] = ''

                    # Session Token & Credits
                    st.session_state['session_token'] = update_session_token('client@internal.system')
                    st.session_state['credits_used'] = get_user_credits('client@internal.system')

                    registrar_log("Cliente", "Login Manual", "Acceso cliente manual")
                    st.rerun()
                else:
                    st.error(get_text('login_error_creds'))
                    registrar_log(u, "Login Fallido", "Manual override fallido")

    st.stop()

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
    Función de Auditoría ASÍNCRONA (NON-BLOCKING):
    Usa hilos para guardar en Google Sheets sin congelar la pantalla del usuario.
    Ideal para alta concurrencia (50-100 usuarios).
    """
    if db_conectada and sheet_logs:
        def _write_background():
            try:
                fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                sheet_logs.append_row([fecha_hora, usuario, accion, detalle])
            except:
                pass
        # Ejecutar en segundo plano
        threading.Thread(target=_write_background).start() 

# --- SIDEBAR: LANGUAGE SELECTOR (Global Access) ---
# Sidebar logic moved to top of file

# --- CHECK LOGIN STATUS (Moved after registrar_log definition) ---
if not st.session_state.get('logged_in', False):
    login_section()

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

# CONSTANTES FISCALES COLOMBIA (AÑO GRAVABLE 2026)
SMMLV_2026 = 1750905
AUX_TRANS_2026 = 249095
UVT_2026 = 52374
TOPE_EFECTIVO = 100 * UVT_2026
BASE_RET_SERVICIOS = 4 * UVT_2026
BASE_RET_COMPRAS = 27 * UVT_2026

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
    # Extracción segura de valores con manejo de errores
    try:
        raw_val = str(row[col_valor]) if pd.notnull(row[col_valor]) else "0"
        # Limpieza: eliminar símbolos de moneda, espacios y comas (asumiendo miles)
        clean_val = raw_val.replace('$', '').replace(' ', '').replace(',', '')
        valor = float(clean_val)
    except (ValueError, TypeError):
        valor = 0.0
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
    aux_trans = AUX_TRANS_2026 if tiene_aux else 0
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
    Usa el modelo definido por el plan del usuario.
    Incluye lógica de consumo de créditos.
    """
    plan = st.session_state.get('user_plan', 'FREE')
    config = PLAN_CONFIG.get(plan, PLAN_CONFIG['FREE'])
    credits = st.session_state.get('credits_used', 0)
    email = st.session_state.get('user_email')

    if credits >= config['limit']:
        return "⚠️ HAS ALCANZADO EL LÍMITE DE CRÉDITOS DE TU PLAN. Por favor, actualiza a PRO o PREMIUM para continuar."

    try:
        # Selección Dinámica de Modelo
        model_name = config['model']
        # Fallback manual si el nombre del plan no coincide con la API (ej. 'gemini-1.5-flash' vs 'models/gemini-1.5-flash')
        # Ajustamos a las versiones estables conocidas si es necesario, o confiamos en el config.
        # Para seguridad, usamos try/catch con fallbacks

        # RETRY LOGIC / FALLBACK AUTOMÁTICO
        intentos = [model_name, 'gemini-1.5-flash', 'gemini-2.5-flash', 'gemini-2.0-flash']
        last_error = ""

        for m in intentos:
            try:
                model = genai.GenerativeModel(m)
                response = model.generate_content(prompt)
                
                # Si llegamos aquí, funcionó
                consume_credit(email)
                st.session_state['credits_used'] = credits + 1
                return response.text
                
            except Exception as e:
                last_error = str(e)
                continue # Intenta el siguiente modelo

        return f"Error IA [v2] (Todos los modelos fallaron): {last_error}"
    except Exception as e:
        return f"Error Crítico IA [v2]: {str(e)}"

# ------------------------------------------------------------------------------
# OCR DE FACTURAS (VELOCIDAD)
# ------------------------------------------------------------------------------
def ocr_factura(imagen):
    """
    OCR consume 1 crédito. Usa Flash para velocidad en todos los planes (o según config).
    """
    plan = st.session_state.get('user_plan', 'FREE')
    config = PLAN_CONFIG.get(plan, PLAN_CONFIG['FREE'])
    credits = st.session_state.get('credits_used', 0)
    email = st.session_state.get('user_email')

    if credits >= config['limit']:
        st.error("⚠️ Límite de créditos alcanzado.")
        return None

    try:
        # OCR siempre usa Flash por velocidad, a menos que se especifique otra cosa.
        # Usamos 'gemini-1.5-flash' explicitamente o el del plan si es compatible.
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = """Extrae datos JSON estricto: {"fecha": "YYYY-MM-DD", "nit": "num", "proveedor": "txt", "concepto": "txt", "base": num, "iva": num, "total": num}"""
        response = model.generate_content([prompt, imagen])

        # Consumir crédito
        consume_credit(email)
        st.session_state['credits_used'] = credits + 1

        return json.loads(response.text.replace("```json", "").replace("```", "").strip())
    except Exception as e:
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

# --- CONFIGURACIÓN DE ESTILO GLOBAL (SIDEBAR CLÁSICO MEJORADO) ---
st.markdown("""
    <style>
        /* 1. ASEGURAR QUE LA BARRA SE VEA */
        [data-testid="stSidebar"] {
            display: block !important;
            z-index: 999998 !important;
            background-color: #020617 !important; /* Fondo oscuro sólido */
            border-right: 1px solid rgba(255, 255, 255, 0.1);
        }

        /* El botón de menú lateral se dejará nativo para evitar conflictos con Streamlit Cloud */

        /* 3. ESTILOS GENERALES (FONDO Y FUENTES) */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=Manrope:wght@400;600;800&display=swap');
        
        .stApp {
            background: radial-gradient(circle at top right, #1e293b, transparent 40%),
                        radial-gradient(circle at bottom left, #1e1b4b, transparent 40%),
                        linear-gradient(180deg, #0f172a 0%, #020617 100%) !important;
            background-attachment: fixed !important;
            font-family: 'Inter', sans-serif;
            color: #94a3b8;
        }
        
        h1, h2, h3 { color: white !important; font-family: 'Inter', sans-serif !important; }
        #MainMenu {visibility: hidden;} 
        footer {visibility: hidden;} 
        /* Estilo para las tarjetas */
        .glass-card, div[data-testid="stExpander"] {
            background: rgba(30, 41, 59, 0.7) !important;
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255,255,255,0.08) !important;
            border-radius: 12px;
        }
    </style>
""", unsafe_allow_html=True)
# ==============================================================================
# ==============================================================================
# 6. CONTENIDO PRINCIPAL (DASHBOARD Y MÓDULOS)
# ==============================================================================
# ==============================================================================

def render_quienes_somos():
    st.markdown("""
    <style>
        .qs-hero {
            background: linear-gradient(135deg, rgba(30,41,59,0.9), rgba(15,23,42,0.95));
            border-radius: 15px;
            padding: 40px;
            margin-bottom: 30px;
            border: 1px solid rgba(255,255,255,0.1);
            text-align: center;
        }
        .qs-title {
            font-size: 2.5rem;
            font-weight: 800;
            background: -webkit-linear-gradient(45deg, #38bdf8, #818cf8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }
        .qs-subtitle {
            color: #94a3b8;
            font-size: 1.2rem;
            margin-bottom: 0;
        }
        .qs-card {
            background: rgba(30,41,59,0.5);
            backdrop-filter: blur(10px);
            border-radius: 12px;
            padding: 25px;
            border: 1px solid rgba(255,255,255,0.05);
            height: 100%;
        }
        .qs-card h3 {
            color: #f8fafc;
            border-bottom: 2px solid #3b82f6;
            padding-bottom: 10px;
            margin-bottom: 15px;
        }
        .qs-card p {
            color: #cbd5e1;
            line-height: 1.7;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="qs-hero">
        <h1 class="qs-title">KINETIK IA</h1>
        <p class="qs-subtitle">El Futuro de la Contabilidad, Hoy.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="qs-card">
            <h3>🏢 Nuestra Empresa</h3>
            <p>En <b>KINETIK IA</b>, desarrollamos tecnología de vanguardia para transformar la forma en que los profesionales financieros y contables operan en Colombia. Nuestra misión es automatizar las tareas repetitivas y blindar a las empresas frente a los entes de control (DIAN, UGPP) mediante el uso estratégico de Inteligencia Artificial.</p>
            <p>Creemos en una contabilidad proactiva, analítica y sin errores humanos, elevando el valor del Contador Público hacia un rol de consultor estratégico.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="qs-card">
            <h3>👨‍💻 Nuestro Creador</h3>
            <p>Fundada y desarrollada por <b>Omar Hernández</b>, un visionario apasionado por la intersección entre las finanzas corporativas y la tecnología disruptiva.</p>
            <p>Inspirado por la complejidad del sistema tributario colombiano, Omar creó <b>Asistente Contable PRO</b> para democratizar el acceso a herramientas de auditoría y análisis de datos de clase mundial, permitiendo que cualquier pyme o contador independiente pueda operar con la eficiencia de una gran corporación.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="qs-card" style="margin-top: 10px;">
        <h3>🚀 Nuestros Servicios Principales</h3>
        <ul style="color: #cbd5e1; line-height: 1.8; font-size: 1.05rem;">
            <li><b>Auditoría Fiscal e Inteligencia Artificial:</b> Motores de cruce masivo para XML de facturación electrónica y reportes exógenos.</li>
            <li><b>Análisis de Riesgo UGPP:</b> Escáner paramétrico avanzado de nómina y costos reales basados en la Ley 1393.</li>
            <li><b>Copiloto Tributario 24/7:</b> Asistente IA interactivo entrenado permanentemente con el Estatuto Tributario y conceptos de la DIAN.</li>
            <li><b>Automatización Documental:</b> Digitalización OCR y conciliaciones bancarias potenciadas por algoritmos predictivos.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

if menu == "Inicio / Dashboard":
    # 1. HEADER EJECUTIVO (HERO SECTION - ENTERPRISE TRUST)
    st.markdown("""
    <div class="hero-wrapper">
        <div class="glow-orb orb-1"></div>
        <div class="glow-orb orb-2"></div>
        <div class="hero-card">
            <div class="hero-badge">
                <span class="pulse-dot"></span> SISTEMA EN LÍNEA ACTIVO
            </div>
            <h1 class="hero-title-mega">Asistente Contable <span class="text-gradient">PRO</span></h1>
            <p class="hero-desc">Inteligencia Artificial Financiera v14.5 • Suite Empresarial</p>
        </div>
    </div>
    <style>
        .hero-wrapper {
            position: relative;
            margin-bottom: 2.5rem;
            padding: 1rem 0;
            overflow: hidden;
            border-radius: 20px;
        }
        .glow-orb {
            position: absolute;
            border-radius: 50%;
            filter: blur(45px);
            opacity: 0.6;
            animation: float 6s ease-in-out infinite;
            z-index: 0;
        }
        .orb-1 {
            width: 180px;
            height: 180px;
            background: rgba(99, 102, 241, 0.8);
            top: -30px;
            left: 10%;
        }
        .orb-2 {
            width: 220px;
            height: 220px;
            background: rgba(16, 185, 129, 0.5);
            bottom: -50px;
            right: 10%;
            animation-delay: -3s;
        }
        @keyframes float {
            0%, 100% { transform: translateY(0) scale(1); }
            50% { transform: translateY(-20px) scale(1.1); }
        }
        .hero-card {
            position: relative;
            z-index: 1;
            background: rgba(20, 24, 39, 0.6);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 20px;
            padding: 4rem 2rem;
            text-align: center;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.4s ease;
        }
        .hero-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 35px 60px -15px rgba(99, 102, 241, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.15);
        }
        .hero-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(16, 185, 129, 0.1);
            color: #10b981;
            padding: 6px 16px;
            border-radius: 50px;
            font-size: 0.8rem;
            font-weight: 700;
            letter-spacing: 1px;
            margin-bottom: 1.8rem;
            border: 1px solid rgba(16, 185, 129, 0.25);
        }
        .pulse-dot {
            width: 8px;
            height: 8px;
            background-color: #10b981;
            border-radius: 50%;
            box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
            70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }
            100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
        }
        .hero-title-mega {
            font-family: 'Inter', sans-serif !important;
            font-size: 3.8rem !important;
            font-weight: 900 !important;
            margin: 0 0 1rem 0;
            letter-spacing: -2px;
            color: #ffffff;
            line-height: 1.1;
        }
        .text-gradient {
            background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #ec4899 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-size: 200% auto;
            animation: shine 4s linear infinite;
        }
        @keyframes shine {
            to { background-position: 200% center; }
        }
        .hero-desc {
            font-size: 1.25rem;
            color: #94a3b8;
            font-weight: 400;
            margin: 0 auto;
            max-width: 600px;
        }
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
            .hero-title-mega { font-size: 2.5rem !important; }
            .hero-card { padding: 2.5rem 1.5rem; }
            .hero-desc { font-size: 1rem; }
        }
    </style>
    """, unsafe_allow_html=True)

    # Los atajos (Quick Actions) falsos y el Ticker falso fueron eliminados.
    # El usuario ahora navegará 100% mediante el menú lateral que sí es funcional.

    # 2. NUEVO DASHBOARD: QUIÉNES SOMOS, NOTICIAS E HISTORIAL

    @st.cache_data(ttl=86400) # Cache por 24 horas para no agotar cuota y cargar rápido
    def get_daily_ai_content():
        try:
            import google.generativeai as genai
            # Usar un modelo rápido y estable
            model = genai.GenerativeModel('gemini-1.5-flash')
            noticia = model.generate_content("Escribe un párrafo muy corto (máximo 4 líneas) con una noticia tributaria o contable importante para Colombia en 2026. Sé profesional.").text
            chiste = model.generate_content("Escribe un chiste corto y amigable sobre contadores, auditores o impuestos para sacar una sonrisa al usuario que está trabajando. Corto y sin explicaciones.").text
            return noticia, chiste
        except Exception:
            return "Las tasas de usura y retención en la fuente se mantienen estables para este mes. Verifica las actualizaciones de la DIAN.", "¡Un contador no envejece, solo se deprecia! Tómate 5 minutos para estirarte y tomar agua."

    noticia_dia, chiste_dia = get_daily_ai_content()

    st.markdown("### 🌟 BIENVENIDO A ASISTENTE CONTABLE PRO")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### 🎯 ¿En qué te podemos ayudar?")
        st.markdown("""
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin-bottom: 2rem;">
            <div class="glass-card" style="padding: 20px; border-left: 4px solid #6366f1;">
                <h4 style="margin:0; color: #a5b4fc;">📄 Digitalización OCR</h4>
                <p style="font-size: 0.9rem; color: #cbd5e1; margin-top: 10px;">Extrae datos de facturas y recibos físicos al instante con inteligencia artificial.</p>
            </div>
            <div class="glass-card" style="padding: 20px; border-left: 4px solid #10b981;">
                <h4 style="margin:0; color: #6ee7b7;">💰 Costeo de Nómina</h4>
                <p style="font-size: 0.9rem; color: #cbd5e1; margin-top: 10px;">Calcula el costo real de tus empleados incluyendo parafiscales y provisiones 2026.</p>
            </div>
            <div class="glass-card" style="padding: 20px; border-left: 4px solid #f43f5e;">
                <h4 style="margin:0; color: #fda4af;">🔍 Auditoría Fiscal</h4>
                <p style="font-size: 0.9rem; color: #cbd5e1; margin-top: 10px;">Detecta inconsistencias en reportes de la DIAN automáticamente.</p>
            </div>
            <div class="glass-card" style="padding: 20px; border-left: 4px solid #f59e0b;">
                <h4 style="margin:0; color: #fcd34d;">🤖 Copiloto Tributario</h4>
                <p style="font-size: 0.9rem; color: #cbd5e1; margin-top: 10px;">Resuelve tus dudas fiscales 24/7 en el menú interactivo lateral.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### 🕒 Tu Historial de Actividad Reciente")
        # Leer historial real desde Firestore
        email = st.session_state.get('user_email')
        if not email or not st.session_state.get('logged_in'):
            st.markdown("""
            <div class="glass-card" style="padding: 20px; text-align: center; color: #94a3b8;">
                <p>Inicia sesión para ver tu historial de actividad real.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            history = get_user_history(email, limit=4)
            if not history:
                st.markdown("""
                <div class="glass-card" style="padding: 20px; text-align: center; color: #94a3b8;">
                    <p>Aún no tienes actividad registrada.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                import datetime
                html_list = '<div class="glass-card" style="padding: 20px;"><ul style="list-style-type: none; padding-left: 0; color: #cbd5e1; font-size: 0.95rem; margin: 0;">'
                colors = ['🟢', '🔵', '🟣', '⚪']
                
                for i, item in enumerate(history):
                    action = item.get('action', 'Acción')
                    timestamp = item.get('timestamp')
                    time_str = "Recientemente"
                    if timestamp:
                        try:
                            # Dependiendo del tipo de objeto devuelto por Firestore
                            if hasattr(timestamp, 'timestamp'):
                                dt = datetime.datetime.fromtimestamp(timestamp.timestamp())
                            else:
                                dt = timestamp
                            time_str = dt.strftime('%d/%m/%Y %H:%M')
                        except: pass
                        
                    color = colors[i % len(colors)]
                    border = 'border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 10px;' if i < len(history)-1 else 'margin-bottom: 0;'
                    html_list += f'<li style="margin-bottom: 15px; {border}">{color} <b>{time_str}</b> - {action}</li>'
                    
                html_list += '</ul></div>'
                st.markdown(html_list, unsafe_allow_html=True)

    with col2:
        st.markdown("#### 📰 Noticia del Día (IA)")
        st.markdown(f"""
        <div class="glass-card" style="padding: 20px; border-top: 4px solid #3b82f6; margin-bottom: 20px; background: linear-gradient(180deg, rgba(59, 130, 246, 0.1) 0%, rgba(0,0,0,0) 100%);">
            <p style="color: #e2e8f0; font-size: 0.95rem; line-height: 1.5; margin:0;">{noticia_dia}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### ☕ Pausa Activa")
        st.markdown(f"""
        <div class="glass-card" style="padding: 20px; border-top: 4px solid #8b5cf6; background: linear-gradient(180deg, rgba(139, 92, 246, 0.1) 0%, rgba(0,0,0,0) 100%);">
            <p style="color: #e2e8f0; font-size: 0.95rem; font-style: italic; margin:0;">"{chiste_dia}"</p>
        </div>
        """, unsafe_allow_html=True)
        


    # 3. SECCIÓN PLANES Y PRECIOS
    st.markdown("---")
    st.markdown("### 💎 MEJORAR NIVEL DE ACCESO")
    
    st.markdown("""
    <style>
        .pricing-card {
            background: var(--glass-bg);
            backdrop-filter: blur(12px);
            border: 1px solid var(--glass-border);
            border-radius: 12px;
            padding: 2rem;
            height: 100%;
            display: flex; flex-direction: column;
            transition: all 0.3s ease;
            box-shadow: var(--shadow-soft);
        }
        .pricing-card:hover { transform: translateY(-5px); border-color: var(--primary); box-shadow: 0 8px 30px rgba(99, 102, 241, 0.2); }
        .pricing-card.pro {
            background: linear-gradient(145deg, rgba(15, 23, 42, 0.9) 0%, rgba(99, 102, 241, 0.1) 100%);
            border: 1px solid var(--primary);
            box-shadow: 0 0 30px rgba(99, 102, 241, 0.15);
            position: relative;
        }
        .pricing-card.premium {
            background: linear-gradient(145deg, rgba(15, 23, 42, 0.9) 0%, rgba(139, 92, 246, 0.2) 100%);
            border: 1px solid #c084fc;
            box-shadow: 0 0 40px rgba(192, 132, 252, 0.2);
            position: relative;
        }
        .popular-badge {
            position: absolute; top: -12px; right: 24px;
            background: linear-gradient(90deg, #6366f1, #8b5cf6);
            color: white; padding: 4px 12px; border-radius: 99px;
            font-size: 0.75rem; font-weight: 700; letter-spacing: 0.5px; font-family: 'Inter';
        }
        .price-tag { font-family: 'Inter'; font-size: 2.5rem; font-weight: 800; color: white; margin: 10px 0; letter-spacing: -1px; }
        .price-tag span { font-size: 0.9rem; color: var(--text-body); font-weight: 500; }
        .price-old { font-size: 1rem; color: #64748b; text-decoration: line-through; margin-top: 10px; }
        .features-ul { list-style: none; padding: 0; margin: 20px 0; color: var(--text-body); flex-grow: 1; font-size: 0.9rem; }
        .features-ul li { margin-bottom: 10px; display: flex; align-items: center; }
        .check { color: var(--success); margin-right: 8px; font-weight: bold; }
        .cross { color: #ef4444; margin-right: 8px; opacity: 0.7; }
    </style>
    """, unsafe_allow_html=True)

    col_free, col_pro, col_prem = st.columns(3)

    # PLAN INICIAL
    with col_free:
        st.markdown("""
        <div class="pricing-card">
            <h3 style="color:#94a3b8; margin:0; font-size: 1.2rem;"> NIVEL INICIAL</h3>
            <div class="price-tag">$0 <span>COP/mes</span></div>
            <ul class="features-ul">
                <li><span class="check">✓</span> Acceso al Dashboard</li>
                <li><span class="check">✓</span> 5 Consultas IA/día</li>
                <li><span class="check">✓</span> Archivos hasta 2 MB</li>
                <li class="dimmed"><span class="cross">✕</span> Agente Tributario</li>
                <li class="dimmed"><span class="cross">✕</span> Conexión Bancaria</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        st.button("PLAN ACTUAL", disabled=True, use_container_width=True)

    # PLAN PRO
    with col_pro:
        st.markdown("""
        <div class="pricing-card pro">
            <h3 style="color:#6366f1; margin:0; font-size: 1.2rem;"> PLAN PRO</h3>
            <div class="price-old">$100.000</div>
            <div class="price-tag">$70.000 <span>COP/mes</span></div>
            <ul class="features-ul">
                <li><span class="check">✓</span> 500 Créditos Mensuales</li>
                <li><span class="check">✓</span> Modelo Gemini 1.5 Flash</li>
                <li><span class="check">✓</span> Archivos hasta 10 MB</li>
                <li><span class="check">✓</span> Soporte Prioritario</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        st.link_button("⚡ MEJORAR A PRO", "https://checkout.wompi.co/l/TU_LINK_PRO", type="primary", use_container_width=True)

    # PLAN PREMIUM
    with col_prem:
        st.markdown("""
        <div class="pricing-card premium">
            <div class="popular-badge">RECOMENDADO</div>
            <h3 style="color:#c084fc; margin:0; font-size: 1.2rem;"> PLAN PREMIUM</h3>
            <div class="price-old">$180.000</div>
            <div class="price-tag">$120.000 <span>COP/mes</span></div>
            <ul class="features-ul">
                <li><span class="check">✓</span> <strong>Ilimitado + Agentic IA</strong></li>
                <li><span class="check">✓</span> Modelo Gemini 1.5 PRO</li>
                <li><span class="check">✓</span> Archivos hasta 50 MB (Massive)</li>
                <li><span class="check">✓</span> Auditoría NIIF Avanzada</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        st.link_button("🚀 OBTENER BLINDAJE TOTAL", "https://checkout.wompi.co/l/TU_LINK_PREMIUM", type="primary", use_container_width=True)

    if not db_conectada:
        st.warning("⚠️ BASE DE DATOS OFFLINE. Verifique conexión a 'DB_Alcontador'.")

# ---------------------------------------------------------
# ELSE: CAMBIO DE MENÚ (ESTE SÍ TOCA EL BORDE IZQUIERDO)
# ---------------------------------------------------------
else:
    # 1. AUDITORÍA
    if menu == "🏢 Quiénes Somos / Historia":
        render_quienes_somos()

    elif menu == "Auditoría Cruce DIAN":
        render_module_guide(
            get_text('title_dian'),
            "https://cdn-icons-png.flaticon.com/512/921/921591.png",
            get_text('desc_dian'),
            get_text('ben_dian')
        )
        
        col_dian, col_conta = st.columns(2)
        with col_dian:
            st.subheader("🏛️ 1. Archivo DIAN")
            file_dian = st.file_uploader("Subir 'Reporte Terceros DIAN' (.xlsx)", type=['xlsx'])
            render_upload_example({'NIT': ['900123456', '890987654'], 'Valor Reportado': ['$ 1,500,000.00', '$ 5,200,000 COP']}, help_text="Sube el reporte de terceros generado por la DIAN. Ahora no requieres columnas estrictas.")

        with col_conta:
            st.subheader("📒 2. Contabilidad")
            file_conta = st.file_uploader("Subir Auxiliar por Tercero (.xlsx)", type=['xlsx'])
            render_upload_example({'NIT': ['900123456', '890987654'], 'Saldo Contable': ['$ 1,500,000', '4,800,000.00']}, help_text="Sube tu balance de comprobación o auxiliar contable. Sin formato estricto.")
            
        instrucciones = st.text_area("✍️ Instrucciones o contexto adicional para la IA (Opcional)", placeholder="Ej: Compara ambos archivos, cruza por NIT y muéstrame solo las diferencias mayores a $5.000.000. Detalla posibles errores en nombres.")

        if file_dian and file_conta:
            df_dian = safe_read_excel(file_dian)
            df_conta = safe_read_excel(file_conta)
            
            if df_dian.empty or df_conta.empty:
                st.error("❌ Error: Uno de los archivos está vacío. Verifica tus Excel.")
                st.stop()
                
            if st.button("▶️ EJECUTAR ANÁLISIS INTELIGENTE", type="primary", use_container_width=True):
                st.success("✅ Archivos cargados. Iniciando Motor de Inteligencia Artificial...")
                
                if api_key_valida:
                    with st.spinner("🤖 Analizando la estructura de los datos y cruzando información..."):
                        # Convertimos a CSV (solo una muestra suficiente) para que Gemini la procese
                        dian_csv = df_dian.head(500).to_csv(index=False)
                        conta_csv = df_conta.head(500).to_csv(index=False)
                        
                        prompt = f'''
                        Actúa como un Auditor Fiscal y Contable experto.
                        Se te han proporcionado dos extractos de datos:
                        
                        --- DATOS DIAN (Reporte Terceros) ---
                        {dian_csv}
                        
                        --- DATOS CONTABILIDAD ---
                        {conta_csv}
                        
                        INSTRUCCIONES DEL USUARIO:
                        "{instrucciones if instrucciones else 'Analiza ambos archivos, deduce las columnas correspondientes a Identificación (NIT/Cédula) y Valor, realiza un cruce para encontrar discrepancias, y presenta un informe detallado con las diferencias encontradas.'}"
                        
                        OBJETIVO:
                        Ignora la necesidad de que las columnas tengan nombres exactos o formatos estrictos.
                        Entiende el archivo, realiza el análisis o cruce solicitado por el usuario y responde de forma estructurada en formato Markdown.
                        Usa tablas obligatoriamente para mostrar las inconsistencias o diferencias entre ambos reportes.
                        Da una conclusión clara y profesional.
                        '''
                        response = consultar_ia_gemini(prompt)
                        render_smart_advisor(response)
                        
                        df_res = extract_md_table_to_df(response)
                        if not df_res.empty:
                            download_section(df_res, "Auditoria_DIAN_IA", "Reporte de Auditoría DIAN")
                        
                        with st.expander("🔍 Ver vista previa de los datos subidos"):
                            c1, c2 = st.columns(2)
                            c1.markdown("**Archivo DIAN:**")
                            c1.dataframe(df_dian.head(10))
                            c2.markdown("**Archivo Contabilidad:**")
                            c2.dataframe(df_conta.head(10))
                else:
                    st.error("⚠️ La Inteligencia Artificial no está conectada. Verifica tu API Key en la barra lateral.")

    elif menu == "Minería de XML (Facturación)":
        render_module_guide(
            get_text('title_xml'),
            "https://cdn-icons-png.flaticon.com/512/2823/2823523.png",
            get_text('desc_xml'),
            get_text('ben_xml')
        )
        archivos_xml = st.file_uploader("Cargar XMLs (Lote)", type=['xml'], accept_multiple_files=True)
        if archivos_xml and st.button("▶️ INICIAR PROCESAMIENTO"):
            st.toast("Procesando lote de archivos...")
            datos_xml = []; barra = st.progress(0)
            for i, f in enumerate(archivos_xml): barra.progress((i+1)/len(archivos_xml)); datos_xml.append(parsear_xml_dian(f))
            df_xml = pd.DataFrame(datos_xml)
            st.success("Extracción completada."); st.dataframe(df_xml, use_container_width=True)
            
            # Universal Download
            download_section(df_xml, "Resumen_Facturacion_XML", "Minería de Datos - Facturación Electrónica")

            # --- AI SMART ADVISOR RESTORED ---
            if api_key_valida:
                total_facturado = df_xml['Total a Pagar'].sum() if 'Total a Pagar' in df_xml.columns else 0
                render_smart_advisor(consultar_ia_gemini(f"Analiza este lote de facturas XML. Total facturado: {total_facturado}. Proveedores principales: {df_xml['Emisor'].unique()}"))

    elif menu == "Conciliación Bancaria IA":
        render_module_guide(
            get_text('title_bank'),
            "https://cdn-icons-png.flaticon.com/512/2830/2830284.png",
            get_text('desc_bank'),
            get_text('ben_bank')
        )
        
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            st.subheader("🏦 Extracto Bancario")
            file_banco = st.file_uploader("Subir Extracto (.xlsx)", type=['xlsx'], key="banco")
        with col_b2:
            st.subheader("📒 Libro Auxiliar Contable")
            file_libros = st.file_uploader("Subir Auxiliar de Bancos (.xlsx)", type=['xlsx'], key="libros")
            
        instrucciones = st.text_area("✍️ Instrucciones Específicas para la IA (Opcional)", height=150, placeholder="Ej: Las columnas de fecha tienen diferentes formatos, trata de cruzarlos. Los montos en el banco son negativos para retiros, pero en libros están en la columna Crédito.")

        if file_banco and file_libros:
            df_banco = safe_read_excel(file_banco)
            df_libros = safe_read_excel(file_libros)
            
            if df_banco.empty or df_libros.empty:
                st.error("❌ Al menos uno de los archivos está vacío.")
                st.stop()
                
            if st.button("▶️ EJECUTAR CONCILIACIÓN INTELIGENTE", type="primary", use_container_width=True):
                st.success("✅ Archivos cargados. Iniciando Conciliador IA...")
                
                if api_key_valida:
                    with st.spinner("🤖 Analizando y emparejando transacciones..."):
                        banco_csv = df_banco.head(500).to_csv(index=False)
                        libros_csv = df_libros.head(500).to_csv(index=False)
                        
                        prompt = f'''
                        Actúa como un Auditor Contable y Financiero experto en conciliaciones bancarias.
                        Tienes dos extractos de transacciones:
                        
                        --- EXTRACTO BANCARIO ---
                        {banco_csv}
                        
                        --- LIBRO AUXILIAR CONTABLE ---
                        {libros_csv}
                        
                        INSTRUCCIONES DEL USUARIO:
                        "{instrucciones if instrucciones else 'Realiza una conciliación bancaria. Encuentra las partidas conciliatorias (lo que está en bancos y no en libros, y viceversa). Busca montos idénticos o muy similares en fechas cercanas.'}"
                        
                        OBJETIVO:
                        Ignora formatos estrictos o nombres de columnas rígidos.
                        Usa tu inteligencia para identificar fechas, descripciones/referencias y montos.
                        Presenta un informe de conciliación con las partidas que cuadran y las partidas pendientes o no conciliadas.
                        Usa tablas para mostrar las transacciones huérfanas o discrepancias de montos.
                        Responde de forma clara y profesional en Markdown.
                        '''
                        response = consultar_ia_gemini(prompt)
                        render_smart_advisor(response)
                        
                        df_res = extract_md_table_to_df(response)
                        if not df_res.empty:
                            download_section(df_res, "Auditoria_DIAN_IA", "Reporte de Auditoría DIAN")
                        
                        with st.expander("🔍 Ver vista previa de los datos subidos"):
                            col1, col2 = st.columns(2)
                            col1.markdown("**Extracto Bancario:**")
                            col1.dataframe(df_banco.head(10))
                            col2.markdown("**Libro Contable:**")
                            col2.dataframe(df_libros.head(10))
                else:
                    st.error("⚠️ La Inteligencia Artificial no está conectada. Verifica tu API Key.")

    elif menu == "Auditoría Fiscal de Gastos":
        render_module_guide(
            get_text('title_gastos'),
            "https://cdn-icons-png.flaticon.com/512/3233/3233483.png",
            get_text('desc_gastos'),
            get_text('ben_gastos')
        )
        
        col_g1, col_g2 = st.columns([1, 2])
        with col_g1:
            ar = st.file_uploader("📥 Cargar Auxiliar de Gastos (.xlsx)", type=["xlsx"])
            render_upload_example(
                {'Fecha': ['2023-10-01', '2023-10-05'], 'Tercero': ['Restaurante X', 'Papelería Y'], 'Valor': [150000, 50000], 'Método Pago': ['Efectivo', 'Tarjeta'], 'Concepto': ['Almuerzo gerencia', 'Resmas']},
                "Formato sugerido",
                "Sube tu reporte de gastos. No te preocupes por el orden o los nombres de las columnas."
            )
            
        with col_g2:
            instrucciones = st.text_area("✍️ Instrucciones Específicas para la IA (Opcional)", height=150, placeholder="Ej: Ignora los gastos por debajo de $50,000. Revisa si 'Efectivo' incumple la norma de bancarización para compras grandes. La empresa es una agencia de publicidad.")

        if ar:
            df = safe_read_excel(ar)
            
            if df.empty:
                st.error("❌ El archivo está vacío.")
                st.stop()
                
            if st.button("▶️ EJECUTAR AUDITORÍA DE GASTOS CON IA", type="primary", use_container_width=True):
                st.success("✅ Archivo cargado. Iniciando Auditor Virtual...")
                
                if api_key_valida:
                    with st.spinner("🤖 Analizando la estructura de los datos y cruzando con normatividad fiscal..."):
                        gastos_csv = df.head(1000).to_csv(index=False)
                        
                        prompt = f'''
                        Actúa como un Auditor Fiscal y Tributario de alto nivel en Colombia.
                        Se te ha proporcionado un listado de gastos de la empresa:
                        
                        --- DATOS DE GASTOS ---
                        {gastos_csv}
                        
                        INSTRUCCIONES DEL USUARIO:
                        "{instrucciones if instrucciones else 'Analiza los gastos, identifica la columna de Valor y Método de Pago. Detecta posibles riesgos fiscales de no deducibilidad (Art. 107 ET: Causalidad, Proporcionalidad, Necesidad) y bancarización (Efectivo mayor a topes). Presenta los hallazgos en una tabla.'}"
                        
                        OBJETIVO:
                        Ignora la necesidad de que las columnas tengan nombres exactos o formatos estrictos.
                        Entiende el archivo, realiza el análisis o auditoría solicitada por el usuario y responde de forma estructurada en formato Markdown.
                        Destaca los riesgos críticos y usa tablas obligatoriamente para mostrar los gastos problemáticos.
                        '''
                        response = consultar_ia_gemini(prompt)
                        render_smart_advisor(response)
                        
                        df_res = extract_md_table_to_df(response)
                        if not df_res.empty:
                            download_section(df_res, "Auditoria_DIAN_IA", "Reporte de Auditoría DIAN")
                        
                        with st.expander("🔍 Ver vista previa de los datos subidos"):
                            st.dataframe(df.head(10))
                else:
                    st.error("⚠️ La Inteligencia Artificial no está conectada. Verifica tu API Key en la barra lateral.")

    elif menu == "Escáner de Nómina (UGPP)":
        render_module_guide(
            get_text('title_ugpp'),
            "https://cdn-icons-png.flaticon.com/512/3364/3364069.png",
            get_text('desc_ugpp'),
            get_text('ben_ugpp')
        )
        
        col_u1, col_u2 = st.columns([1, 2])
        with col_u1:
            ar = st.file_uploader("📥 Cargar Base de Nómina (.xlsx)", type=["xlsx"])
            render_upload_example(
                {'Empleado': ['Juan', 'Ana'], 'Salario Base': [2000000, 3000000], 'Bonos Flexibles': [500000, 1500000], 'Aux. Trasporte': [140606, 0]},
                "Formato sugerido",
                "Sube la nómina detallada. No te preocupes por el orden de las columnas, la IA las entenderá."
            )
        
        with col_u2:
            instrucciones = st.text_area("✍️ Instrucciones Específicas para la IA (Opcional)", height=150, placeholder="Ej: Comprueba que los bonos no constitutivos de salario (columna 'Flexibles') no superen el 40% del total devengado. Muestra alertas rojas si alguien se pasa.")

        if ar:
            df = safe_read_excel(ar)
            
            if df.empty:
                st.error("❌ El archivo está vacío.")
                st.stop()
                
            if st.button("▶️ EJECUTAR ESCÁNER UGPP CON IA", type="primary", use_container_width=True):
                st.success("✅ Archivo cargado. Iniciando Auditor UGPP Virtual...")
                
                if api_key_valida:
                    with st.spinner("🤖 Analizando topes y componentes salariales según Ley 1393..."):
                        nomina_csv = df.head(1000).to_csv(index=False)
                        
                        prompt = f'''
                        Actúa como un Auditor experto en Nómina y requerimientos de la UGPP en Colombia.
                        Se te ha proporcionado un listado de nómina de empleados:
                        
                        --- DATOS DE NÓMINA ---
                        {nomina_csv}
                        
                        INSTRUCCIONES DEL USUARIO:
                        "{instrucciones if instrucciones else 'Analiza la nómina, identifica salarios y pagos no constitutivos de salario. Aplica la Ley 1393 de 2010 (pagos no salariales no deben superar el 40% del total devengado). Identifica empleados en riesgo de sanción UGPP.'}"
                        
                        OBJETIVO:
                        Ignora formatos estrictos de columnas. Entiende qué significa cada dato.
                        Realiza el análisis o cálculo solicitado. Si detectas empleados donde los pagos no constitutivos superan el 40%, enuméralos en una tabla obligatoriamente.
                        Calcula el exceso o base presunta si es posible con los datos provistos.
                        Responde de forma estructurada, profesional y clara en formato Markdown.
                        '''
                        response = consultar_ia_gemini(prompt)
                        render_smart_advisor(response)
                        
                        df_res = extract_md_table_to_df(response)
                        if not df_res.empty:
                            download_section(df_res, "Auditoria_DIAN_IA", "Reporte de Auditoría DIAN")
                        
                        with st.expander("🔍 Ver vista previa de los datos subidos"):
                            st.dataframe(df.head(10))
                else:
                    st.error("⚠️ La Inteligencia Artificial no está conectada. Verifica tu API Key en la barra lateral.")

    elif menu == "Proyección de Tesorería":
        render_module_guide(
            get_text('title_treasury'),
            "https://cdn-icons-png.flaticon.com/512/5806/5806289.png",
            get_text('desc_treasury'),
            get_text('ben_treasury')
        )
        saldo_hoy = st.number_input("💵 Saldo Disponible Hoy ($):", min_value=0.0, format="%.2f")
        c1, c2 = st.columns(2)
        with c1:
             fcxc = st.file_uploader("Cartera (CxC)", type=['xlsx'])
             render_upload_example({'Fecha Vencimiento': ['2025-02-15'], 'Cliente': ['Cliente ABC'], 'Saldo': ['$ 5,000,000']}, "Ejemplo CxC", help_text="Sube tus Cuentas por Cobrar. La IA detectará las fechas y montos.")
        with c2:
             fcxp = st.file_uploader("Proveedores (CxP)", type=['xlsx'])
             render_upload_example({'Fecha Vencimiento': ['2025-02-10'], 'Proveedor': ['Prov. XYZ'], 'Total': ['2,500,000 COP']}, "Ejemplo CxP", help_text="Sube tus Cuentas por Pagar. La IA detectará las fechas y montos.")
             
        instrucciones = st.text_area("✍️ Instrucciones o contexto adicional para la IA (Opcional)", placeholder="Ej: Proyecta los pagos por semana en vez de por día. Considera que a los proveedores se les paga los viernes.")

        if fcxc and fcxp:
            dcxc = safe_read_excel(fcxc)
            dcxp = safe_read_excel(fcxp)
            
            if dcxc.empty or dcxp.empty:
                st.error("❌ Error: Al menos uno de los archivos está vacío.")
                st.stop()
                
            if st.button("▶️ GENERAR PROYECCIÓN CON IA", type="primary", use_container_width=True):
                st.success("✅ Archivos cargados. Iniciando Analista de Tesorería IA...")
                
                if api_key_valida:
                    with st.spinner("🤖 Analizando fechas de vencimiento y saldos..."):
                        cxc_csv = dcxc.head(500).to_csv(index=False)
                        cxp_csv = dcxp.head(500).to_csv(index=False)
                        
                        prompt = f'''
                        Actúa como un Gerente Financiero / Tesorero experto.
                        Tienes un Saldo Disponible Hoy de: ${saldo_hoy:,.2f}
                        Y los siguientes dos listados:
                        
                        --- CUENTAS POR COBRAR (CxC) ---
                        {cxc_csv}
                        
                        --- CUENTAS POR PAGAR (CxP) ---
                        {cxp_csv}
                        
                        INSTRUCCIONES DEL USUARIO:
                        "{instrucciones if instrucciones else 'Haz una proyección de flujo de caja. Empareja los ingresos y egresos proyectados en el tiempo. Suma los saldos diarios o semanales.'}"
                        
                        OBJETIVO:
                        Ignora formatos de columna rígidos. Identifica las columnas de Fecha, Monto, y Proveedor/Cliente.
                        Genera un flujo de caja estructurado y profesional en Markdown.
                        Obligatoriamente muestra el resultado de la proyección (Saldos finales por fecha) usando una tabla.
                        Advierte si el flujo de caja se vuelve negativo en algún punto.
                        '''
                        response = consultar_ia_gemini(prompt)
                        render_smart_advisor(response)
                        
                        df_res = extract_md_table_to_df(response)
                        if not df_res.empty:
                            download_section(df_res, "Proyeccion_Tesoreria_IA", "Flujo de Caja Proyectado")
                        
                        with st.expander("🔍 Ver vista previa de los datos subidos"):
                            c1, c2 = st.columns(2)
                            c1.markdown("**Cartera:**")
                            c1.dataframe(dcxc.head(10))
                            c2.markdown("**Proveedores:**")
                            c2.dataframe(dcxp.head(10))
                else:
                    st.error("⚠️ La IA no está conectada. Verifica tu API Key.")


    # ==============================================================================
    # 🚨 MÓDULO DE NÓMINA (CORREGIDO: Auto-Detección y Protección de Errores)
    # ==============================================================================
    elif menu == "Costeo de Nómina Real":
        render_module_guide(
            get_text('title_payroll'),
            "https://cdn-icons-png.flaticon.com/512/2328/2328761.png",
            get_text('desc_payroll'),
            get_text('ben_payroll')
        )
        
        col_c1, col_c2 = st.columns([1, 2])
        with col_c1:
            ac = st.file_uploader("Cargar Listado Personal (.xlsx)", type=['xlsx'])
            render_upload_example({'Nombre': ['Ana Gomez'], 'Salario Base': ['$ 3,500,000'], 'Auxilio Trans': ['NO'], 'Riesgo ARL': [1]}, help_text="Sube el listado de empleados. La IA detectará las columnas correspondientes.")
        
        with col_c2:
            instrucciones = st.text_area("✍️ Instrucciones o contexto adicional para la IA (Opcional)", height=150, placeholder="Ej: Considera que todos tienen riesgo ARL nivel 2. Ignora la columna de bonos ocasionales para el cálculo de aportes.")

        if ac:
            dc = safe_read_excel(ac)
            
            if dc.empty:
                st.error("❌ Error: El archivo está vacío o no es legible.")
                st.stop()
                
            if st.button("▶️ CALCULAR COSTEO CON IA", type="primary", use_container_width=True):
                st.success("✅ Archivo cargado. Iniciando Liquidador de Nómina Inteligente...")
                
                if api_key_valida:
                    with st.spinner("🤖 Calculando carga prestacional y aportes patronales..."):
                        nomina_csv = dc.head(500).to_csv(index=False)
                        
                        prompt = f'''
                        Actúa como un Experto Analista de Nómina en Colombia.
                        Tienes la siguiente nómina de empleados:
                        
                        --- DATOS DE NÓMINA ---
                        {nomina_csv}
                        
                        INSTRUCCIONES DEL USUARIO:
                        "{instrucciones if instrucciones else 'Calcula el costo real mensual por empleado para la empresa. Incluye salario, prestaciones sociales (cesantías, intereses, prima, vacaciones) y seguridad social/parafiscales patronales si aplican. Si no se especifica, asume ARL nivel 1 y evalúa si aplican exoneraciones de salud y parafiscales según Ley 1819.'}"
                        
                        OBJETIVO:
                        Ignora formatos de columna rígidos. Identifica Salarios, Nombres, Riesgos.
                        Realiza el cálculo contable solicitado.
                        Obligatoriamente muestra los resultados desglosados (Empleado, Salario, Carga Prestacional, Costo Total) en una tabla Markdown.
                        Incluye conclusiones u observaciones sobre optimización de costos laborales si lo consideras pertinente.
                        '''
                        response = consultar_ia_gemini(prompt)
                        render_smart_advisor(response)
                        
                        df_res = extract_md_table_to_df(response)
                        if not df_res.empty:
                            download_section(df_res, "Costeo_Nomina_Real_IA", "Costeo de Nómina Mensual")
                        
                        with st.expander("🔍 Ver vista previa de los datos subidos"):
                            st.dataframe(dc.head(10))
                else:
                    st.error("⚠️ La IA no está conectada. Verifica tu API Key.")

    
    # ==============================================================================
    # FIN DE LA CORRECCIÓN DE NÓMINA - CONTINÚAN LOS OTROS MÓDULOS
    # ==============================================================================

    elif menu == "Analítica Financiera Inteligente":
        render_module_guide(
            get_text('title_fin_ai'),
            "https://cdn-icons-png.flaticon.com/512/10041/10041467.png",
            get_text('desc_fin_ai'),
            get_text('ben_fin_ai')
        )
        
        col_f1, col_f2 = st.columns([1, 2])
        with col_f1:
            fi = st.file_uploader("Cargar Datos Financieros (.xlsx/.csv)", type=['xlsx', 'csv'])
            render_upload_example({'Cuenta': ['Ingresos Op', 'Gastos Admin'], 'Saldo': ['$ 50,000,000', '$ 12,000,000']}, help_text="Sube tus datos financieros. La IA los estructurará automáticamente.")
            
        with col_f2:
            instrucciones = st.text_area("✍️ Instrucciones o contexto adicional para la IA (Opcional)", height=150, placeholder="Ej: Agrupa todos los gastos de viaje en una sola categoría. Dime cuál es el rubro de gasto más alto y cómo reducirlo.")

        if fi and api_key_valida:
            df = safe_read_excel(fi)
            
            if df.empty:
                st.error("❌ Error: El archivo está vacío.")
                st.stop()
                
            if st.button("▶️ INICIAR ANÁLISIS IA", type="primary", use_container_width=True):
                st.success("✅ Datos cargados. Analista Financiero virtual en proceso...")
                with st.spinner("🤖 Analizando finanzas corporativas..."):
                    datos_csv = df.head(1000).to_csv(index=False)
                    
                    prompt = f'''
                    Actúa como un Auditor y Consultor Financiero.
                    Se te proporcionan los siguientes datos financieros:
                    
                    --- DATOS FINANCIEROS ---
                    {datos_csv}
                    
                    INSTRUCCIONES DEL USUARIO:
                    "{instrucciones if instrucciones else 'Agrupa los saldos por cuentas/categorías. Identifica los rubros más representativos e indica la salud financiera o áreas de optimización.'}"
                    
                    OBJETIVO:
                    Entiende el archivo sin requerir columnas exactas. Identifica conceptos y valores.
                    Responde con un análisis profundo en Markdown.
                    Muestra obligatoriamente una tabla con el resumen de las cuentas principales y sus montos.
                    '''
                    response = consultar_ia_gemini(prompt)
                    render_smart_advisor(response)
                    
                    df_res = extract_md_table_to_df(response)
                    if not df_res.empty:
                        download_section(df_res, "Analitica_Financiera_IA", "Análisis Financiero Inteligente")
                        
                    with st.expander("🔍 Ver vista previa de los datos subidos"):
                        st.dataframe(df.head(10))


    elif menu == "Narrador Financiero & NIIF":
        render_module_guide(
            get_text('title_narrator'),
            "https://cdn-icons-png.flaticon.com/512/3208/3208727.png",
            get_text('desc_narrator'),
            get_text('ben_narrator')
        )
        c1, c2 = st.columns(2)
        with c1:
             f1 = st.file_uploader("Año Actual", type=['xlsx'])
             render_upload_example({'Cuenta': ['Caja General'], 'Saldo 2025': ['$ 15,000,000.00']}, "Ej. Año Actual", help_text="Sube el balance del periodo actual.")
        with c2:
             f2 = st.file_uploader("Año Anterior", type=['xlsx'])
             render_upload_example({'Cuenta': ['Caja General'], 'Saldo 2024': ['$ 12,000,000']}, "Ej. Año Anterior", help_text="Sube el balance del periodo anterior.")
             
        instrucciones = st.text_area("✍️ Instrucciones o contexto adicional para la IA (Opcional)", height=150, placeholder="Ej: Redacta el informe con tono amigable. Destaca por qué subieron tanto las ventas y propón medidas para bajar los gastos administrativos.")

        if f1 and f2 and api_key_valida:
            d1 = safe_read_excel(f1)
            d2 = safe_read_excel(f2)
            
            if d1.empty or d2.empty:
                st.error("❌ Error: Al menos uno de los archivos está vacío.")
                st.stop()
            
            if st.button("✨ GENERAR INFORME Y NOTAS NIIF CON IA", type="primary", use_container_width=True):
                st.success("✅ Balances cargados. Iniciando Narrador Financiero...")
                with st.spinner("🤖 Analizando variaciones y redactando informe NIIF..."):
                    d1_csv = d1.head(500).to_csv(index=False)
                    d2_csv = d2.head(500).to_csv(index=False)
                    
                    prompt = f'''
                    Actúa como un CFO Corporativo y experto en NIIF.
                    Tienes los saldos contables de dos periodos:
                    
                    --- AÑO ACTUAL ---
                    {d1_csv}
                    
                    --- AÑO ANTERIOR ---
                    {d2_csv}
                    
                    INSTRUCCIONES DEL USUARIO:
                    "{instrucciones if instrucciones else 'Calcula las variaciones (absolutas y relativas) entre ambos periodos. Genera: 1. Un Informe Gerencial Ejecutivo destacando lo más importante. 2. Un borrador de Nota a los Estados Financieros bajo NIIF para las cuentas con mayor variación.'}"
                    
                    OBJETIVO:
                    Ignora el formato de las columnas. Cruza la información asumiendo que los nombres de cuentas similares son los mismos.
                    Responde en formato Markdown profesional.
                    Muestra obligatoriamente una tabla comparativa con las mayores variaciones.
                    '''
                    response = consultar_ia_gemini(prompt)
                    render_smart_advisor(response)
                    
                    df_res = extract_md_table_to_df(response)
                    if not df_res.empty:
                        download_section(df_res, "Notas_NIIF_IA", "Informe Financiero y Notas NIIF")
                        
                    with st.expander("🔍 Ver vista previa de los datos subidos"):
                        col1, col2 = st.columns(2)
                        col1.markdown("**Año Actual:**")
                        col1.dataframe(d1.head(10))
                        col2.markdown("**Año Anterior:**")
                        col2.dataframe(d2.head(10))


    elif menu == "Validador de RUT Oficial":
        render_module_guide(
            get_text('title_rut'),
            "https://cdn-icons-png.flaticon.com/512/9422/9422888.png",
            get_text('desc_rut'),
            get_text('ben_rut')
        )
        nit = st.text_input("Ingrese NIT o Cédula (Sin DV):", max_chars=15)
        if st.button("🔢 VERIFICAR"):
            dv = calcular_dv_colombia(nit); st.metric("Dígito de Verificación (DV)", dv); st.link_button("🔗 Consulta Estado en Muisca (DIAN)", "https://muisca.dian.gov.co/WebRutMuisca/DefConsultaEstadoRUT.faces")

    elif menu == "Digitalización OCR":
        render_module_guide(
            get_text('title_ocr'),
            "https://cdn-icons-png.flaticon.com/512/3588/3588241.png",
            get_text('desc_ocr'),
            get_text('ben_ocr')
        )
        metodo_ingreso = st.radio("Método de Ingreso", ["📂 Cargar Imágenes", "📸 Tomar Foto (Cámara)"], horizontal=True, label_visibility="collapsed")
        imagenes_a_procesar = []
        
        if metodo_ingreso == "📂 Cargar Imágenes":
            af = st.file_uploader("Sube facturas escaneadas", type=["jpg", "png"], accept_multiple_files=True)
            if af: imagenes_a_procesar.extend(af)
        else:
            foto = st.camera_input("Apunta a la factura física y captura")
            if foto: imagenes_a_procesar.append(foto)
            
        if len(imagenes_a_procesar) > 0:
            if st.button("🧠 PROCESAR IMÁGENES", type="primary", use_container_width=True):
                if not api_key_valida:
                    st.error("⚠️ La IA no está conectada. Verifica la API Key.")
                else:
                    do = []; bar = st.progress(0)
                    for i, f in enumerate(imagenes_a_procesar): 
                        bar.progress((i+1)/len(imagenes_a_procesar))
                        info = ocr_factura(Image.open(f))
                        if info: do.append(info)
                        
                    if do:
                        df_ocr = pd.DataFrame(do)
                        st.dataframe(df_ocr, use_container_width=True)
                        download_section(df_ocr, "Digitalizacion_OCR", "Datos Extraídos (OCR)")
                        
                        with st.spinner("🤖 Generando resumen masivo..."):
                             render_smart_advisor(consultar_ia_gemini(f"Resume estas facturas escaneadas: {df_ocr.to_string()}. Total: {df_ocr['total'].sum() if 'total' in df_ocr.columns else 'N/A'}."))
                    else:
                        st.warning("No se pudo extraer información de las imágenes.")

    elif menu == "Generador Logístico" or menu == "Generador de Cotizaciones":
        st.title("🚢 Generador de Liquidación Logística")
        st.markdown("---")
        # --- 1. CONFIGURACIÓN DE ENCABEZADO ---
        col_a, col_b, col_c = st.columns(3)
        cliente = col_a.text_input("Cliente / Razón Social", "CLIENTE GENERAL S.A.S")
        nit_cliente = col_b.text_input("NIT / Identificación", "900.000.000")
        fecha_op = col_c.date_input("Fecha de Operación")
        # TRM DEL DÍA (CRÍTICO)
        st.info("💡 Ingrese la TRM para convertir automáticamente los gastos en USD.")
        trm_dia = st.number_input("Tasa Representativa (TRM)", value=4150.0, step=1.0, format="%.2f")

        st.divider()
        # --- 2. DESCARGA DE PLANTILLA ---
        import io
        import pandas as pd
        from fpdf import FPDF
        st.subheader("1. Descargar Plantilla")
        # Modelo basado en el archivo "Juli" simplificado
        df_base = pd.DataFrame({
            "Categoria": ["GASTOS EN ORIGEN", "GASTOS EN ORIGEN", "FLETE INTERNACIONAL", "ADUANA", "TRANSPORTE TERRESTRE"],
            "Descripcion": ["Pick Up / Recogida", "Trámites en Origen", "Flete Marítimo/Aéreo", "Agenciamiento Aduanero", "Entrega en Bodega"],
            "Valor": [150, 65, 1200, 350000, 2800000],
            "Moneda": ["USD", "USD", "USD", "COP", "COP"]
        })
        buffer_down = io.BytesIO()
        with pd.ExcelWriter(buffer_down, engine='xlsxwriter') as writer:
            df_base.to_excel(writer, index=False)

        st.download_button("⬇️ Bajar Plantilla Excel", data=buffer_down.getvalue(), file_name="Plantilla_Liquidacion.xlsx", mime="application/vnd.ms-excel")

        # --- 3. CARGA Y PROCESAMIENTO ---
        st.subheader("2. Cargar Liquidación y Generar PDF")
        archivo = st.file_uploader("Sube el Excel con los datos", type=["xlsx", "xls"])
        if archivo:
            try:
                df = safe_read_excel(archivo)
                
                # Limpieza de nombres de columnas (Quitar espacios, manejar tildes)
                df.columns = [x.upper().strip() for x in df.columns]
                
                # Mapeo inteligente de columnas
                col_cat = next((x for x in df.columns if "CAT" in x), None)
                col_desc = next((x for x in df.columns if "DESC" in x), None)
                col_val = next((x for x in df.columns if "VAL" in x), None)
                col_mon = next((x for x in df.columns if "MON" in x), None)
                
                if not all([col_cat, col_desc, col_val, col_mon]):
                    st.error("❌ Error en columnas. Usa la plantilla descargable.")
                else:
                    # Lógica Matemática
                    def calcular_final(fila):
                        val = float(str(fila[col_val]).replace('$','').replace(',','')) # Limpiar texto
                        moneda = str(fila[col_mon]).upper().strip()
                        if "USD" in moneda:
                            return val * trm_dia
                        return val
                    df['TOTAL_COP'] = df.apply(calcular_final, axis=1)
                    
                    # Métricas
                    gran_total = df['TOTAL_COP'].sum()
                    total_usd = df[df[col_mon].astype(str).str.contains("USD")]['TOTAL_COP'].sum() / trm_dia
                    
                    m1, m2 = st.columns(2)
                    m1.metric("Total en Dólares (USD)", f"${total_usd:,.2f}")
                    m2.metric("GRAN TOTAL (COP)", f"${gran_total:,.0f}")
                    
                    st.dataframe(df, use_container_width=True)
                    # --- UNIVERSAL DOWNLOAD & AI ---
                    download_section(df, "Liquidacion_Logistica", f"Liquidación Importación - {cliente}")

                    if api_key_valida:
                        with st.spinner("🤖 Optimizando costos logísticos..."):
                             render_smart_advisor(consultar_ia_gemini(f"Analiza esta liquidación de importación. Total USD: {total_usd}. Total COP: {gran_total}. Ítems clave: {df[col_cat].unique()}. Da 3 tips de ahorro logístico."))
                    
                    # (Legacy PDF button removed to avoid confusion, using Universal instead)
                    if st.button("🖨️ Generar PDF Formal"):
                        class PDF(FPDF):
                            def header(self):
                                self.set_font('Arial', 'B', 14)
                                self.cell(0, 10, 'LIQUIDACION DE IMPORTACION', 0, 1, 'C')
                                self.ln(5)
                                
                        pdf = PDF()
                        pdf.add_page()
                        pdf.set_font('Arial', '', 10)
                        
                        # Datos
                        pdf.cell(0, 8, f"CLIENTE: {cliente}", 0, 1)
                        pdf.cell(0, 8, f"NIT: {nit_cliente} | FECHA: {fecha_op}", 0, 1)
                        pdf.cell(0, 8, f"TRM NEGOCIACION: ${trm_dia:,.2f}", 0, 1)
                        pdf.ln(5)
                        
                        # Iterar Categorías
                        categorias = df[col_cat].unique()
                        for cat in categorias:
                            pdf.set_fill_color(220, 220, 220)
                            pdf.set_font('Arial', 'B', 10)
                            pdf.cell(0, 8, str(cat), 1, 1, 'L', 1) # Título Sección
                            
                            # Items
                            pdf.set_font('Arial', '', 9)
                            items = df[df[col_cat] == cat]
                            for _, row in items.iterrows():
                                desc = str(row[col_desc])[:50]
                                val_orig = float(str(row[col_val]).replace('$','').replace(',',''))
                                mon = str(row[col_mon])
                                tot = row['TOTAL_COP']
                                
                                pdf.cell(100, 6, desc, 1)
                                pdf.cell(30, 6, f"{val_orig:,.2f} {mon}", 1)
                                pdf.cell(60, 6, f"${tot:,.0f}", 1, 1)
                            
                            # Subtotal
                            sub = items['TOTAL_COP'].sum()
                            pdf.set_font('Arial', 'B', 9)
                            pdf.cell(130, 6, "SUBTOTAL:", 1, 0, 'R')
                            pdf.cell(60, 6, f"${sub:,.0f}", 1, 1, 'R')
                            pdf.ln(2)
                            
                        # Total Final
                        pdf.ln(5)
                        pdf.set_font('Arial', 'B', 12)
                        pdf.cell(130, 10, "TOTAL A PAGAR:", 0, 0, 'R')
                        pdf.cell(60, 10, f"${gran_total:,.0f}", 1, 1, 'R')
                        
                        val = pdf.output(dest='S').encode('latin-1')
                        st.download_button("💾 Descargar PDF", data=val, file_name="Liquidacion.pdf", mime="application/pdf")
            
            except Exception as e:
                st.error(f"Error técnico: {e}")





    elif menu == "👑 Consola Administrativa":
        st.title("👑 Consola Administrativa")
        st.markdown("---")
        
        # Validar PIN
        if "admin_authenticated" not in st.session_state:
            st.session_state.admin_authenticated = False
            
        if not st.session_state.admin_authenticated:
            pin_input = st.text_input("Ingrese PIN de Administrador:", type="password")
            if st.button("Ingresar"):
                if pin_input == "2711":
                    st.session_state.admin_authenticated = True
                    st.rerun()
                else:
                    st.error("PIN Incorrecto.")
        else:
            if st.button("Cerrar Sesión Admin", key="logout_admin"):
                st.session_state.admin_authenticated = False
                st.rerun()
                
            db = get_firestore_db()
            if not db:
                st.error("❌ No hay conexión a la base de datos (Firestore).")
            else:
                with st.spinner("Conectando con Firestore y recopilando métricas en tiempo real..."):
                    users_ref = db.collection('users')
                    
                    try:
                        docs = users_ref.stream()
                        
                        user_data = []
                        total_users = 0
                        pagos = 0
                        tokens = 0
                        
                        # Conteo de conectados en las últimas 24h
                        import datetime
                        now = datetime.datetime.now(datetime.timezone.utc)
                        conectados_24h = 0
                        
                        for doc in docs:
                            total_users += 1
                            data = doc.to_dict()
                            
                            email = doc.id
                            plan = data.get('plan', 'FREE')
                            credits_used = data.get('credits_used', 0)
                            last_login_ts = data.get('last_login')
                            
                            # Manejo de Timestamp
                            last_login_str = "Nunca"
                            is_recent = False
                            if last_login_ts:
                                try:
                                    # Firestore devuelve datetime con timezone
                                    delta = now - last_login_ts
                                    if delta.total_seconds() < 86400: # 24 horas
                                        conectados_24h += 1
                                        is_recent = True
                                    last_login_str = last_login_ts.strftime('%Y-%m-%d %H:%M')
                                except:
                                    pass
                                    
                            if plan.upper() in ['PRO', 'PREMIUM']:
                                pagos += 1
                                
                            tokens += credits_used
                            
                            user_data.append({
                                "Email": email,
                                "Plan": plan.upper(),
                                "Créditos Usados": credits_used,
                                "Último Login": last_login_str,
                                "Activo (24h)": "🟢 Sí" if is_recent else "⚪ No"
                            })
                            
                    except Exception as e:
                        error_msg = str(e)
                        if "has not been used" in error_msg or "SERVICE_DISABLED" in error_msg:
                            st.error("⚠️ **Tu Base de Datos de Firebase está desactivada en Google Cloud.**")
                            st.info("💡 **CÓMO ARREGLARLO:**\n1. Haz clic en este enlace oficial de Google: 👉 [Activar API de Firestore](https://console.developers.google.com/apis/api/firestore.googleapis.com/overview?project=alcontador-data)\n2. Dale al botón azul de **'Habilitar'**.\n3. Espera 2 minutos y recarga esta página.")
                        else:
                            st.error(f"❌ Error al leer Firebase: {error_msg}")
                            st.info("💡 Asegúrate de que tu Service Account tenga el rol de 'Administrador de Cloud Datastore'.")
                            
                        st.markdown("### 📊 Panel de Control (Modo Demostración)")
                        c1, c2, c3, c4 = st.columns(4)
                        c1.metric("Usuarios Registrados", "---")
                        c2.metric("Suscripciones (Pagos)", "---")
                        c3.metric("Tokens/Créditos Usados", "---")
                        c4.metric("Conectados (24h)", "---")
                        st.stop()
                
                st.markdown("### 📊 Panel de Control en Tiempo Real")
                
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Usuarios Registrados", total_users)
                c2.metric("Suscripciones (Pagos)", pagos)
                c3.metric("Tokens/Créditos Usados", tokens)
                c4.metric("Conectados (24h)", conectados_24h)
                
                st.markdown("### 👥 Base de Datos de Usuarios")
                if user_data:
                    import pandas as pd
                    df_users = pd.DataFrame(user_data)
                    # Ordenar por activo primero y luego por fecha
                    df_users = df_users.sort_values(by=["Activo (24h)", "Último Login"], ascending=[False, False])
                    st.dataframe(df_users, use_container_width=True)
                    
                    # Grafiquito rápido de distribución de planes
                    plan_counts = df_users['Plan'].value_counts()
                    st.markdown("#### Distribución de Planes")
                    st.bar_chart(plan_counts)
                else:
                    st.info("No hay usuarios registrados aún.")



# ==============================================================================
# PIE DE PÁGINA
# ==============================================================================
st.markdown("---")
st.markdown("<center><strong>Asistente Contable Pro</strong> | Versión 1.0</center>", unsafe_allow_html=True)



# ==============================================================================
# COPILOTO TRIBUTARIO (CHATBOT FLOTANTE SIDEBAR)
def render_tax_copilot():
    """
    Renderiza el asistente de IA en la barra lateral.
    """
    # Cargar la imagen del avatar con audífonos en Base64 para inyectarla en HTML
    import base64
    import os
    img_b64 = ""
    # Usar ruta relativa para mayor compatibilidad
    img_path = os.path.join("assets", "asesor_formal.jpg")
    
    if os.path.exists(img_path):
        try:
            with open(img_path, "rb") as f:
                img_b64 = base64.b64encode(f.read()).decode()
        except Exception as e:
            st.error(f"Error cargando imagen: {e}")
            
    img_src = f"data:image/jpeg;base64,{img_b64}" if img_b64 else "https://cdn-icons-png.flaticon.com/512/8943/8943377.png"

    # Inyectar CSS para el header del chat en el sidebar
    st.markdown("""
    <style>
    .chat-header-sidebar {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    .chat-avatar-sidebar {
        width: 45px;
        height: 45px;
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid #34d399;
    }
    /* Ocultar el texto "Press Enter to submit form" de Streamlit */
    div[data-testid="InputInstructions"] {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("---") # Separador visual
        
        # Estado del Chat (Persistencia)
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
            
        with st.expander("💬 Copiloto y Soporte IA", expanded=False):
            
            # Cabecera del chat con la imagen
            st.markdown(f"""
            <div class="chat-header-sidebar">
                <img src="{img_src}" class="chat-avatar-sidebar">
                <div>
                    <h3 style="margin:0; color:white; font-size:14px;">Soporte y Copiloto</h3>
                    <span style="color:#34d399; font-size:11px; font-weight:600;">● En línea | Responde al instante</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Contenedor de Historia (Scroll simulado)
            chat_container = st.container(height=300)
            with chat_container:
                for msg in st.session_state.chat_history:
                    # Usar la foto formal para el asistente, y el emoji predeterminado para el usuario
                    avatar_img = img_src if msg["role"] == "assistant" else "👤"
                    with st.chat_message(msg["role"], avatar=avatar_img):
                        st.markdown(msg["content"])
            
            # Zona de Input (Tipo Formulario para no recargar toda la app)
            with st.form(key="chat_form", clear_on_submit=True):
                user_input = st.text_input("Escribe tu consulta aquí...", placeholder="Ej: ¿Cómo subo el Excel?")
                submit_btn = st.form_submit_button("Enviar Consulta 🚀")
                
            if submit_btn and user_input:
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                
                contexto_legal = f"""
                ACTÚA COMO: 
                1. EXPERTO CONTADOR Y ABOGADO TRIBUTARISTA DE COLOMBIA (Normativa 2026).
                2. AGENTE DE SOPORTE TÉCNICO de esta aplicación ('Asistente Contable Pro'). Ayuda al usuario a entender cómo usar los módulos, qué archivos subir o cómo solucionar errores.
                
                DATOS OFICIALES 2026:
                - SMMLV: ${SMMLV_2026:,.0f}
                - AUXILIO TRANSPORTE: ${AUX_TRANS_2026:,.0f}
                - UVT 2026: ${UVT_2026:,.0f}
                - BASE RETENCIÓN COMPRAS (27 UVT): ${BASE_RET_COMPRAS:,.0f}
                - BASE RETENCIÓN SERVICIOS (4 UVT): ${BASE_RET_SERVICIOS:,.0f}
                - TOPE BANCARIZACIÓN (100 UVT): ${TOPE_EFECTIVO:,.0f}
                
                INSTRUCCIÓN: Responde de forma clara y amigable. Si es una duda contable, cita la norma. Si es una duda sobre la app, guíalo paso a paso.
                PREGUNTA DEL USUARIO: {user_input}
                """
                
                try:
                    with st.spinner("Analizando..."):
                        respuesta = consultar_ia_gemini(contexto_legal)
                    
                    st.session_state.chat_history.append({"role": "assistant", "content": respuesta})
                    st.rerun() 
                except Exception as e:
                    st.error(f"Error IA: {str(e)}")
        
        # Colocar la normativa al final de la barra lateral
        st.markdown("---")
        st.caption(f"🇨🇴 **Normativa 2026 Activa**")
        st.caption(f"UVT: $52,374 | SMMLV: $1.7M")

# Ejecutar el Chatbot al final para asegurar que todas las constantes están cargadas
render_tax_copilot()

