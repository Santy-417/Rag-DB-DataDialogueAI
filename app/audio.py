import os
import tempfile
import whisper
from gtts import gTTS

_modelo_whisper = None


def _get_whisper():
    global _modelo_whisper
    if _modelo_whisper is None:
        _modelo_whisper = whisper.load_model("base")
    return _modelo_whisper


def transcribir_audio(ruta_audio: str) -> str:
    modelo = _get_whisper()
    resultado = modelo.transcribe(ruta_audio, language="es")
    return resultado["text"].strip()


def texto_a_audio(texto: str) -> str:
    tts = gTTS(text=texto, lang="es")
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(tmp.name)
    return tmp.name
