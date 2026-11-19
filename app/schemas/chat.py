from pydantic import BaseModel, ConfigDict, Field


class ChatRequest(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
    )

    question: str = Field(
        min_length=3,
        max_length=2000,
        examples=["¿Qué es FastAPI?"],
    )
    temperature: float = Field(default=0.3, ge=0.0, le=2.0, description="Temperatura del modelo (0.0 a 2.0)")
    top_p: float = Field(default=1.0, ge=0.0, le=1.0, description="Top P sampling")
    max_tokens: int = Field(default=300, ge=1, le=4000, description="Límite de tokens de salida")


class ChatResponse(BaseModel):
    answer: str
    provider: str