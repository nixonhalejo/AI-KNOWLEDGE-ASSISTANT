import httpx
from fastapi import APIRouter, HTTPException

from app.core.config import settings
from app.provider.openrouter import OpenRouterProvider
from app.schemas.agent import AgentChatRequest, AgentChatResponse
from app.services.agent_service import AgentService

router = APIRouter(prefix="/agent", tags=["agent"])

service = AgentService(provider=OpenRouterProvider())


@router.post("/chat", response_model=AgentChatResponse)
async def agent_chat(request: AgentChatRequest) -> AgentChatResponse:
    try:
        answer, tools_used = await service.run(
            question=request.question,
            confirmed=request.confirmed,
        )
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=502, detail="Error al comunicarse con el proveedor de IA"
        ) from exc

    return AgentChatResponse(
        answer=answer,
        model=settings.OPENROUTER_MODEL,
        tools_used=tools_used,
    )