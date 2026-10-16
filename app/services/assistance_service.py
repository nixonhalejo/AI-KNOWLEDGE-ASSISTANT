from app.provider.base import LLMProvider

SYSTEM_PROMPT = (
    "Eres un asistente de conocimiento empresarial especializado. "
    "Responde de forma clara, concisa y profesional."
)


class AssistantService:

    def __init__(self, provider: LLMProvider):
        self.provider = provider

    async def ask(
        self,
        question: str,
        temperature: float = 0.3,
        top_p: float = 1.0,
        max_tokens: int = 300,
    ) -> str:
        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": question,
            },
        ]

        return await self.provider.generate(
            messages=messages,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
        )