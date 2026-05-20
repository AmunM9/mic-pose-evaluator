from datetime import datetime

from pydantic import BaseModel


class RubricCriterionOut(BaseModel):
    id: int
    name: str
    description: str
    max_score: int

    model_config = {"from_attributes": True}


class RubricResultOut(BaseModel):
    id: int
    criterion_id: int
    score: float
    feedback: str
    criterion: RubricCriterionOut

    model_config = {"from_attributes": True}


class EvaluationListItem(BaseModel):
    id: int
    filename: str
    file_size_bytes: int
    overall_score: float | None
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class EvaluationDetail(BaseModel):
    id: int
    filename: str
    file_size_bytes: int
    transcript: str | None
    overall_score: float | None
    speaker_count: int
    status: str
    error_message: str | None
    created_at: datetime
    updated_at: datetime
    rubric_results: list[RubricResultOut]

    model_config = {"from_attributes": True}
