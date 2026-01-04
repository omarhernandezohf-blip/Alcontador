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
from streamlit_oauth import OAuth2Component
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
import uuid
import firebase_admin
from firebase_admin import credentials, firestore

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Alcontador Empresarial",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CONFIGURACIÓN DE ESTILO GLOBAL (ENTERPRISE TRUST THEME) ---
st.markdown("""
    <style>
        /* --- SIDEBAR TOGGLE VISIBILITY FIX --- */
        [data-testid="stSidebarCollapsedControl"] {
            z-index: 999999 !important;
            color: white !important;
            background-color: rgba(255, 255, 255, 0.2) !important;
            border: 2px solid white !important;
            border-radius: 50%;
            padding: 6px;
            display: block !important;
            position: fixed !important;
            left: 20px !important;
            top: 20px !important;
        }

        [data-testid="stSidebarNav"] {
            z-index: 999999 !important;
        }

        [data-testid="stSidebar"] {
            z-index: 999998 !important;
            background-color: #020617 !important;
        }

        /* --- FONTS --- */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=Manrope:wght@400;600;800&display=swap');

        /* --- VARIABLES --- */
        :root {
            --bg-void: #020617;
            --bg-deep: #0f172a;
            --primary: #6366f1; /* Electric Indigo */
            --secondary: #3b82f6; /* Slate Blue */
            --success: #10b981; /* Emerald */
            --text-primary: #ffffff;
            --text-body: #94a3b8;
            --glass-bg: rgba(30, 41, 59, 0.7);
            --glass-border: rgba(255, 255, 255, 0.08);
            --shadow-soft: 0 4px 24px -1px rgba(0, 0, 0, 0.2);
            --shadow-glow: 0 0 20px rgba(99, 102, 241, 0.15);
        }

        /* --- BASE & BACKGROUND --- */
        .stApp {
            background: radial-gradient(circle at top right, #1e293b, transparent 40%),
                        radial-gradient(circle at bottom left, #1e1b4b, transparent 40%),
                        linear-gradient(180deg, #0f172a 0%, #020617 100%) !important;
            background-attachment: fixed !important;
            font-family: 'Inter', sans-serif;
            color: var(--text-body);
        }

        /* --- TYPOGRAPHY --- */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Inter', sans-serif !important;
            color: var(--text-primary) !important;
            font-weight: 800 !important;
            letter-spacing: -0.5px !important;
        }

        p, div, span, label {
            font-family: 'Inter', sans-serif;
            color: var(--text-body);
        }

        /* --- GLASSMORPHISM CARDS --- */
        div[data-testid="stExpander"], .glass-card, .pricing-card, .pro-module-header {
            background: var(--glass-bg) !important;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255,255,255,0.08) !important;
            border-top: 1px solid rgba(255,255,255,0.15) !important; /* Highlight top */
            border-radius: 12px !important;
            box-shadow: var(--shadow-soft);
        }

        /* --- SIDEBAR (CONTROL DOCK) --- */
        [data-testid="stSidebar"] {
            background: #020617 !important;
            border-right: 1px solid rgba(255,255,255,0.05);
        }

        /* Radio Buttons as Nav Tabs */
        .stRadio > div[role="radiogroup"] > label {
            background: transparent !important;
            border: none;
            padding: 12px 16px !important;
            color: var(--text-body) !important;
            border-left: 3px solid transparent;
            transition: all 0.2s ease;
            font-weight: 500;
        }

        .stRadio > div[role="radiogroup"] > label:hover {
            color: var(--text-primary) !important;
            background: rgba(255,255,255,0.03) !important;
        }

        .stRadio > div[role="radiogroup"] > label[data-checked="true"] {
            background: linear-gradient(90deg, rgba(99, 102, 241, 0.1), transparent) !important;
            border-left: 3px solid var(--primary) !important;
            color: var(--text-primary) !important;
            font-weight: 600;
        }

        /* --- WIDGETS --- */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stSelectbox > div > div > div {
            background-color: rgba(15, 23, 42, 0.6) !important;
            color: white !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 8px;
        }

        /* --- BUTTONS --- */
        .stButton > button {
            background: var(--primary) !important;
            color: white !important;
            border-radius: 8px !important;
            border: none !important;
            font-weight: 600 !important;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
            transition: all 0.2s;
        }
        .stButton > button:hover {
            background: #4f46e5 !important; /* Darker Indigo */
            box-shadow: 0 6px 16px rgba(99, 102, 241, 0.5);
            transform: translateY(-1px);
        }

        /* --- DATAFRAMES --- */
        [data-testid="stDataFrame"] {
            background: rgba(15, 23, 42, 0.5);
            border: 1px solid rgba(255,255,255,0.05);
            border-radius: 8px;
        }

        /* --- METRICS --- */
        [data-testid="stMetricValue"] {
            font-family: 'Inter', sans-serif;
            font-weight: 700;
            color: var(--text-primary) !important;
            text-shadow: 0 0 20px rgba(255,255,255,0.1);
        }
        [data-testid="stMetricLabel"] {
            color: var(--text-body) !important;
            font-size: 0.85rem;
            font-weight: 500;
        }

        /* Hide Defaults */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* Helpers */
        .pro-module-icon { width: 32px; height: 32px; margin-right: 12px; opacity: 0.9; }
        .detail-box {
            background: rgba(59, 130, 246, 0.05);
            border-left: 3px solid var(--secondary);
            padding: 16px;
            border-radius: 0 8px 8px 0;
            margin-bottom: 24px;
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
        'model': 'gemini-1.5-pro',
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
        'desc_ugpp': "Audit labor payments. Verifies if NON-salary payments exceed 40% of the total (Art. 30 Law 1393).",
        'ben_ugpp': ["Cálculo automático de exceso", "Alerta de riesgo alto", "Soporte para fiscalización"],

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
# 2. GESTIÓN DE CONEXIONES EXTERNAS (BACKEND) Y SEGURIDAD (OAUTH2)
# ==============================================================================

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
    if google_secrets_ok:
        try:
            oauth2 = OAuth2Component(
                client_id=st.secrets["google"]["client_id"],
                client_secret=st.secrets["google"]["client_secret"],
                authorize_endpoint="https://accounts.google.com/o/oauth2/v2/auth",
                token_endpoint="https://oauth2.googleapis.com/token",
                refresh_token_endpoint="https://oauth2.googleapis.com/token",
                revoke_token_endpoint="https://oauth2.googleapis.com/revoke",
            )

            # --- CENTER THE BUTTON USING COLUMNS AS REQUESTED ---
            left_col, center_col, right_col = st.columns([1, 2, 1])

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

# --- SIDEBAR: LANGUAGE SELECTOR (Global Access) ---
with st.sidebar:
    # Language selector accessible even on Login Page
    lang = st.selectbox("Language / Idioma", ["Español", "English"], key="lang")

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

        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)

            # Consumir crédito solo si éxito
            consume_credit(email)
            st.session_state['credits_used'] = credits + 1

            return response.text
        except Exception as e:
            return f"Error IA ({model_name}): {str(e)}"
    except Exception as e:
        return f"Error crítico IA: {str(e)}"

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

# ==============================================================================
# ==============================================================================
# 5. BARRA LATERAL (SIDEBAR) - NAVEGACIÓN Y LOGIN
# ==============================================================================
# ==============================================================================

with st.sidebar:
    # Logo
    st.image("https://cdn-icons-png.flaticon.com/512/2830/2830303.png", width=80)
    st.markdown("### 💼 Suite Financiera", unsafe_allow_html=True)
    
    # --- PANEL DE USUARIO LOGUEADO (SIDEBAR) ---
    current_plan = st.session_state.get('user_plan', 'FREE')
    plan_data = PLAN_CONFIG.get(current_plan, PLAN_CONFIG['FREE'])
    plan_bg = "#FFD700" if current_plan == 'PRO' else "#A9A9A9"
    if current_plan == 'PREMIUM': plan_bg = "#cf1b1b" # Red for Premium

    status_db = "🟢 DB Online" if db_conectada else "🔴 DB Offline"
    
    # Security: Escape variables injected into HTML
    user_plan_safe = html.escape(str(current_plan))
    estado_ia_safe = html.escape(str(estado_ia))
    status_db_safe = html.escape(str(status_db))

    # User Info from Google
    user_name = html.escape(str(st.session_state.get('username', 'Commander')))
    user_pic = html.escape(str(st.session_state.get('user_picture', '')))

    # Show User Profile
    if user_pic:
        st.markdown(f"<img src='{user_pic}' style='width: 50px; height: 50px; border-radius: 50%; margin-bottom: 10px; border: 2px solid var(--primary);'>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style='background: rgba(255,255,255,0.05); padding: 15px; border-radius: 4px; border-left: 3px solid {plan_bg}; margin-bottom: 20px;'>
        <small style='color: #94a3b8; text-transform:uppercase;'>{get_text('lbl_operator')}</small><br>
        <strong style='font-size: 1.1rem; color:white; font-family: "Inter", sans-serif;'>{user_name}</strong><br>
        <span style="font-size: 0.8rem; color: var(--primary);">{user_plan_safe} {get_text('lbl_access')}</span><br>
        <small style='color: #64748b;'>{estado_ia_safe}</small><br>
        <small style='color: {'#06b6d4' if db_conectada else '#ef4444'}; font-weight:bold;'>{status_db_safe}</small>
    </div>
    """, unsafe_allow_html=True)

    # --- CREDIT USAGE ---
    credits_used = st.session_state.get('credits_used', 0)
    limit = plan_data['limit']
    progress = min(credits_used / limit, 1.0) if limit > 0 else 1.0

    st.markdown(f"<small style='color:#94a3b8'>{get_text('lbl_credits')} {credits_used} / {limit}</small>", unsafe_allow_html=True)
    st.progress(progress)

    if current_plan == 'FREE':
        st.markdown("---")
        st.write(f"🔓 {get_text('lbl_unlock')}")
        st.link_button(
            get_text('lbl_go_pro'),
            "https://checkout.wompi.co/l/TU_LINK_PRO",
            type="primary"
        )
        st.link_button(
            get_text('lbl_go_prem'),
            "https://checkout.wompi.co/l/TU_LINK_PREMIUM"
        )

    if st.button(get_text('lbl_logout')):
        registrar_log(st.session_state.get('username', 'Unknown'), "Logout", "Salida del sistema")
        st.session_state.clear()
        st.rerun()

    st.markdown("---")
    
    # MENU MAPPING FOR NAVIGATION LOGIC
    MENU_KEYS = {
        get_text('menu_dash'): "Inicio / Dashboard",
        get_text('menu_dian'): "Auditoría Cruce DIAN",
        get_text('menu_xml'): "Minería de XML (Facturación)",
        get_text('menu_bank'): "Conciliación Bancaria IA",
        get_text('menu_fiscal'): "Auditoría Fiscal de Gastos",
        get_text('menu_ugpp'): "Escáner de Nómina (UGPP)",
        get_text('menu_treasury'): "Proyección de Tesorería",
        get_text('menu_payroll'): "Costeo de Nómina Real",
        get_text('menu_fin_ai'): "Analítica Financiera Inteligente",
        get_text('menu_narrator'): "Narrador Financiero & NIIF",
        get_text('menu_rut'): "Validador de RUT Oficial",
        get_text('menu_ocr'): "Digitalización OCR"
    }

    opciones_menu = list(MENU_KEYS.keys())

    menu_selection = st.radio(get_text('lbl_modules'), opciones_menu)
    # Reverse lookup to get canonical key for logic
    menu = MENU_KEYS.get(menu_selection, "Inicio / Dashboard")
    
    st.markdown("<br><center><small style='color: #64748b;'>v14.5 ENTERPRISE</small></center>", unsafe_allow_html=True)

# ==============================================================================
# ==============================================================================
# 6. CONTENIDO PRINCIPAL (DASHBOARD Y MÓDULOS)
# ==============================================================================
# ==============================================================================

if menu == "Inicio / Dashboard":
    # 1. HEADER EJECUTIVO (HERO SECTION - ENTERPRISE TRUST)
    st.markdown("""
    <div class="hero-container">
        <div class="hero-content">
            <h1 class="hero-title">Asistente Contable <span style="color: var(--primary)">PRO</span></h1>
            <div class="hero-subtitle">v14.5 Suite Empresarial • <span style="color: var(--success)">Sistema En Línea</span></div>
        </div>
    </div>
    <style>
        .hero-container {
            position: relative;
            padding: 3rem 2rem;
            margin-bottom: 2rem;
            background: linear-gradient(90deg, rgba(99, 102, 241, 0.1), transparent);
            border-left: 4px solid var(--primary);
            border-radius: 8px;
            overflow: hidden;
            backdrop-filter: blur(12px);
            box-shadow: var(--shadow-soft);
        }
        .hero-title {
            font-family: 'Inter', sans-serif !important;
            font-size: 3rem !important;
            font-weight: 800 !important;
            margin: 0;
            letter-spacing: -1px;
            color: white;
            text-shadow: 0 0 40px rgba(99, 102, 241, 0.3);
        }
        .hero-subtitle {
            font-family: 'Inter', sans-serif;
            font-size: 1.1rem;
            color: var(--text-body);
            margin-top: 0.5rem;
            font-weight: 500;
        }
    </style>
    """, unsafe_allow_html=True)

    # 2. BENTO GRID DASHBOARD (Métricas y Gráficos)

    def metric_card(label, value, delta, is_positive=True):
        color = "#10b981" if is_positive else "#f43f5e"
        arrow = "↑" if is_positive else "↓"
        st.markdown(f"""
        <div class="glass-card" style="height: 100%; display: flex; flex-direction: column; justify-content: center; padding: 24px;">
            <div style="color: var(--text-body); font-family: 'Inter'; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; margin-bottom: 8px; letter-spacing: 0.5px;">{label}</div>
            <div style="font-family: 'Inter'; font-size: 2rem; font-weight: 800; color: white; margin-bottom: 5px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; letter-spacing: -1px;">{value}</div>
            <div style="color: {color}; font-size: 0.95rem; font-weight: 600; font-family: 'Inter';">
                {arrow} {delta} <span style="color: var(--text-body); font-weight: 400;">vs periodo anterior</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 📊 MÉTRICAS EN VIVO")
    col1, col2, col3, col4 = st.columns(4)
    with col1: metric_card("INGRESOS TOTALES", "$124,500", "12%", True)
    with col2: metric_card("GASTOS OP.", "$42,300", "5%", False)
    with col3: metric_card("UTILIDAD NETA", "$82,200", "18%", True)
    with col4: metric_card("MARGEN EBITDA", "34%", "2%", True)

    st.markdown("---")

    c_chart_1, c_chart_2 = st.columns([2, 1])
    with c_chart_1:
        st.markdown("#### 📈 TENDENCIA DE FLUJO DE CAJA")
        chart_data = pd.DataFrame(np.random.randn(20, 3) + [10, 10, 10], columns=['Ingresos', 'Gastos', 'Utilidad'])
        st.area_chart(chart_data, color=["#06b6d4", "#ef4444", "#10b981"])
    with c_chart_2:
        st.markdown("#### 📉 DESGLOSE DE GASTOS")
        gastos_data = pd.DataFrame({'Categoría': ['Nómina', 'Software', 'Oficina', 'Publicidad'], 'Monto': [5000, 2000, 1500, 3000]})
        st.bar_chart(gastos_data.set_index('Categoría'), color="#8b5cf6")

    st.markdown("### 📝 REGISTRO DE TRANSACCIONES")
    df_transacciones = pd.DataFrame({
        "ID": ["TRX-001", "TRX-002", "TRX-003", "TRX-004", "TRX-005"],
        "FECHA": ["2024-05-01", "2024-05-02", "2024-05-02", "2024-05-03", "2024-05-03"],
        "CONCEPTO": ["Pago Cliente A", "Suscripción AWS", "Pago Cliente B", "Licencias Oficina", "Consultoría"],
        "ESTADO": ["COMPLETADO", "PENDIENTE", "COMPLETADO", "COMPLETADO", "REVISIÓN"],
        "MONTO": ["+$1,200", "-$300", "+$4,500", "-$150", "+$2,000"]
    })
    st.dataframe(df_transacciones, use_container_width=True, hide_index=True)

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
            padding: 2.5rem;
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
        .pro-badge {
            position: absolute; top: -12px; right: 24px;
            background: var(--success);
            color: white; padding: 4px 12px; border-radius: 99px;
            font-size: 0.75rem; font-weight: 700; letter-spacing: 0.5px; font-family: 'Inter';
        }
        .price-tag { font-family: 'Inter'; font-size: 3rem; font-weight: 800; color: white; margin: 10px 0; letter-spacing: -1px; }
        .price-tag span { font-size: 1rem; color: var(--text-body); font-weight: 500; font-family: 'Inter'; }
        .price-old { font-size: 1.1rem; color: #64748b; text-decoration: line-through; margin-top: 10px; font-family: 'Inter'; }
        .features-ul { list-style: none; padding: 0; margin: 24px 0; color: var(--text-body); flex-grow: 1; font-family: 'Inter'; font-size: 1rem; }
        .features-ul li { margin-bottom: 12px; display: flex; align-items: center; }
        .check { color: var(--success); margin-right: 12px; font-weight: bold; }
        .cross { color: #ef4444; margin-right: 12px; opacity: 0.7; }
        .dimmed { color: #475569; }
    </style>
    """, unsafe_allow_html=True)

    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.markdown("""
        <div class="pricing-card">
            <h3 style="color:white; margin:0; font-size: 1.4rem;">NIVEL INICIAL</h3>
            <div class="price-tag">$0 <span>COP/mes</span></div>
            <ul class="features-ul">
                <li><span class="check">✓</span> Acceso al Dashboard</li>
                <li><span class="check">✓</span> 5 Consultas IA/día</li>
                <li class="dimmed"><span class="cross">✕</span> Agente Tributario</li>
                <li class="dimmed"><span class="cross">✕</span> Conexión Bancaria</li>
            </ul>
        </div>""", unsafe_allow_html=True)
        st.button("CONTINUAR GRATIS", key="btn_free", use_container_width=True)

    with col_p2:
        st.markdown("""
        <div class="pricing-card pro">
            <div class="pro-badge">⭐ MÁS POPULAR</div>
            <h3 style="color:white; margin:0; font-size: 1.4rem;">PLAN PRO</h3>
            <div class="price-old">$100.000</div> <div class="price-tag">$70.000 <span>COP/mes</span></div>
            <ul class="features-ul">
                <li><span class="check">✓</span> <strong>500 Créditos Mensuales</strong></li>
                <li><span class="check">✓</span> Modelo Gemini 1.5 Flash (Rápido)</li>
                <li><span class="check">✓</span> Todos los Módulos Contables</li>
                <li><span class="check">✓</span> Soporte Prioritario</li>
            </ul>
        </div>""", unsafe_allow_html=True)
        st.link_button("⚡ MEJORAR A PRO", "https://checkout.wompi.co/l/TU_LINK_PRO", type="primary", use_container_width=True)

    with st.expander("🧠 Ver Plan Premium (Inteligencia Superior)"):
        st.markdown("""
        <div class="pricing-card" style="border: 1px solid #10b981;">
            <h3 style="color:white; margin:0; font-size: 1.4rem;">PLAN PREMIUM</h3>
            <div class="price-old">$180.000</div> <div class="price-tag">$120.000 <span>COP/mes</span></div>
            <ul class="features-ul">
                <li><span class="check">✓</span> <strong>2.000 Créditos Mensuales</strong></li>
                <li><span class="check">✓</span> <strong>Modelo Gemini 1.5 PRO (Razonamiento Complejo)</strong></li>
                <li><span class="check">✓</span> Análisis Financiero Profundo</li>
                <li><span class="check">✓</span> Auditoría NIIF Avanzada</li>
            </ul>
        </div>""", unsafe_allow_html=True)
        st.link_button("🚀 OBTENER PREMIUM", "https://checkout.wompi.co/l/TU_LINK_PREMIUM", use_container_width=True)

    if not db_conectada:
        st.warning("⚠️ BASE DE DATOS OFFLINE. Verifique conexión a 'DB_Alcontador'.")

# ---------------------------------------------------------
# ELSE: CAMBIO DE MENÚ (ESTE SÍ TOCA EL BORDE IZQUIERDO)
# ---------------------------------------------------------
else:
    # 1. AUDITORÍA
    if menu == "Auditoría Cruce DIAN":
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

                    # --- AI SMART ADVISOR RESTORED ---
                    if api_key_valida:
                        with st.spinner("🤖 Consultando análisis experto..."):
                            summary_prompt = f"Actúa como un auditor fiscal experto. Se encontraron {num_hallazgos} diferencias por un total de {total_riesgo}. Analiza qué riesgos implica esto frente a la UGPP y la DIAN en Colombia."
                            response = consultar_ia_gemini(summary_prompt)
                            render_smart_advisor(response)
                
                except Exception as e:
                    st.error(f"Algo salió mal: {e}. Revisa 'Configuración manual' arriba.")

    # 2. MINERÍA XML
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
            out = io.BytesIO();
            with pd.ExcelWriter(out, engine='xlsxwriter') as w: df_xml.to_excel(w, index=False)
            st.download_button("📥 Descargar Reporte Maestro (.xlsx)", out.getvalue(), "Resumen_XML.xlsx")

            # --- AI SMART ADVISOR RESTORED ---
            if api_key_valida:
                total_facturado = df_xml['Total a Pagar'].sum() if 'Total a Pagar' in df_xml.columns else 0
                render_smart_advisor(consultar_ia_gemini(f"Analiza este lote de facturas XML. Total facturado: {total_facturado}. Proveedores principales: {df_xml['Emisor'].unique()}"))

    elif menu == "Conciliación Bancaria IA":
        render_module_guide(
            get_text('title_bank'),
            "https://cdn-icons-png.flaticon.com/512/2489/2489756.png",
            get_text('desc_bank'),
            get_text('ben_bank')
        )
        
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
                for i, (idx_b, vb, fb, fecha_b_orig, desc_b) in enumerate(zip(df_banco.index, df_banco[col_valor_b], df_banco['Fecha_Dt'], df_banco[col_fecha_b], df_banco[col_desc_b])):
                    bar.progress((i+1)/total_rows)
                    cands = df_libro[
                        (df_libro[col_valor_l] == vb) & 
                        (~df_libro['Conciliado']) & 
                        (df_libro['Fecha_Dt'].between(fb - timedelta(days=3), fb + timedelta(days=3)))
                    ]
                    
                    if not cands.empty:
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
                
                with t1: st.dataframe(df_matches, use_container_width=True)
                with t2: st.dataframe(df_pend_banco, use_container_width=True)
                with t3: st.dataframe(df_pend_libro, use_container_width=True)

                # --- AI SMART ADVISOR RESTORED ---
                if api_key_valida:
                    with st.spinner("🤖 Analizando partidas pendientes..."):
                        render_smart_advisor(consultar_ia_gemini(f"Tengo {len(df_pend_banco)} partidas pendientes en bancos y {len(df_pend_libro)} en libros. ¿Qué me recomiendas revisar primero?"))

    elif menu == "Auditoría Fiscal de Gastos":
        st.markdown("""<div class='pro-module-header'><img src='https://cdn-icons-png.flaticon.com/512/1642/1642346.png' class='pro-module-icon'><div class='pro-module-title'><h2>Auditoría Fiscal Masiva (Art. 771-5)</h2></div></div>""", unsafe_allow_html=True)
        st.markdown("""<div class='detail-box'><strong>Objetivo:</strong> Verificar el cumplimiento de los requisitos de deducibilidad (Bancarización y Retenciones).<br>Detecta pagos en efectivo superiores a 100 UVT y bases de retención omitidas.</div>""", unsafe_allow_html=True)
        
        ar = st.file_uploader("Cargar Auxiliar de Gastos (.xlsx)", type=['xlsx'])
        
        if ar:
            df = pd.read_excel(ar)
            # ... (Existing Logic kept brief for length, assumig no changes needed in logic, just UI restoration)
            # Re-implementing logic for completeness as I am overwriting the file
            def detectar_idx(columnas, keywords):
                cols_str = [str(c).lower().strip() for c in columnas]
                for i, col in enumerate(cols_str):
                    for kw in keywords:
                        if kw in col: return i
                return 0

            kw_fecha = ['fecha', 'date', 'dia']
            kw_tercero = ['tercero', 'beneficiario', 'nombre', 'proveedor']
            kw_valor = ['valor', 'monto', 'importe', 'saldo', 'debito', 'total']
            kw_metodo = ['metodo', 'forma', 'pago', 'medio', 'banco', 'caja']
            kw_concepto = ['concepto', 'detalle', 'descripcion', 'nota']

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
                df['val_check_safe'] = pd.to_numeric(df[cv], errors='coerce').fillna(0)
                def wrapper_analisis(row):
                    return analizar_gasto_fila(row, cv, cm, cc)
                analisis_result = df.apply(wrapper_analisis, axis=1)
                df['Hallazgo_Temp'] = analisis_result.apply(lambda x: x[0])
                df['Riesgo_Temp'] = analisis_result.apply(lambda x: x[1])
                df_riesgos = df[df['Riesgo_Temp'] != "BAJO"].copy()
                
                st.divider()
                if df_riesgos.empty:
                    st.balloons()
                    st.success("✅ ¡Excelente! No se encontraron riesgos fiscales evidentes.")
                else:
                    st.warning(f"⚠️ Se encontraron {len(df_riesgos)} operaciones con riesgo fiscal.")
                    df_res = pd.DataFrame({
                        "Fecha": df_riesgos[cf].astype(str),
                        "Tercero": df_riesgos[ct].astype(str),
                        "Valor": df_riesgos['val_check_safe'].apply(lambda x: f"${x:,.0f}"),
                        "Método Pago": df_riesgos[cm].astype(str),
                        "Riesgo": df_riesgos['Riesgo_Temp'],
                        "Hallazgo": df_riesgos['Hallazgo_Temp']
                    })
                    st.dataframe(df_res, use_container_width=True)
                    
                    if api_key_valida:
                        with st.spinner("🤖 Analizando impacto tributario..."):
                             render_smart_advisor(consultar_ia_gemini(f"Como auditor, explica las consecuencias de tener {len(df_riesgos)} gastos rechazados por Art 771-5 (pago efectivo)."))

    # --------------------------------------------------------------------------
    # MÓDULO 1: ESCÁNER UGPP (LEY 1393 - REGLA DEL 40%)
    # --------------------------------------------------------------------------
    elif menu == "Escáner de Nómina (UGPP)":
        render_module_guide(
            get_text('title_ugpp'),
            "https://cdn-icons-png.flaticon.com/512/3135/3135817.png",
            get_text('desc_ugpp'),
            get_text('ben_ugpp')
        )
        
        an = st.file_uploader("Cargar Nómina UGPP (.xlsx)", type=['xlsx'], key="upl_ugpp")
        if an:
            dn = pd.read_excel(an)
            cols_todas = dn.columns.tolist()
            cols_numericas = dn.select_dtypes(include=['float64', 'int64']).columns.tolist()
            if not cols_numericas: cols_numericas = cols_todas

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
                opciones_ns = ["< No Aplica / Es $0 >"] + cols_numericas
                cns = c3.selectbox("Pagos No Salariales (Bonos/Auxilios)", opciones_ns, index=0, key="ugpp_ns")

            if st.button("▶️ ESCANEAR RIESGO UGPP", type="primary"):
                dn['salario_safe'] = pd.to_numeric(dn[cs], errors='coerce').fillna(0)
                if cns == "< No Aplica / Es $0 >":
                    dn['no_salarial_safe'] = 0.0
                else:
                    dn['no_salarial_safe'] = pd.to_numeric(dn[cns], errors='coerce').fillna(0)

                dn['total_rem'] = dn['salario_safe'] + dn['no_salarial_safe']
                dn['limite_40'] = dn['total_rem'] * 0.40
                dn['exceso'] = dn['no_salarial_safe'] - dn['limite_40']
                dn['exceso'] = dn['exceso'].clip(lower=0)
                dn['estado'] = dn['exceso'].apply(lambda x: "RIESGO ALTO" if x > 0 else "OK")

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

                    if api_key_valida:
                        with st.spinner("🤖 Calculando riesgo de sanción..."):
                            render_smart_advisor(consultar_ia_gemini(f"Analiza este riesgo UGPP. {len(riesgos)} empleados exceden el 40%. Total exceso: {dn['exceso'].sum()}. ¿Qué sanción aplica?"))

    elif menu == "Proyección de Tesorería":
        render_module_guide(
            get_text('title_treasury'),
            "https://cdn-icons-png.flaticon.com/512/5806/5806289.png",
            get_text('desc_treasury'),
            get_text('ben_treasury')
        )
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
                            render_smart_advisor(consultar_ia_gemini(f"Analiza este flujo de caja. Saldo inicial: {saldo_hoy}. Datos: {cal.head(10).to_string()}"))
                except: st.error("Error en el formato de fechas.")

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
        
        ac = st.file_uploader("Cargar Listado Personal (.xlsx)", type=['xlsx'])
        if ac:
            try:
                dc = pd.read_excel(ac)
                st.info("Configura las columnas (El sistema intenta detectarlas automáticamente):")
                
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
                
                c_arl = st.selectbox("5. Nivel ARL (Opcional - Si no seleccionas, asume Nivel 1)", ["No Aplica"] + cols)
                col_arl = c_arl if c_arl != "No Aplica" else None

                if st.button("▶️ CALCULAR DESGLOSE"):
                    rc = []
                    errores = 0
                    for r in dc.to_dict('records'):
                        try:
                            val_salario = float(r[cs])
                        except:
                            val_salario = 0
                            errores += 1

                        costo_total, total_seg, total_prest, paraf = calcular_costo_empresa_fila(r, cs, ca, col_arl, ce)
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

                    if api_key_valida:
                        with st.spinner("🤖 Analizando carga prestacional..."):
                             render_smart_advisor(consultar_ia_gemini(f"Analiza esta nómina. Total empleados: {len(rc)}. Costo total mensual: {sum([float(x['Costo Total Mensual'].replace('$','').replace(',','')) for x in rc])}. Da consejos de optimización."))

            except Exception as e:
                st.error(f"Error leyendo el archivo: {str(e)}. Revisa que el Excel no tenga filas vacías al inicio.")
    
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
        fi = st.file_uploader("Cargar Datos Financieros (.xlsx/.csv)", type=['xlsx', 'csv'])
        if fi and api_key_valida:
            df = pd.read_csv(fi) if fi.name.endswith('.csv') else pd.read_excel(fi)
            c1, c2 = st.columns(2); cd = c1.selectbox("Columna Descripción", df.columns); cv = c2.selectbox("Columna Valor", df.columns)
            if st.button("▶️ INICIAR ANÁLISIS IA"):
                res = df.groupby(cd)[cv].sum().sort_values(ascending=False).head(10); st.bar_chart(res)
                render_smart_advisor(consultar_ia_gemini(f"Actúa como auditor financiero. Analiza estos saldos principales y da recomendaciones: {res.to_string()}"))

    elif menu == "Narrador Financiero & NIIF":
        render_module_guide(
            get_text('title_narrator'),
            "https://cdn-icons-png.flaticon.com/512/3208/3208727.png",
            get_text('desc_narrator'),
            get_text('ben_narrator')
        )
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
                    render_smart_advisor(consultar_ia_gemini(prompt))

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
st.markdown("<center><strong>Asistente Contable Pro</strong> | Versión 1.0</center>", unsafe_allow_html=True)
