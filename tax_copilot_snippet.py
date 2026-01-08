
# ==============================================================================
# COPILOTO TRIBUTARIO (CHATBOT FLOTANTE SIDEBAR)
# ==============================================================================
def render_tax_copilot():
    """
    Renderiza el asistente de IA en la barra lateral (siempre accesible).
    Usa las constantes 2026 definidas previamente.
    """
    with st.sidebar:
        st.markdown("---") # Separador visual
        
        # Estado del Chat (Persistencia)
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
            
        with st.expander("💬 Copiloto Tributario 2026", expanded=False):
            st.caption("🤖 Asistente Virtual | Normativa 2026")
            st.info("💡 Pregúntame sobre Retenciones, UVT, NIIF o Nómina.")
            
            # Contenedor de Historia (Scroll simulado)
            chat_container = st.container()
            with chat_container:
                for msg in st.session_state.chat_history:
                    with st.chat_message(msg["role"]):
                        st.markdown(msg["content"])
            
            # Zona de Input (Tipo Formulario para no recargar toda la app)
            with st.form(key="chat_form", clear_on_submit=True):
                user_input = st.text_input("Escribe tu consulta aquí...", placeholder="Ej: ¿Cuál es la base de retención por servicios?")
                submit_btn = st.form_submit_button("Enviar Consulta 🚀")
                
            if submit_btn and user_input:
                # 1. Mostrar usuario
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                
                # 2. Contexto 2026
                contexto_legal = f"""
                ACTÚA COMO UN EXPERTO CONTADOR Y ABOGADO TRIBUTARISTA DE COLOMBIA.
                TU FUENTE DE VERDAD ES LA NORMATIVA VIGENTE PARA EL AÑO FISCAL 2026.
                
                DATOS OFICIALES 2026:
                - SMMLV: ${SMMLV_2026:,.0f}
                - AUXILIO TRANSPORTE: ${AUX_TRANS_2026:,.0f}
                - UVT 2026: ${UVT_2026:,.0f}
                - BASE RETENCIÓN COMPRAS (27 UVT): ${BASE_RET_COMPRAS:,.0f}
                - BASE RETENCIÓN SERVICIOS (4 UVT): ${BASE_RET_SERVICIOS:,.0f}
                - TOPE BANCARIZACIÓN (100 UVT): ${TOPE_EFECTIVO:,.0f}
                
                INSTRUCCIÓN: Responde de forma clara, profesional y cita siempre la norma (Artículos ET, Decretos) si aplica.
                PREGUNTA DEL USUARIO: {user_input}
                """
                
                # 3. Llamada a Gemini
                try:
                    with st.spinner("Analizando..."):
                        respuesta = consultar_ia_gemini(contexto_legal)
                    
                    st.session_state.chat_history.append({"role": "assistant", "content": respuesta})
                    st.rerun() # Recargar para mostrar el mensaje
                except Exception as e:
                    st.error(f"Error IA: {str(e)}")

# Ejecutar el Chatbot al final para asegurar que todas las constantes están cargadas
render_tax_copilot()
