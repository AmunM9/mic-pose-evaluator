import io
import json

import openai

from app.config import settings

# Transcripción: whisper-1 — estable, WER <10% en español LATAM, soportado en SDK 1.58
# Diarización: gpt-4o-mini post-procesa el texto y asigna roles VENDEDOR/CLIENTE por contexto
# vs gpt-4o-transcribe-diarize + diarized_json: no soportado en SDK 1.58 (rechaza con Connection error)
_client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

_DIARIZE_SYSTEM = """Eres un experto en análisis de conversaciones de venta en español latinoamericano.
Recibirás la transcripción continua de una llamada comercial. Tu tarea es:
1. Identificar quién es el VENDEDOR (quien ofrece, presenta beneficios, cierra) y quién es el CLIENTE.
2. Reformatear el texto como un diálogo etiquetado, un turno por línea.
Responde ÚNICAMENTE con JSON válido, sin texto adicional."""

_DIARIZE_PROMPT = """Transcripción de la llamada:
---
{transcript}
---

Devuelve exactamente este JSON:
{{
  "lines": [
    {{"speaker": "VENDEDOR", "text": "..."}},
    {{"speaker": "CLIENTE", "text": "..."}}
  ],
  "speaker_count": <entero, número de participantes distintos identificados>
}}"""


async def transcribe_audio(filename: str, content: bytes) -> tuple[str, int]:
    """Retorna (transcript_formateado, numero_de_speakers).

    Paso 1 — whisper-1 convierte el audio a texto continuo.
    Paso 2 — gpt-4o-mini detecta roles (VENDEDOR/CLIENTE) y formatea como diálogo.
    Formato de salida: "VENDEDOR: texto\\nCLIENTE: texto\\n..."
    """
    transcription = await _client.audio.transcriptions.create(
        model="whisper-1",
        file=(filename, io.BytesIO(content)),
        language="es",
    )
    return await _diarize(transcription.text)


async def _diarize(transcript: str) -> tuple[str, int]:
    response = await _client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": _DIARIZE_SYSTEM},
            {"role": "user", "content": _DIARIZE_PROMPT.format(transcript=transcript)},
        ],
        temperature=0,
        response_format={"type": "json_object"},
    )

    data = json.loads(response.choices[0].message.content)
    lines: list[dict] = data.get("lines", [])
    speaker_count: int = int(data.get("speaker_count", 1))

    formatted = "\n".join(f"{line['speaker']}: {line['text']}" for line in lines)

    # Si GPT no pudo diarizar, devolver el texto original sin etiquetas
    if not formatted.strip():
        return transcript, 1

    return formatted, speaker_count
