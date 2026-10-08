from app.schemas.chat import ChatRequest, ChatResponse


class AssistanceService:

    async def generate_response(self, request: ChatRequest) -> ChatResponse:
        # Lógica simulada de asistente de IA
        simulated_answer = (
            f"Procesada la pregunta: '{request.question}'. "
            "Esta es una respuesta generada por el servicio de conocimiento."
        )
        return ChatResponse(
            answer=simulated_answer,
            provider="mock-ai-provider",
        )