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
    page_title="ONE AI FOR TECH — Agente Inteligente",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────
# CSS – Diseño profesional y sobrio
# ─────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Fuentes ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --ink-900: #10151b;
        --ink-800: #161c23;
        --ink-700: #1f2730;
        --ink-500: #3b4552;
        --ink-300: #7c8794;
        --paper: #161c23;
        --paper-surface: #1f2730;
        --text: #e7e9eb;
        --text-muted: #8b939d;
        --accent: #2f6f5e;
        --accent-strong: #3a8a72;
        --accent-tint: rgba(47,111,94,.15);
        --border-light: #2a323c;
        --border-dark: #2a323c;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        -webkit-font-smoothing: antialiased;
    }

    /* ── Ocultar branding Streamlit y botón de Deploy ── */
    #MainMenu, footer, [data-testid="stAppDeployButton"], .stDeployButton {
        display: none !important;
        visibility: hidden !important;
    }

    header[data-testid="stHeader"] {
        background: transparent !important;
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        height: 52px !important;
        pointer-events: none !important;
        z-index: 99999 !important;
    }

    /* Estilo del botón para expandir la barra lateral (cuando está oculta) */
    [data-testid="collapsedControl"] {
        visibility: visible !important;
        display: flex !important;
        pointer-events: auto !important;
        position: fixed !important;
        top: 10px !important;
        left: 14px !important;
        z-index: 100000 !important;
        background: var(--ink-900) !important;
        border: 1px solid var(--border-dark) !important;
        border-radius: 8px !important;
        margin: 0 !important;
        padding: 4px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.25) !important;
    }
    [data-testid="collapsedControl"] button {
        color: #e7e9eb !important;
        background: transparent !important;
        border: none !important;
    }
    [data-testid="collapsedControl"] svg {
        fill: #e7e9eb !important;
        color: #e7e9eb !important;
        stroke: #e7e9eb !important;
    }

    /* Estilo del botón de colapsar la barra lateral cuando está desplegada */
    [data-testid="stSidebarCollapseButton"] button {
        color: #e7e9eb !important;
        background: transparent !important;
    }
    [data-testid="stSidebarCollapseButton"] svg {
        fill: #e7e9eb !important;
        color: #e7e9eb !important;
        stroke: #e7e9eb !important;
    }

    /* ── Fondo general oscuro ── */
    .stApp {
        background: var(--ink-800) !important;
    }
    .main .block-container {
        background: var(--ink-800) !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        max-width: 100% !important;
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: var(--ink-900) !important;
        border-right: 1px solid var(--border-dark);
        width: 296px !important;
    }
    section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
        background: var(--ink-900) !important;
    }
    section[data-testid="stSidebar"] * {
        color: #e7e9eb !important;
    }
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown li {
        font-size: 12.5px;
        line-height: 1.4;
    }

    /* Sidebar brand */
    .brand-eyebrow {
        font-size: 11px;
        letter-spacing: .08em;
        text-transform: uppercase;
        color: var(--ink-300) !important;
        margin-bottom: 4px;
    }
    .brand-title {
        font-size: 16px;
        font-weight: 600;
        color: #fff !important;
    }
    .brand-sub {
        font-size: 12.5px;
        color: var(--ink-300) !important;
        margin-top: 2px;
    }

    /* Sidebar section headers */
    .kb-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 8px;
    }
    .kb-title {
        font-size: 13px;
        font-weight: 600;
        color: #fff !important;
    }

    /* Status pill */
    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        color: #8fd7c1 !important;
        background: rgba(47,111,94,.18);
        border: 1px solid rgba(47,111,94,.4);
        padding: 3px 9px;
        border-radius: 999px;
    }
    .status-dot {
        display: inline-block;
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #4fd8ab;
    }

    /* Document list item */
    .doc-item {
        display: flex;
        align-items: baseline;
        gap: 10px;
        padding: 8px 0;
        border-bottom: 1px solid var(--border-dark);
        font-size: 12.5px;
        line-height: 1.4;
    }
    .doc-item:last-child { border-bottom: none; }
    .doc-index {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        color: var(--ink-300) !important;
        flex-shrink: 0;
        width: 16px;
    }
    .doc-name {
        color: #e7e9eb !important;
        word-break: break-word;
    }

    /* Sidebar buttons */
    section[data-testid="stSidebar"] .stButton > button {
        font-family: 'Inter', sans-serif !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        padding: 10px 14px !important;
        border-radius: 8px !important;
        width: 100% !important;
        transition: all .15s ease !important;
    }
    section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background: var(--accent) !important;
        color: #fff !important;
        border: 1px solid transparent !important;
    }
    section[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
        background: var(--accent-strong) !important;
    }
    section[data-testid="stSidebar"] .stButton > button[kind="secondary"] {
        background: transparent !important;
        color: var(--ink-300) !important;
        border: 1px solid var(--border-dark) !important;
    }
    section[data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover {
        color: #fff !important;
        border-color: var(--ink-300) !important;
    }

    /* ── Topbar Centrada, Compacta y Alineada ── */
    .topbar {
        max-width: 900px;
        margin: 10px auto 16px auto !important;
        padding: 8px 18px;
        border-radius: 10px;
        border: 1px solid var(--border-dark);
        background: var(--ink-900);
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 4px 12px rgba(0,0,0,0.25);
    }
    .topbar-title {
        font-size: 13.5px;
        font-weight: 600;
        color: #fff;
    }
    .topbar-sub {
        font-size: 11.5px;
        color: var(--ink-300);
        margin-top: 1px;
    }
    .topbar-badge {
        font-family: 'JetBrains Mono', monospace;
        font-size: 10.5px;
        color: #8fd7c1;
        background: rgba(47,111,94,.18);
        border: 1px solid rgba(47,111,94,.4);
        padding: 3px 9px;
        border-radius: 999px;
    }

    /* ── Welcome ── */
    .welcome-container {
        max-width: 600px;
        margin: 80px auto 0;
        text-align: center;
    }
    .welcome-icon {
        width: 48px;
        height: 48px;
        margin: 0 auto 20px;
        border-radius: 10px;
        background: var(--accent-tint);
        display: flex;
        align-items: center;
        justify-content: center;
        color: var(--accent-strong);
        font-size: 22px;
    }
    .welcome-container h1 {
        font-size: 22px;
        font-weight: 600;
        margin: 0 0 10px;
        color: #fff;
    }
    .welcome-container p {
        font-size: 14px;
        color: var(--text-muted);
        line-height: 1.65;
        margin: 0 0 32px;
    }

    /* Suggestion chips (Streamlit buttons) */
    .main .stButton > button {
        font-family: 'Inter', sans-serif !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        color: var(--text) !important;
        background: var(--ink-700) !important;
        border: 1px solid var(--border-dark) !important;
        border-radius: 999px !important;
        padding: 10px 18px !important;
        transition: border-color .15s ease, background .15s ease !important;
    }
    .main .stButton > button:hover {
        border-color: var(--accent) !important;
        background: var(--accent-tint) !important;
    }

    /* ── Chat messages ── */
    [data-testid="stChatMessage"] {
        max-width: 900px;
        margin-left: auto;
        margin-right: auto;
        background: transparent !important;
        border: none !important;
        padding: 6px 16px !important;
    }

    /* User messages */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stMarkdownContainer"],
    [data-testid="stChatMessage"]:has(img[alt="user"]) [data-testid="stMarkdownContainer"] {
        background: var(--accent);
        color: #fff !important;
        padding: 12px 16px;
        border-radius: 12px;
        border-bottom-right-radius: 4px;
    }
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stMarkdownContainer"] p,
    [data-testid="stChatMessage"]:has(img[alt="user"]) [data-testid="stMarkdownContainer"] p {
        color: #fff !important;
        font-size: 14px;
        line-height: 1.55;
    }

    /* Assistant messages */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) [data-testid="stMarkdownContainer"],
    [data-testid="stChatMessage"]:has(img[alt="assistant"]) [data-testid="stMarkdownContainer"] {
        background: var(--ink-700);
        border: 1px solid var(--border-dark);
        padding: 12px 16px;
        border-radius: 12px;
        border-bottom-left-radius: 4px;
        color: var(--text);
    }
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) [data-testid="stMarkdownContainer"] p,
    [data-testid="stChatMessage"]:has(img[alt="assistant"]) [data-testid="stMarkdownContainer"] p {
        color: var(--text) !important;
        font-size: 14px;
        line-height: 1.6;
    }
    /* Lists, strong, etc inside assistant */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) [data-testid="stMarkdownContainer"] li,
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) [data-testid="stMarkdownContainer"] strong,
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) [data-testid="stMarkdownContainer"] em,
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) [data-testid="stMarkdownContainer"] td,
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) [data-testid="stMarkdownContainer"] th,
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) [data-testid="stMarkdownContainer"] h1,
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) [data-testid="stMarkdownContainer"] h2,
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) [data-testid="stMarkdownContainer"] h3 {
        color: var(--text) !important;
    }

    /* Sources section */
    .sources-section {
        background: var(--accent-tint);
        padding: 8px 12px;
        border-radius: 8px;
        border-left: 3px solid var(--accent);
        margin-top: 8px;
        font-size: 12px;
        color: #8fd7c1;
    }

    /* ── Chat input ── */
    [data-testid="stChatInput"] {
        max-width: 900px !important;
        margin: 0 auto !important;
    }
    [data-testid="stChatInput"] > div {
        background: var(--ink-700) !important;
        border-color: var(--border-dark) !important;
        border-radius: 12px !important;
    }
    [data-testid="stChatInput"] > div:focus-within {
        border-color: var(--accent) !important;
    }
    [data-testid="stChatInput"] textarea {
        font-family: 'Inter', sans-serif !important;
        font-size: 14px !important;
        color: var(--text) !important;
    }
    [data-testid="stChatInput"] textarea::placeholder {
        color: var(--ink-300) !important;
    }
    [data-testid="stChatInput"] button {
        background: var(--accent) !important;
        color: #fff !important;
    }

    /* ── Indicador de Carga Custom ── */
    @keyframes loader-spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    .loading-indicator {
        display: flex;
        align-items: center;
        gap: 10px;
        background: var(--ink-700);
        border: 1px solid var(--border-dark);
        padding: 10px 16px;
        border-radius: 12px;
        border-bottom-left-radius: 4px;
        max-width: fit-content;
    }
    .loading-indicator .loader-circle {
        width: 18px;
        height: 18px;
        border: 2.5px solid var(--border-dark);
        border-top-color: var(--accent-strong);
        border-radius: 50%;
        animation: loader-spin 0.7s linear infinite;
        flex-shrink: 0;
    }
    .loading-indicator .loader-text {
        color: var(--text-muted);
        font-size: 13.5px;
        margin: 0;
    }

    /* Ocultar spinner nativo de Streamlit */
    .stSpinner { display: none !important; }

    /* ── Footer ── */
    .app-footer {
        text-align: center;
        font-size: 11px;
        color: var(--ink-300);
        padding: 12px 0 8px;
    }

    /* ── Sidebar dividers ── */
    section[data-testid="stSidebar"] hr {
        border-color: var(--border-dark) !important;
    }

    /* ── Streamlit alerts override ── */
    .stAlert {
        max-width: 900px;
        margin-left: auto;
        margin-right: auto;
    }

    /* ── Tables inside chat ── */
    [data-testid="stChatMessage"] table {
        color: var(--text) !important;
    }
    [data-testid="stChatMessage"] table th,
    [data-testid="stChatMessage"] table td {
        border-color: var(--border-dark) !important;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────
# Funciones auxiliares de UI
# ─────────────────────────────────────────────────────────
def render_topbar(doc_count: int):
    """Renderiza la barra superior profesional."""
    st.markdown(f"""
    <div class="topbar">
        <div>
            <div class="topbar-title">Agente Inteligente</div>
            <div class="topbar-sub">Asistente conversacional con base de conocimiento</div>
        </div>
        <span class="topbar-badge">{doc_count} documentos</span>
    </div>
    """, unsafe_allow_html=True)


def export_chat_markdown(messages) -> str:
    """Genera un archivo Markdown con el historial de la conversación."""
    if not messages:
        return ""
    md = "# 🤖 Conversación — ONE AI FOR TECH (Challenge Alura)\n\n"
    md += "---\n\n"
    for msg in messages:
        role = "🧑‍💻 **Usuario**" if msg["role"] == "user" else "🤖 **Agente Inteligente**"
        md += f"### {role}\n\n{msg['content']}\n\n"
        if msg.get("sources"):
            sources_str = ", ".join(msg["sources"])
            md += f"_📚 Fuentes consultadas: {sources_str}_\n\n"
        md += "---\n\n"
    return md


def render_sidebar():
    """Renderiza el sidebar con diseño profesional."""
    with st.sidebar:
        # Brand
        st.markdown("""
        <div style="padding: 4px 0 12px;">
            <div class="brand-eyebrow">Challenge Alura · Oracle ONE</div>
            <div class="brand-title">ONE AI FOR TECH</div>
            <div class="brand-sub">Panel del agente — G10 2026</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        # Estado de la base de conocimiento
        kb_exists = check_vector_store_exists()
        files = get_file_list(str(DATA_DIR), [".pdf"])

        status_html = (
            '<span class="status-pill"><span class="status-dot"></span>indexada</span>'
            if kb_exists
            else '<span class="status-pill" style="color:#f59e0b !important;border-color:rgba(245,158,11,.4);background:rgba(245,158,11,.12);"><span class="status-dot" style="background:#f59e0b;"></span>sin indexar</span>'
        )
        st.markdown(f"""
        <div class="kb-header">
            <span class="kb-title">Base de conocimiento</span>
            {status_html}
        </div>
        """, unsafe_allow_html=True)

        # Lista de documentos
        if files:
            docs_html = ""
            for i, f in enumerate(sorted(files, key=lambda x: x.name), 1):
                docs_html += f"""
                <div class="doc-item">
                    <span class="doc-index">{str(i).zfill(2)}</span>
                    <span class="doc-name">{f.name}</span>
                </div>
                """
            st.markdown(docs_html, unsafe_allow_html=True)
        else:
            st.info("No hay archivos PDF en `data/knowledge_base/`.")

        st.markdown("---")

        # Botones de acción
        if st.button("⟳ Indexar documentos", use_container_width=True, type="primary"):
            with st.spinner("Indexando documentos..."):
                try:
                    result = ingest_documents()
                    if result:
                        st.success("Documentos indexados exitosamente")
                        st.rerun()
                    else:
                        st.warning("No se encontraron documentos para indexar")
                except Exception as e:
                    st.error(f"Error: {e}")

        # Guardar / Exportar conversación
        if st.session_state.get("messages"):
            chat_md = export_chat_markdown(st.session_state.messages)
            st.download_button(
                label="💾 Guardar conversación",
                data=chat_md,
                file_name="conversacion_one_ai.md",
                mime="text/markdown",
                use_container_width=True,
                type="secondary",
            )
        else:
            st.button(
                "💾 Guardar conversación",
                disabled=True,
                use_container_width=True,
                type="secondary",
                help="Se activará una vez que inicies la conversación.",
            )

        if st.button("Limpiar conversación", use_container_width=True, type="secondary"):
            st.session_state.messages = []
            st.session_state.memory = get_memory()
            if "chain" in st.session_state:
                del st.session_state["chain"]
            st.rerun()

        return files


def render_welcome():
    """Renderiza la pantalla de bienvenida con sugerencias."""
    st.markdown("""
    <div class="welcome-container">
        <div class="welcome-icon">✦</div>
        <h1>¿En qué puedo ayudarte?</h1>
        <p>
            Preguntame sobre el programa Oracle Next Education, sus etapas
            o cualquiera de las formaciones indexadas en la base de conocimiento.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Suggestion chips como botones de Streamlit
    cols = st.columns(3)
    suggestions = [
        "¿Qué etapas tiene el programa?",
        "Contame sobre RAG avanzado",
        "¿Qué es Oracle Cloud Infrastructure?",
    ]
    for i, suggestion in enumerate(suggestions):
        with cols[i]:
            if st.button(suggestion, key=f"chip_{i}", use_container_width=True):
                st.session_state.chip_clicked = suggestion
                st.rerun()


def init_session_state():
    """Inicializa el estado de la sesión."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "memory" not in st.session_state:
        st.session_state.memory = get_memory()
    if "chain" not in st.session_state:
        st.session_state.chain = None
    if "chip_clicked" not in st.session_state:
        st.session_state.chip_clicked = None


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


def process_question(prompt: str):
    """Procesa una pregunta del usuario y genera la respuesta."""
    st.session_state.messages.append({"role": "user", "content": prompt, "sources": []})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        chain, error = get_or_create_chain()

        if error:
            st.error(error)
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"Error: {error}",
                "sources": [],
            })
        else:
            # Indicador de carga HTML custom (reemplaza st.spinner)
            loading_placeholder = st.empty()
            loading_placeholder.markdown(
                '<div class="loading-indicator">'
                '<div class="loader-circle"></div>'
                '<span class="loader-text">Buscando en la base de conocimiento...</span>'
                '</div>',
                unsafe_allow_html=True,
            )

            try:
                result = ask_agent(chain, prompt)
                answer = result["answer"]
                sources = result["sources"]
            except Exception as e:
                error_str = str(e)
                if "RESOURCE_EXHAUSTED" in error_str or "429" in error_str:
                    answer = (
                        "**Se excedió la cuota de la API.**\n\n"
                        f"El modelo `{LLM_MODEL}` alcanzó su límite. "
                        "Podés esperar unos segundos e intentar de nuevo."
                    )
                else:
                    answer = f"Error al procesar tu pregunta: {e}"
                sources = []

            # Limpiar indicador de carga y mostrar respuesta
            loading_placeholder.empty()

            st.markdown(answer)
            if sources:
                sources_text = format_sources(sources)
                st.markdown(
                    f'<div class="sources-section">{sources_text}</div>',
                    unsafe_allow_html=True,
                )

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "sources": sources,
            })


# ─────────────────────────────────────────────────────────
# App Principal
# ─────────────────────────────────────────────────────────
def main():
    """Función principal de la aplicación."""
    init_session_state()
    files = render_sidebar()

    # Validar configuración
    errors = validate_config()
    if errors:
        for error in errors:
            st.error(f"⚠️ {error}")
        st.stop()

    # Topbar
    render_topbar(len(files) if files else 0)

    # Si se hizo clic en un chip de sugerencia, lo procesamos PRIMERO
    if st.session_state.chip_clicked:
        prompt = st.session_state.chip_clicked
        st.session_state.chip_clicked = None
        process_question(prompt)
        st.rerun()

    # Capturar prompt del chat input
    input_prompt = st.chat_input("Escribí tu pregunta...")

    # Renderizar pantalla de bienvenida (SOLO si no hay mensajes en el historial)
    if not st.session_state.messages:
        render_welcome()
    else:
        # Renderizar historial de mensajes
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if message.get("sources"):
                    sources_text = format_sources(message["sources"])
                    st.markdown(
                        f'<div class="sources-section">{sources_text}</div>',
                        unsafe_allow_html=True,
                    )

    # Si el usuario envió una pregunta desde el chat input
    if input_prompt:
        process_question(input_prompt)
        st.rerun()

    # Footer
    st.markdown("""
    <div class="app-footer">
        Desarrollado para el Challenge Alura · Oracle Next Education (ONE) — AI for Tech
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
