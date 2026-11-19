from fastapi import APIRouter

from app.provider.openrouter import OpenRouterProvider
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.assistance_service import AssistantService

router = APIRouter(prefix="/chat", tags=["chat"])

provider = OpenRouterProvider()
service = AssistantService(provider=provider)


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    # Pasamos el objeto 'request' completo para que el servicio tenga acceso 
    # a la pregunta, temperature, max_tokens, etc.
    answer = await service.ask(request=request)
    
    return ChatResponse(answer=answer, provider="openrouter")