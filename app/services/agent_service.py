import json

from app.tools.registry import execute_tool, tool_definitions

SYSTEM_PROMPT = (
    "Eres un asistente de planificación académica. Usa las herramientas cuando "
    "ayuden a responder y no inventes cálculos. Si faltan datos para una "
    "herramienta, pídeselos al usuario. Explica brevemente cómo obtuviste el resultado."
)


class AgentService:
    MAX_STEPS = 5

    def __init__(self, provider) -> None:
        self.provider = provider

    async def run(
        self, question: str, confirmed: bool = False
    ) -> tuple[str, list[str]]:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ]
        tools_used: list[str] = []

        for _ in range(self.MAX_STEPS):
            reply = await self.provider.generate(
                messages=messages,
                tools=tool_definitions(),
                max_tokens=600,
            )
            calls = reply.get("tool_calls")

            if not calls:
                return reply.get("content") or "", tools_used

            messages.append(
                {
                    "role": "assistant",
                    "content": reply.get("content"),
                    "tool_calls": calls,
                }
            )

            for call in calls:
                name = call["function"]["name"]
                result = execute_tool(
                    name, call["function"]["arguments"], confirmed
                )
                tools_used.append(name)
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": call["id"],
                        "content": json.dumps(result, ensure_ascii=False),
                    }
                )

        return (
            "No pude completar la solicitud en el número máximo de pasos.",
            tools_used,
        )