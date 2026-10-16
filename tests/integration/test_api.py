from unittest.mock import AsyncMock, patch
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@patch("app.api.routes.chat.service.ask", new_callable=AsyncMock)
def test_chat_endpoint(mock_ask):
    mock_ask.return_value = "FastAPI es un marco web de alto rendimiento."

    response = client.post(
        "/chat",
        json={"question": "¿Qué es FastAPI?"},
    )

    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert data["provider"] == "openrouter"
    assert "FastAPI" in data["answer"]