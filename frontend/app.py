import streamlit as st
import requests

API_BASE = "http://127.0.0.1:8000"

st.title("Asistente de Proyectos - RAG + LLM")

# Input form
with st.form("query_form"):
    user_question = st.text_area("Escribe tu pregunta en lenguaje natural:", height=150)
    submitted = st.form_submit_button("Consultar")

if submitted:
    if not user_question.strip():
        st.warning("Por favor, escribe una pregunta.")
    else:
        with st.spinner("Consultando modelo..."):
            try:
                # Make the POST request to the FastAPI backend
                response = requests.post(f"{API_BASE}/api/queryNatural", json={"question": user_question})
                result = response.json()

                if "response" in result:
                    # Streamlit can render Markdown directly
                    st.markdown("### 📄 Resumen generado")
                    st.markdown(result["response"])
                else:
                    st.error(f"Error: {result.get('error', 'Respuesta inesperada')}")
            except Exception as e:
                st.error(f"No se pudo conectar con el backend: {e}")
