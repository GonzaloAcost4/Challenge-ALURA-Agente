"""
Interfaz principal del Agente Inteligente - Streamlit.
Challenge Alura - Oracle Next Education.
"""
import streamlit as st
from pathlib import Path
import sys

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import validate_config, DATA_DIR, LLM_MODEL
from app.rag import ingest_documents, check_vector_store_exists
from app.agent import create_agent, ask_agent, get_memory
from app.utils import get_file_list, format_sources


# ─────────────────────────────────────────────────────────
# Configuración de la Página
# ─────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🤖 Agente Inteligente | Challenge Alura",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────
# CSS Personalizado
# ─────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Tipografía */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Header */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    }

    .main-header h1 {
        color: white;
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
    }

    .main-header p {
        color: rgba(255, 255, 255, 0.85);
        font-size: 1rem;
        margin: 0.5rem 0 0 0;
    }

    /* Status badges */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
    }

    .status-ready {
        background: rgba(16, 185, 129, 0.15);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }

    .status-warning {
        background: rgba(245, 158, 11, 0.15);
        color: #f59e0b;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e1e2e 0%, #2d2d44 100%);
    }

    section[data-testid="stSidebar"] .stMarkdown {
        color: #e2e8f0;
    }

    /* Info cards */
    .info-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 1.2rem;
        border-radius: 12px;
        border: 1px solid rgba(148, 163, 184, 0.1);
        margin-bottom: 1rem;
    }

    .info-card h4 {
        color: #93c5fd;
        margin: 0 0 0.5rem 0;
        font-size: 0.9rem;
    }

    .info-card p {
        color: #cbd5e1;
        margin: 0;
        font-size: 0.85rem;
    }

    /* Sources section */
    .sources-section {
        background: rgba(99, 102, 241, 0.08);
        padding: 0.8rem 1rem;
        border-radius: 8px;
        border-left: 3px solid #6366f1;
        margin-top: 0.5rem;
        font-size: 0.85rem;
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem 0 1rem 0;
        color: #64748b;
        font-size: 0.8rem;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────
# Funciones auxiliares de UI
# ─────────────────────────────────────────────────────────
def render_header():
    """Renderiza el header principal."""
    st.markdown("""
    <div class="main-header">
        <h1>🤖 Agente Inteligente</h1>
        <p>Asistente conversacional con base de conocimiento | Challenge Alura - Oracle ONE</p>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar():
    """Renderiza el sidebar con información y controles."""
    with st.sidebar:
        st.markdown("## 🧠 Panel de Control")
        st.markdown("---")

        # Estado de la base de conocimiento
        kb_exists = check_vector_store_exists()
        files = get_file_list(str(DATA_DIR), [".pdf"])

        st.markdown("### 📚 Base de Conocimiento")

        if kb_exists:
            st.markdown(
                '<span class="status-badge status-ready">● Indexada</span>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<span class="status-badge status-warning">● Sin indexar</span>',
                unsafe_allow_html=True,
            )

        # Lista de archivos
        if files:
            st.markdown(f"**{len(files)}** PDF(s) de formaciones:")
            for f in files:
                st.markdown(f"📄 `{f.name}`")
        else:
            st.info(
                "No hay archivos PDF en `data/knowledge_base/`.\n\n"
                "Coloca los documentos PDF del programa ONE AI FOR TECH."
            )

        st.markdown("---")

        # Botón de ingesta
        st.markdown("### ⚙️ Acciones")

        if st.button("🔄 Indexar Documentos", use_container_width=True, type="primary"):
            with st.spinner("Indexando documentos..."):
                try:
                    result = ingest_documents()
                    if result:
                        st.success("✅ Documentos indexados exitosamente")
                        st.rerun()
                    else:
                        st.warning("No se encontraron documentos para indexar")
                except Exception as e:
                    st.error(f"Error: {e}")

        if st.button("🗑️ Limpiar Conversación", use_container_width=True):
            st.session_state.messages = []
            st.session_state.memory = get_memory()
            if "chain" in st.session_state:
                del st.session_state["chain"]
            st.rerun()

        st.markdown("---")

        # Info del proyecto
        st.markdown("### ℹ️ Sobre el Proyecto")
        st.markdown("""
        <div class="info-card">
            <h4>🏫 Challenge Alura</h4>
            <p>Oracle Next Education (ONE) - AI for Tech</p>
        </div>
        <div class="info-card">
            <h4>🔧 Stack Tecnológico</h4>
            <p>Python · LangChain · Groq (Llama 3) · ChromaDB · Streamlit</p>
        </div>
        <div class="info-card">
            <h4>☁️ Despliegue</h4>
            <p>Oracle Cloud Infrastructure (OCI)</p>
        </div>
        """, unsafe_allow_html=True)


def init_session_state():
    """Inicializa el estado de la sesión."""
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "memory" not in st.session_state:
        st.session_state.memory = get_memory()

    if "chain" not in st.session_state:
        st.session_state.chain = None


def get_or_create_chain():
    """Obtiene o crea la cadena del agente."""
    if st.session_state.chain is None:
        try:
            st.session_state.chain = create_agent(memory=st.session_state.memory)
        except ValueError as e:
            return None, str(e)
        except Exception as e:
            return None, f"Error inicializando el agente: {e}"
    return st.session_state.chain, None


# ─────────────────────────────────────────────────────────
# App Principal
# ─────────────────────────────────────────────────────────
def main():
    """Función principal de la aplicación."""
    init_session_state()
    render_header()
    render_sidebar()

    # Validar configuración
    errors = validate_config()
    if errors:
        for error in errors:
            st.error(f"⚠️ {error}")
        st.stop()

    # Mensaje de bienvenida si no hay historial
    if not st.session_state.messages:
        st.markdown("""
        <div style="text-align: center; padding: 3rem 1rem;">
            <p style="font-size: 3rem; margin-bottom: 1rem;">🎓🤖</p>
            <h3 style="color: #e2e8f0; font-weight: 600;">¡Bienvenido al Asistente ONE AI FOR TECH!</h3>
            <p style="color: #94a3b8; max-width: 550px; margin: 0 auto;">
                Soy tu asistente inteligente para el programa <b>Oracle Next Education - AI for Tech (G10 2026)</b>.
                Puedo responder tus preguntas sobre el curso, sus etapas y sus formaciones especializadas. ¡Haceme una pregunta!
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Mostrar historial de mensajes
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar="🧑‍💻" if message["role"] == "user" else "🤖"):
            st.markdown(message["content"])
            if message.get("sources"):
                sources_text = format_sources(message["sources"])
                st.markdown(
                    f'<div class="sources-section">{sources_text}</div>',
                    unsafe_allow_html=True,
                )

    # Input del usuario
    if prompt := st.chat_input("Escribí tu pregunta aquí..."):
        # Agregar mensaje del usuario al historial
        st.session_state.messages.append({"role": "user", "content": prompt, "sources": []})

        # Mostrar mensaje del usuario
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(prompt)

        # Obtener respuesta del agente
        with st.chat_message("assistant", avatar="🤖"):
            chain, error = get_or_create_chain()

            if error:
                st.error(error)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"❌ {error}",
                    "sources": [],
                })
            else:
                with st.spinner("Pensando..."):
                    try:
                        result = ask_agent(chain, prompt)
                        answer = result["answer"]
                        sources = result["sources"]
                    except Exception as e:
                        error_str = str(e)
                        if "RESOURCE_EXHAUSTED" in error_str or "429" in error_str:
                            answer = (
                                "⏳ **Se excedió la cuota de la API.**\n\n"
                                f"El modelo `{LLM_MODEL}` alcanzó su límite. "
                                "Podés:\n"
                                "- Esperar unos segundos e intentar de nuevo\n"
                                "- Cambiar `LLM_MODEL` en tu archivo `.env` y reiniciar"
                            )
                        else:
                            answer = f"❌ Error al procesar tu pregunta: {e}"
                        sources = []

                # Mostrar la respuesta (fuera del spinner para que desaparezca)
                st.markdown(answer)
                if sources:
                    sources_text = format_sources(sources)
                    st.markdown(
                        f'<div class="sources-section">{sources_text}</div>',
                        unsafe_allow_html=True,
                    )

                # Guardar en el historial
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources,
                })

    # Footer
    st.markdown("""
    <div class="footer">
        Desarrollado con ❤️ para el Challenge Alura | Oracle Next Education (ONE) - AI for Tech
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
