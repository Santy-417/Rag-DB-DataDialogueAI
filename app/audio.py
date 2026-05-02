import io
import tempfile
from openai import OpenAI
from gtts import gTTS
from .config import settings

_client = OpenAI(api_key=settings.OPENAI_API_KEY)


def transcribir_audio(audio_bytes: bytes) -> str:
    audio_buffer = io.BytesIO(audio_bytes)
    audio_buffer.name = "recording.wav"
    resultado = _client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_buffer,
        language="es",
    )
    return resultado.text.strip()


def texto_a_audio(texto: str) -> bytes:
    tts = gTTS(text=texto[:800], lang="es", slow=False)
    buf = io.BytesIO()
    tts.write_to_fp(buf)
    buf.seek(0)
    return buf.read()