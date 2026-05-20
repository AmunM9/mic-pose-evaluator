import logging
import os
import time
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.config import settings
from app.database import get_db
from app.models import Evaluation, RubricCriterion, RubricResult
from app.schemas import EvaluationDetail, EvaluationListItem
from app.services.evaluation import CRITERIA, evaluate_transcript
from app.services.transcription import transcribe_audio

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/evaluations", tags=["evaluations"])

ALLOWED_EXTENSIONS = {".mp3", ".wav", ".m4a", ".webm"}
UPLOAD_DIR = Path("/tmp/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def _validate_audio_file(file: UploadFile) -> None:
    ext = Path(file.filename or "").suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=422,
            detail=f"Formato no soportado: {ext}. Usa {', '.join(ALLOWED_EXTENSIONS)}",
        )


async def _ensure_criteria_exist(db: AsyncSession) -> dict[int, int]:
    """Crea los criterios de rúbrica si no existen. Retorna {criterion_id_local -> db_id}."""
    id_map = {}
    for c in CRITERIA:
        result = await db.execute(select(RubricCriterion).where(RubricCriterion.name == c["name"]))
        criterion = result.scalar_one_or_none()
        if not criterion:
            criterion = RubricCriterion(name=c["name"], description=c["description"], max_score=10)
            db.add(criterion)
            await db.flush()
        id_map[c["id"]] = criterion.id
    return id_map


@router.post(
    "/upload",
    response_model=EvaluationDetail,
    summary="Subir audio para evaluación",
    description="Recibe un archivo de audio, lo transcribe con Whisper y evalúa con GPT-4o-mini según la rúbrica comercial.",
    responses={422: {"description": "Formato inválido o archivo muy grande"}},
)
async def upload_audio(file: UploadFile, db: AsyncSession = Depends(get_db)):
    _validate_audio_file(file)

    content = await file.read()
    size_bytes = len(content)
    max_bytes = settings.MAX_AUDIO_SIZE_MB * 1024 * 1024
    if size_bytes > max_bytes:
        raise HTTPException(
            status_code=422,
            detail=f"El archivo supera el límite de {settings.MAX_AUDIO_SIZE_MB}MB",
        )

    safe_name = f"{uuid.uuid4()}{Path(file.filename or 'audio').suffix.lower()}"
    file_path = UPLOAD_DIR / safe_name
    file_path.write_bytes(content)

    evaluation = Evaluation(
        filename=file.filename or safe_name,
        file_size_bytes=size_bytes,
        status="processing",
    )
    db.add(evaluation)
    await db.flush()
    eval_id = evaluation.id
    start = time.monotonic()

    try:
        transcript, speaker_count = await transcribe_audio(str(file_path))
        evaluation.transcript = transcript
        evaluation.speaker_count = speaker_count

        criterion_id_map = await _ensure_criteria_exist(db)
        raw_results = await evaluate_transcript(transcript)

        scores = []
        for r in raw_results:
            db_criterion_id = criterion_id_map[r["criterion_id"]]
            rubric_result = RubricResult(
                evaluation_id=eval_id,
                criterion_id=db_criterion_id,
                score=r["score"],
                feedback=r["feedback"],
            )
            db.add(rubric_result)
            scores.append(r["score"])

        evaluation.overall_score = round(sum(scores) / len(scores), 2)
        evaluation.status = "completed"

    except Exception as exc:
        evaluation.status = "error"
        evaluation.error_message = str(exc)
        logger.error("evaluation_failed", extra={"evaluation_id": eval_id, "error": str(exc)})
        await db.commit()
        raise HTTPException(status_code=500, detail=f"Error procesando audio: {exc}") from exc
    finally:
        if file_path.exists():
            os.remove(file_path)

    await db.commit()

    duration_ms = int((time.monotonic() - start) * 1000)
    logger.info(
        "evaluation_completed",
        extra={
            "evaluation_id": eval_id,
            "audio_filename": file.filename,
            "duration_ms": duration_ms,
            "status": evaluation.status,
        },
    )

    result = await db.execute(
        select(Evaluation)
        .options(selectinload(Evaluation.rubric_results).selectinload(RubricResult.criterion))
        .where(Evaluation.id == eval_id)
    )
    return result.scalar_one()


@router.get(
    "",
    response_model=list[EvaluationListItem],
    summary="Listar evaluaciones",
    description="Retorna todas las evaluaciones ordenadas por fecha de creación descendente.",
)
async def list_evaluations(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Evaluation).order_by(Evaluation.created_at.desc()))
    return result.scalars().all()


@router.get(
    "/{evaluation_id}",
    response_model=EvaluationDetail,
    summary="Detalle de evaluación",
    description="Retorna la evaluación completa incluyendo transcripción y resultados por criterio.",
    responses={404: {"description": "Evaluación no encontrada"}},
)
async def get_evaluation(evaluation_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Evaluation)
        .options(selectinload(Evaluation.rubric_results).selectinload(RubricResult.criterion))
        .where(Evaluation.id == evaluation_id)
    )
    evaluation = result.scalar_one_or_none()
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")
    return evaluation


@router.delete(
    "/{evaluation_id}",
    status_code=204,
    summary="Eliminar evaluación",
    description="Elimina la evaluación y todos sus resultados asociados.",
    responses={404: {"description": "Evaluación no encontrada"}},
)
async def delete_evaluation(evaluation_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Evaluation).where(Evaluation.id == evaluation_id))
    evaluation = result.scalar_one_or_none()
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluación no encontrada")
    await db.delete(evaluation)
    await db.commit()
