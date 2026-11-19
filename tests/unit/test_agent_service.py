from unittest.mock import AsyncMock

from app.services.agent_service import AgentService


async def test_agent_executes_tool_then_answers():
    provider = AsyncMock()
    provider.generate.side_effect = [
        {
            "role": "assistant",
            "content": None,
            "tool_calls": [
                {
                    "id": "call_1",
                    "type": "function",
                    "function": {
                        "name": "calculate_study_hours",
                        "arguments": '{"hours_per_day": 1.5, "days": 4}',
                    },
                }
            ],
        },
        {"role": "assistant", "content": "Son 6 horas."},
    ]

    service = AgentService(provider=provider)
    answer, tools_used = await service.run("¿Cuántas horas son?")

    assert answer == "Son 6 horas."
    assert tools_used == ["calculate_study_hours"]
    assert provider.generate.await_count == 2


async def test_agent_stops_after_max_steps():
    provider = AsyncMock()
    provider.generate.return_value = {
        "role": "assistant",
        "content": None,
        "tool_calls": [
            {
                "id": "call_1",
                "type": "function",
                "function": {"name": "run_shell", "arguments": "{}"},
            }
        ],
    }

    service = AgentService(provider=provider)
    answer, _ = await service.run("pregunta cualquiera")

    assert "máximo de pasos" in answer
    assert provider.generate.await_count == AgentService.MAX_STEPS