import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


@pytest.mark.asyncio
async def test_transcribe_audio_mock():
    from app.services.transcription import transcribe_audio

    # Mock respuesta de Whisper
    mock_whisper = MagicMock()
    mock_whisper.text = "Hola, soy el vendedor."

    # Mock respuesta de GPT diarización
    mock_diarize_message = MagicMock()
    mock_diarize_message.content = json.dumps({
        "lines": [{"speaker": "VENDEDOR", "text": "Hola, soy el vendedor."}],
        "speaker_count": 1,
    })
    mock_diarize_choice = MagicMock()
    mock_diarize_choice.message = mock_diarize_message
    mock_diarize_response = MagicMock()
    mock_diarize_response.choices = [mock_diarize_choice]

    mock_client = AsyncMock()
    mock_client.audio.transcriptions.create = AsyncMock(return_value=mock_whisper)
    mock_client.chat.completions.create = AsyncMock(return_value=mock_diarize_response)

    with patch("app.services.transcription._client", mock_client):
        transcript, speaker_count = await transcribe_audio("test.mp3", b"fake audio")

    assert transcript == "VENDEDOR: Hola, soy el vendedor."
    assert speaker_count == 1
    mock_client.audio.transcriptions.create.assert_called_once()
    mock_client.chat.completions.create.assert_called_once()
    call_kwargs = mock_client.audio.transcriptions.create.call_args.kwargs
    assert call_kwargs["model"] == "whisper-1"
    assert call_kwargs["language"] == "es"


@pytest.mark.asyncio
async def test_evaluate_transcript_mock():
    from app.services.evaluation import evaluate_transcript

    mock_results = {
        "results": [
            {"criterion_id": i, "score": 8, "feedback": f"Buen desempeño en criterio {i}"}
            for i in range(1, 6)
        ]
    }

    mock_message = MagicMock()
    mock_message.content = json.dumps(mock_results)

    mock_choice = MagicMock()
    mock_choice.message = mock_message

    mock_response = MagicMock()
    mock_response.choices = [mock_choice]

    mock_client = AsyncMock()
    mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

    with patch("app.services.evaluation._client", mock_client):
        results = await evaluate_transcript("Transcripción de prueba")

    assert len(results) == 5
    assert all(r["score"] == 8.0 for r in results)
    assert all("criterion_name" in r for r in results)
    mock_client.chat.completions.create.assert_called_once()
    call_kwargs = mock_client.chat.completions.create.call_args.kwargs
    assert call_kwargs["model"] == "gpt-4o-mini"


@pytest.mark.asyncio
async def test_evaluate_transcript_invalid_json():
    from app.services.evaluation import evaluate_transcript

    mock_message = MagicMock()
    mock_message.content = "esto no es json"

    mock_choice = MagicMock()
    mock_choice.message = mock_message

    mock_response = MagicMock()
    mock_response.choices = [mock_choice]

    mock_client = AsyncMock()
    mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

    with patch("app.services.evaluation._client", mock_client):
        with pytest.raises(Exception):
            await evaluate_transcript("Transcripción de prueba")
