import pytest

from app.schemas.chat import ChatRequest
from app.services.assistance_service import AssistanceService


@pytest.mark.asyncio
async def test_generate_response() -> None:
    service = AssistanceService()
    request = ChatRequest(question="¿Qué es FastAPI?")

    response = await service.generate_response(request)

    assert response.provider == "mock-ai-provider"
    assert "FastAPI" in response.answer