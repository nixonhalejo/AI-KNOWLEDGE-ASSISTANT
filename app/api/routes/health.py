from fastapi import APIRouter
from app.schemas.health import InfoResponse

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "ok"}

@router.get("/api/v1/info", response_model=InfoResponse)
async def get_info():
    return InfoResponse()