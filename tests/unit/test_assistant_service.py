from unittest.mock import AsyncMock
import pytest

from app.schemas.chat import ChatRequest
from app.services.assistance_service import AssistantService


@pytest.mark.asyncio
async def test_generate_response() -> None:
    # 1. Crear un proveedor falso (mock) que simule la IA
    mock_provider = AsyncMock()
    mock_provider.generate.return_value = "FastAPI es un marco web de alto rendimiento."

    # 2. Instanciar el servicio inyectándole el proveedor mock
    service = AssistantService(provider=mock_provider)
    request = ChatRequest(question="¿Qué es FastAPI?")

    # 3. Llamar al método ask() del servicio
    answer = await service.ask(question=request.question)

    # 4. Validar la respuesta devuelta por el mock
    assert "FastAPI" in answer
    mock_provider.generate.assert_called_once()