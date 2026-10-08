from fastapi import APIRouter, Depends

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.assistance_service import AssistanceService

router = APIRouter(tags=["chat"])


@router.post(
    "/chat",
    response_model=ChatResponse,
)
async def chat(
    request: ChatRequest,
    service: AssistanceService = Depends(AssistanceService),
) -> ChatResponse:
    return await service.generate_response(request)