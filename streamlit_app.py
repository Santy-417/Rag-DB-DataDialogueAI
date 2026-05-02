import tempfile
import streamlit as st
from app.rag_chain import consultar_bd
from app.audio import transcribir_audio, texto_a_audio

st.set_page_config(page_title="DataDialogue AI", page_icon="🏦", layout="centered")

st.title("🏦 DataDialogue AI")
st.caption("Consulta la base de datos bancaria en lenguaje natural")

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

for msg in st.session_state.mensajes:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sql"):
            with st.expander("Ver SQL generado"):
                st.code(msg["sql"], language="sql")
        if msg.get("tabla") is not None and not msg["tabla"].empty:
            with st.expander("Ver tabla de resultados"):
                st.dataframe(msg["tabla"], use_container_width=True)
        if msg.get("audio_path"):
            st.audio(msg["audio_path"])

tab_texto, tab_audio = st.tabs(["💬 Texto", "🎙️ Audio"])

with tab_texto:
    pregunta = st.chat_input("Escribe tu pregunta sobre el banco...")
    if pregunta:
        st.session_state.mensajes.append({"role": "user", "content": pregunta})
        with st.chat_message("user"):
            st.markdown(pregunta)

        with st.chat_message("assistant"):
            with st.spinner("Consultando..."):
                resultado = consultar_bd(pregunta)
            st.markdown(resultado["respuesta"])
            if resultado["sql"]:
                with st.expander("Ver SQL generado"):
                    st.code(resultado["sql"], language="sql")
            if resultado["resultado"] is not None and not resultado["resultado"].empty:
                with st.expander("Ver tabla de resultados"):
                    st.dataframe(resultado["resultado"], use_container_width=True)

        st.session_state.mensajes.append({
            "role": "assistant",
            "content": resultado["respuesta"],
            "sql": resultado["sql"],
            "tabla": resultado["resultado"],
        })

with tab_audio:
    st.markdown("Sube un archivo de audio con tu pregunta (mp3, wav, m4a).")
    archivo_audio = st.file_uploader("Subir audio", type=["mp3", "wav", "m4a", "ogg"])

    if archivo_audio and st.button("Transcribir y consultar"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{archivo_audio.name.split('.')[-1]}") as tmp:
            tmp.write(archivo_audio.read())
            ruta_tmp = tmp.name

        with st.spinner("Transcribiendo audio..."):
            try:
                pregunta_audio = transcribir_audio(ruta_tmp)
            except Exception as e:
                st.error(f"Error al transcribir: {e}")
                pregunta_audio = None

        if pregunta_audio:
            st.info(f"Pregunta detectada: **{pregunta_audio}**")
            st.session_state.mensajes.append({"role": "user", "content": pregunta_audio})

            with st.spinner("Consultando base de datos..."):
                resultado = consultar_bd(pregunta_audio)

            with st.spinner("Generando respuesta en audio..."):
                try:
                    ruta_respuesta = texto_a_audio(resultado["respuesta"])
                except Exception:
                    ruta_respuesta = None

            st.markdown(f"**Respuesta:** {resultado['respuesta']}")
            if resultado["sql"]:
                with st.expander("Ver SQL generado"):
                    st.code(resultado["sql"], language="sql")
            if resultado["resultado"] is not None and not resultado["resultado"].empty:
                with st.expander("Ver tabla de resultados"):
                    st.dataframe(resultado["resultado"], use_container_width=True)
            if ruta_respuesta:
                st.audio(ruta_respuesta)

            st.session_state.mensajes.append({
                "role": "assistant",
                "content": resultado["respuesta"],
                "sql": resultado["sql"],
                "tabla": resultado["resultado"],
                "audio_path": ruta_respuesta,
            })
