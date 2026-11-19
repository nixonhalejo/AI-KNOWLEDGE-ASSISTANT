from typing import Literal

from pydantic import BaseModel, Field


class ConceptArgs(BaseModel):
    concept: str = Field(min_length=2, max_length=60)


class HoursArgs(BaseModel):
    hours_per_day: float = Field(gt=0, le=24)
    days: int = Field(ge=1, le=365)


class TaskArgs(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    estimated_hours: float = Field(gt=0, le=200)

class EstimateEffortArgs(BaseModel):
    difficulty: Literal["basico", "intermedio", "avanzado"]
    topics: int = Field(ge=1, le=50)
    weekly_hours: float = Field(gt=0, le=40)