import streamlit as st
import pandas as pd
import io
from datetime import datetime
import google.generativeai as genai
import time

# ==============================================================================
# 1. CONFIGURACIÓN DE PÁGINA (OBLIGATORIO AL PRINCIPIO)
# ==============================================================================
st.set_page_config(
    page_title="Suite Financiera Pro",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. INYECCIÓN DE ESTILOS CSS PREMIUM (TU DISEÑO MAQUILLADO)
# ==============================================================================
st.markdown("""
    <style>
        /* Importar tipografía moderna 'Inter' */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        /* Aplicar tipografía global */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            color: #1e293b; 
        }

        /* --- MEJORA DE LA BARRA LATERAL --- */
        [data-testid="stSidebar"] {
            background-color: #f8fafc;
            border-right: 1px solid #e2e8f0;
        }
        
        /* Tarjeta de Perfil en Sidebar */
        .profile-card {
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            margin-bottom: 20px;
            border-left: 5px solid #cbd5e1;
            transition: transform 0.2s;
        }
        .profile-card:hover {
            transform: translateY(-2px);
        }
        .profile-card.pro { border-left-color: #F59E0B; } /* Dorado */
        .profile-card.free { border-left-color: #64748b; } /* Gris */
        
        /* Botones del menú de navegación (Radio Buttons disfrazados) */
        .stRadio > div[role="radiogroup"] > label {
            background: white;
            padding: 12px 15px;
            border-radius: 8px;
            margin-bottom: 8px;
            border: 1px solid #e2e8f0;
            transition: all 0.2s;
            cursor: pointer;
            font-weight: 500;
            color: #475569;
        }
        .stRadio > div[role="radiogroup"] > label:hover {
            background: #f1f5f9;
            border-color: #cbd5e1;
            color: #0f172a;
            padding-left: 20px; /* Efecto de desplazamiento */
        }
        /* Ocultar círculos de radio buttons */
        .stRadio div[role="radiogroup"] label div:first-child {
            display: none;
        }

        /* --- MEJORA DE ELEMENTOS PRINCIPALES --- */
        h1, h2, h3 {
            color: #0f172a;
            font-weight: 700;
            letter-spacing: -0.025em;
        }
        
        /* Contenedores de métricas */
        [data-testid="stMetricValue"] {
            font-size: 1.8rem !important;
            font-weight: 700 !important;
            color: #2563eb;
        }

        /* Botones Primarios (Azules) */
        .stButton > button {
            width: 100%;
            border-radius: 8px;
            font-weight: 600;
            height: 3em;
        }

        /* Estilo específico para el Paywall */
        .paywall-container {
            margin-top: 20px; 
            padding: 30px; 
            border-radius: 16px; 
            border: 1px solid #334155; 
            background: radial-gradient(circle at center, #1e293b 0%, #0f172a 100%); 
            text-align: center; 
            position: relative; 
            overflow: hidden;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        }
        
        .blur-content {
            filter: blur(8px); 
            opacity: 0.4; 
            user-select: none;
            color: #94a3b8;
        }

        .cta-button {
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
            color: white !important;
            padding: 15px 35px;
            border-radius: 50px;
            text-decoration: none;
            font-weight: bold;
            box-shadow: 0 0 20px rgba(37, 99, 235, 0.5);
            display: inline-block;
            margin-top: 20px;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .cta-button:hover {
            transform: scale(1.05);
            box-shadow: 0 0 30px rgba(37, 99, 235, 0.7);
        }

    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. LÓGICA DE NEGOCIO Y CONFIGURACIÓN (Backend)
# ==============================================================================

# Configuración silenciosa de la IA (Secrets)
try:
    if "general" in st.secrets:
        # Aquí lee la clave que guardaste en secrets.toml
        GOOGLE_API_KEY = st.secrets["general"]["api_key_google"]
        genai.configure(api_key=GOOGLE_API_KEY)
        estado_ia_global = True
    else:
        estado_ia_global = False
except Exception:
    estado_ia_global = False

# Inicializar variables de sesión (Login)
if 'user_plan' not in st.session_state:
    st.session_state['user_plan'] = 'FREE'
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# ==============================================================================
# 4. BARRA LATERAL (SIDEBAR) - NUEVO DISEÑO
# ==============================================================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2830/2830303.png", width=60)
    st.markdown("### 💼 Suite Financiera")
    st.markdown("---")
    
    # --- SISTEMA DE LOGIN ---
    if not st.session_state.get('logged_in', False):
        st.info("🔒 Acceso Seguro")
        with st.expander("Ingresar a tu Cuenta", expanded=True):
            u = st.text_input("Usuario")
            p = st.text_input("Contraseña", type="password")
            if st.button("Iniciar Sesión", type="primary"):
                # VALIDACIÓN
                if u == "admin" and p == "admin": 
                    st.session_state['user_plan'] = 'PRO'
                    st.session_state['logged_in'] = True
                    st.rerun()
                elif u == "cliente": # Cliente genérico
                    st.session_state['user_plan'] = 'FREE'
                    st.session_state['logged_in'] = True
                    st.rerun()
                else:
                    st.error("❌ Credenciales incorrectas")
    
    # --- PERFIL DE USUARIO LOGUEADO (Diseño CSS Aplicado) ---
    else:
        # Determinamos clase CSS según plan
        plan_css = "pro" if st.session_state['user_plan'] == 'PRO' else "free"
        icono_ia = "🟢" if estado_ia_global else "🔴"
        txt_ia = "IA Conectada" if estado_ia_global else "IA Offline"
        
        # HTML Inyectado con clases CSS
        st.markdown(f"""
        <div class='profile-card {plan_css}'>
            <small style='color: #64748b; text-transform: uppercase; font-size: 0.7rem; font-weight: 700;'>Bienvenido de nuevo</small><br>
            <div style='margin-top: 5px; margin-bottom: 8px;'>
                <strong style='font-size: 1.1rem; color: #0f172a;'>Usuario {st.session_state['user_plan']}</strong>
            </div>
            <div style='display: flex; align-items: center; gap: 5px; font-size: 0.85rem;'>
                <span>{icono_ia}</span> <span style='color: #475569;'>{txt_ia}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state['user_plan'] == 'FREE':
            if st.button("💎 ACTUALIZAR A PRO"):
                st.toast("Redirigiendo a pasarela de pagos...")

        if st.button("Cerrar Sesión"):
            st.session_state['logged_in'] = False
            st.rerun()

    st.markdown("---")
    
    # --- MENÚ DE NAVEGACIÓN ---
    opciones_menu = [
        "Inicio / Dashboard",
        "Auditoría Cruce DIAN",
        "Minería de XML (Facturación)",
        "Conciliación Bancaria IA",
        "Analítica Financiera",
        "Reportes NIIF"
    ]
    
    if not st.session_state.get('logged_in', False):
        menu = "Inicio / Dashboard"
    else:
        st.caption("MÓDULOS OPERATIVOS")
        menu = st.radio("Navegación", opciones_menu, label_visibility="collapsed")
    
    st.markdown("<br><center><small style='color: #94a3b8;'>v14.2 Enterprise Edition</small></center>", unsafe_allow_html=True)

# ==============================================================================
# 5. ÁREA PRINCIPAL (CONTENIDO)
# ==============================================================================

# PANTALLA DE INICIO (DASHBOARD)
if menu == "Inicio / Dashboard":
    st.title("Panel de Control Financiero")
    st.markdown("Bienvenido a la plataforma de inteligencia contable.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style="background:white; padding:20px; border-radius:10px; border:1px solid #e2e8f0;">
            <h4 style="margin:0; color:#64748b;">Documentos Procesados</h4>
            <h2 style="margin:0; color:#0f172a;">1,248</h2>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="background:white; padding:20px; border-radius:10px; border:1px solid #e2e8f0;">
            <h4 style="margin:0; color:#64748b;">Riesgos Detectados</h4>
            <h2 style="margin:0; color:#dc2626;">12</h2>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style="background:white; padding:20px; border-radius:10px; border:1px solid #e2e8f0;">
            <h4 style="margin:0; color:#64748b;">Ahorro Tributario</h4>
            <h2 style="margin:0; color:#16a34a;">$45M</h2>
        </div>
        """, unsafe_allow_html=True)
        
    st.info("👈 Selecciona un módulo en el menú lateral para comenzar.")

# MÓDULO ESTRELLA: AUDITORÍA DIAN
elif menu == "Auditoría Cruce DIAN":
    st.markdown("## 🛡️ Auditoría Fiscal (Cruce DIAN vs Contabilidad)")
    st.markdown("Detecta inconsistencias antes que la DIAN lo haga. Algoritmo de cruce matricial avanzado.")
    st.markdown("---")

    col_upload1, col_upload2 = st.columns(2)
    
    with col_upload1:
        st.markdown("#### 1. Archivo DIAN (Exógena)")
        file_dian = st.file_uploader("Sube el Excel descargado de la DIAN", type=['xlsx'], key="f1")
        
    with col_upload2:
        st.markdown("#### 2. Tu Contabilidad (Auxiliar)")
        file_conta = st.file_uploader("Sube tu auxiliar por tercero", type=['xlsx'], key="f2")
        
    if file_dian and file_conta:
        try:
            df_dian = pd.read_excel(file_dian)
            df_conta = pd.read_excel(file_conta)
            
            st.divider()
            st.success("✅ Archivos cargados correctamente. Configura las columnas para el cruce:")
            
            with st.container(border=True):
                c1, c2, c3, c4 = st.columns(4)
                nit_dian = c1.selectbox("Columna NIT (DIAN)", df_dian.columns)
                val_dian = c2.selectbox("Columna Valor (DIAN)", df_dian.columns)
                nit_conta = c3.selectbox("Columna NIT (Contabilidad)", df_conta.columns)
                val_conta = c4.selectbox("Columna Valor (Contabilidad)", df_conta.columns)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("▶️ EJECUTAR AUDITORÍA BLINDADA", type="primary"):
                # --- LÓGICA DE CÁLCULO (Blindada contra errores de nombres) ---
                dian_grouped = df_dian.groupby(nit_dian)[val_dian].sum().reset_index(name='Valor_DIAN')
                dian_grouped.rename(columns={nit_dian: 'NIT'}, inplace=True)

                conta_grouped = df_conta.groupby(nit_conta)[val_conta].sum().reset_index(name='Valor_Conta')
                conta_grouped.rename(columns={nit_conta: 'NIT'}, inplace=True)
                
                # Cruce
                cruce = pd.merge(dian_grouped, conta_grouped, on='NIT', how='outer').fillna(0)
                cruce['Diferencia'] = cruce['Valor_DIAN'] - cruce['Valor_Conta']
                
                # Filtrar solo errores materiales (> 1000 pesos)
                diferencias = cruce[abs(cruce['Diferencia']) > 1000].sort_values(by="Diferencia", ascending=False)
                
                total_riesgo = diferencias['Diferencia'].abs().sum()
                num_hallazgos = len(diferencias)
                
                # --- RESULTADOS ---
                st.markdown("### 🔍 Resultados del Escáner")
                
                if num_hallazgos == 0:
                    st.balloons()
                    st.success("✅ ¡Contabilidad Perfecta! No hay diferencias materiales.")
                else:
                    st.error(f"⚠️ Se detectaron {num_hallazgos} inconsistencias que requieren atención.")
                    
                    # Métricas grandes
                    m1, m2 = st.columns(2)
                    m1.metric("Riesgo Financiero Total", f"${total_riesgo:,.0f}")
                    m2.metric("Terceros con Error", f"{num_hallazgos}")
                    
                    st.divider()
                    
                    # --- LÓGICA DEL PAYWALL (VENTAS) ---
                    if st.session_state.get('user_plan') == 'FREE':
                        # 1. Mostrar poquito (Teaser)
                        st.markdown("#### 👁️ Vista Previa (Limitada)")
                        st.caption("Mostrando los 2 errores más críticos:")
                        st.dataframe(diferencias.head(2).style.format("{:,.0f}"), use_container_width=True)
                        
                        # 2. El Muro de Pago (Diseño Nuevo)
                        st.markdown(f"""
                        <div class="paywall-container">
                            <div class="blur-content">
                                <p>NIT: 900.xxx.xxx | Diferencia: $45.000.000 | CRÍTICO</p>
                                <p>NIT: 890.xxx.xxx | Diferencia: $12.500.000 | CRÍTICO</p>
                                <p>NIT: 860.xxx.xxx | Diferencia: $ 8.200.000 | MEDIO</p>
                                <p>NIT: 800.xxx.xxx | Diferencia: $ 1.500.000 | BAJO</p>
                                <p> + {num_hallazgos - 2} registros más ocultos...</p>
                            </div>
                            <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center; background: rgba(15, 23, 42, 0.6); backdrop-filter: blur(4px);">
                                <h2 style="color: #fff; text-shadow: 0 2px 4px rgba(0,0,0,0.5);">🔒 REPORTE COMPLETO BLOQUEADO</h2>
                                <p style="color: #e2e8f0; font-size: 1.1rem; max-width: 600px; margin-bottom: 5px;">
                                    Tienes <strong>{num_hallazgos} inconsistencias</strong> por valor de <strong>${total_riesgo:,.0f}</strong>.
                                </p>
                                <p style="color: #cbd5e1; font-size: 0.9rem;">Evita sanciones del Art. 651 ET.</p>
                                <a href="#" class="cta-button">
                                    🔓 DESBLOQUEAR AHORA POR $59.000
                                </a>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                    else:
                        # --- VISTA PRO (Usuario Pago) ---
                        st.success("💎 ACCESO VIP: Visualizando auditoría completa.")
                        st.dataframe(diferencias.style.format("{:,.0f}"), use_container_width=True)
                        
                        # Botón de Descarga Excel
                        buffer = io.BytesIO()
                        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                            diferencias.to_excel(writer, sheet_name='Errores_DIAN', index=False)
                            # Autoajustar columnas (opcional, visual)
                            worksheet = writer.sheets['Errores_DIAN']
                            for i, col in enumerate(diferencias.columns):
                                width = max(diferencias[col].astype(str).map(len).max(), len(col))
                                worksheet.set_column(i, i, width + 2)
                                
                        st.download_button(
                            label="📥 Descargar Reporte Oficial (.xlsx)",
                            data=buffer,
                            file_name=f"Auditoria_DIAN_{datetime.now().date()}.xlsx",
                            mime="application/vnd.ms-excel",
                            type="primary"
                        )

        except Exception as e:
            st.error(f"Hubo un error al procesar los archivos: {e}")
            st.warning("Asegúrate de seleccionar las columnas correctas que contienen números.")

# OTROS MÓDULOS (Placeholder)
else:
    st.info(f"🚧 El módulo **{menu}** está en construcción o mantenimiento.")
    st.markdown("Vuelve pronto para ver las nuevas funcionalidades de IA.")