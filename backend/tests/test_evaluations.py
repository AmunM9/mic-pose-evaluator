import io
from unittest.mock import AsyncMock, patch

import pytest

MOCK_TRANSCRIPT = "Hola, soy Juan de Mic&Pose. ¿En qué le puedo ayudar hoy?"
# transcribe_audio ahora retorna tuple[str, int]
MOCK_TRANSCRIBE_RETURN = (MOCK_TRANSCRIPT, 2)
MOCK_RESULTS = [
    {
        "criterion_id": i,
        "score": float(7 + i % 3),
        "feedback": f"Feedback para criterio {i}",
        "criterion_name": f"Criterio {i}",
        "criterion_description": f"Descripción {i}",
    }
    for i in range(1, 6)
]


@pytest.mark.asyncio
async def test_upload_audio_success(client):
    with (
        patch("app.routers.evaluations.transcribe_audio", new=AsyncMock(return_value=MOCK_TRANSCRIBE_RETURN)),
        patch("app.routers.evaluations.evaluate_transcript", new=AsyncMock(return_value=MOCK_RESULTS)),
    ):
        audio_bytes = io.BytesIO(b"fake audio content")
        response = await client.post(
            "/api/v1/evaluations/upload",
            files={"file": ("test.mp3", audio_bytes, "audio/mpeg")},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"
    assert data["transcript"] == MOCK_TRANSCRIPT
    assert data["overall_score"] is not None
    assert len(data["rubric_results"]) == 5


@pytest.mark.asyncio
async def test_upload_invalid_extension(client):
    response = await client.post(
        "/api/v1/evaluations/upload",
        files={"file": ("test.txt", b"contenido", "text/plain")},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_evaluations_empty(client):
    response = await client.get("/api/v1/evaluations")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_evaluation_detail(client):
    with (
        patch("app.routers.evaluations.transcribe_audio", new=AsyncMock(return_value=MOCK_TRANSCRIBE_RETURN)),
        patch("app.routers.evaluations.evaluate_transcript", new=AsyncMock(return_value=MOCK_RESULTS)),
    ):
        upload = await client.post(
            "/api/v1/evaluations/upload",
            files={"file": ("test.mp3", io.BytesIO(b"fake"), "audio/mpeg")},
        )
    eval_id = upload.json()["id"]

    response = await client.get(f"/api/v1/evaluations/{eval_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == eval_id
    assert len(data["rubric_results"]) == 5


@pytest.mark.asyncio
async def test_get_evaluation_not_found(client):
    response = await client.get("/api/v1/evaluations/99999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_evaluation(client):
    with (
        patch("app.routers.evaluations.transcribe_audio", new=AsyncMock(return_value=MOCK_TRANSCRIBE_RETURN)),
        patch("app.routers.evaluations.evaluate_transcript", new=AsyncMock(return_value=MOCK_RESULTS)),
    ):
        upload = await client.post(
            "/api/v1/evaluations/upload",
            files={"file": ("test.mp3", io.BytesIO(b"fake"), "audio/mpeg")},
        )
    eval_id = upload.json()["id"]

    delete_response = await client.delete(f"/api/v1/evaluations/{eval_id}")
    assert delete_response.status_code == 204

    get_response = await client.get(f"/api/v1/evaluations/{eval_id}")
    assert get_response.status_code == 404
