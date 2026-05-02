import streamlit as st
from streamlit_mic_recorder import mic_recorder
from app.rag_chain import consultar_bd
from app.audio import transcribir_audio, texto_a_audio

st.set_page_config(page_title="DataDialogue AI", page_icon="🏦", layout="wide")

st.markdown("""
<style>
    /* Fondo general */
    .stApp { background-color: #0f1117; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1a1d27;
        border-right: 1px solid #2d3147;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #1a1d27;
        border-radius: 12px;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 20px;
        color: #8b95b0;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: #3b5bdb !important;
        color: white !important;
    }

    /* Mensajes del chat */
    [data-testid="stChatMessage"] {
        border-radius: 12px;
        margin-bottom: 8px;
        padding: 4px 8px;
    }

    /* Botón principal */
    .stButton > button {
        background-color: #3b5bdb;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
        width: 100%;
        transition: background-color 0.2s;
    }
    .stButton > button:hover {
        background-color: #2f4ac7;
        color: white;
    }

    /* Input de chat */
    [data-testid="stChatInput"] textarea {
        border-radius: 12px !important;
        border: 1px solid #2d3147 !important;
        background-color: #1a1d27 !important;
    }

    /* Expanders */
    [data-testid="stExpander"] {
        border: 1px solid #2d3147;
        border-radius: 8px;
        background-color: #1a1d27;
    }

    /* Métricas en sidebar */
    [data-testid="stMetric"] {
        background-color: #0f1117;
        border-radius: 10px;
        padding: 12px;
        border: 1px solid #2d3147;
    }

    /* Info box */
    .stAlert {
        border-radius: 10px;
    }

    /* Título principal */
    h1 { color: #ffffff !important; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏦 DataDialogue AI")
    st.markdown("Sistema RAG de consultas bancarias en lenguaje natural.")
    st.divider()

    st.markdown("#### Preguntas de ejemplo")
    ejemplos = [
        "¿Qué clientes viven en Bogotá?",
        "¿Cuál es el saldo total de cuentas activas?",
        "¿Cuántos movimientos hubo en marzo de 2024?",
        "¿Qué cliente tiene más saldo?",
        "¿Cuántas cuentas corrientes hay?",
    ]
    for ej in ejemplos:
        if st.button(ej, key=ej):
            st.session_state.pregunta_rapida = ej

    st.divider()
    st.markdown("#### Base de datos")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Tablas", "4")
        st.metric("Clientes", "6")
    with col2:
        st.metric("Cuentas", "7")
        st.metric("Movimientos", "10")

    st.divider()
    if st.button("🗑️ Limpiar conversación"):
        st.session_state.mensajes = []
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
<div style="
    padding:0.75rem;
    background:linear-gradient(135deg,rgba(30,30,50,0.8),rgba(20,20,40,0.9));
    border:1px solid #2d3147;border-radius:8px;text-align:center;
">
    <div style="
        font-size:0.75rem;font-weight:700;letter-spacing:0.1em;
        background:linear-gradient(90deg,#6a7fd0,#a0b0ff);
        -webkit-background-clip:text;-webkit-text-fill-color:transparent;
        background-clip:text;margin-bottom:0.4rem;
    ">NEXTFLOW AI &copy; 2025</div>
    <div style="font-size:0.65rem;color:#8b95b0;line-height:1.8;">
        Santiago Chavarro Osorio<br>
        Samuel Aristizabal Botero<br>
        Santiago Andrés Giraldo Granada
    </div>
</div>
""", unsafe_allow_html=True)

# ── Estado ────────────────────────────────────────────────────────────────────
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []
if "pregunta_rapida" not in st.session_state:
    st.session_state.pregunta_rapida = None

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("## 💬 Chat bancario")
st.caption("Escribe o habla tu consulta y el sistema la traduce a SQL automáticamente.")
st.divider()

# ── Historial de mensajes ─────────────────────────────────────────────────────
for msg in st.session_state.mensajes:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sql"):
            with st.expander("🔍 Ver SQL generado"):
                st.code(msg["sql"], language="sql")
        if msg.get("tabla") is not None and not msg["tabla"].empty:
            with st.expander("📊 Ver tabla de resultados"):
                st.dataframe(msg["tabla"], width="stretch")
        if msg.get("audio_path"):
            st.audio(msg["audio_path"])

# ── Tabs de input ─────────────────────────────────────────────────────────────
tab_texto, tab_audio = st.tabs(["💬 Texto", "🎙️ Voz"])

def procesar_pregunta(pregunta: str, con_audio: bool = False):
    st.session_state.mensajes.append({"role": "user", "content": pregunta})
    with st.chat_message("user"):
        st.markdown(pregunta)

    with st.chat_message("assistant"):
        with st.spinner("Consultando base de datos..."):
            resultado = consultar_bd(pregunta)

        st.markdown(resultado["respuesta"])

        if resultado["sql"]:
            with st.expander("🔍 Ver SQL generado"):
                st.code(resultado["sql"], language="sql")
        if resultado["resultado"] is not None and not resultado["resultado"].empty:
            with st.expander("📊 Ver tabla de resultados"):
                st.dataframe(resultado["resultado"], width="stretch")

        if con_audio:
            with st.spinner("Generando respuesta en audio..."):
                try:
                    audio_bytes = texto_a_audio(resultado["respuesta"])
                    st.audio(audio_bytes, format="audio/mp3")
                except Exception:
                    pass

    st.session_state.mensajes.append({
        "role": "assistant",
        "content": resultado["respuesta"],
        "sql": resultado["sql"],
        "tabla": resultado["resultado"],
    })

with tab_texto:
    # Pregunta rápida desde sidebar
    if st.session_state.pregunta_rapida:
        pregunta_rapida = st.session_state.pregunta_rapida
        st.session_state.pregunta_rapida = None
        procesar_pregunta(pregunta_rapida)

    pregunta = st.chat_input("Escribe tu pregunta sobre el banco...")
    if pregunta:
        procesar_pregunta(pregunta)

with tab_audio:
    st.markdown("Graba tu pregunta directamente desde el navegador.")
    audio = mic_recorder(
        start_prompt="🔴 Iniciar grabación",
        stop_prompt="⏹️ Detener grabación",
        key="voice_recorder",
    )

    if audio and audio.get("bytes"):
        with st.spinner("Transcribiendo audio..."):
            try:
                pregunta_audio = transcribir_audio(audio["bytes"])
            except Exception as e:
                st.error(f"Error al transcribir: {e}")
                pregunta_audio = None

        if pregunta_audio:
            st.info(f"🎤 Pregunta detectada: **{pregunta_audio}**")
            procesar_pregunta(pregunta_audio, con_audio=True)
