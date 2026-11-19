import json

import pytest

from app.tools.registry import execute_tool, tool_definitions


def run_estimate(**kwargs):
    return execute_tool("estimate_learning_effort", json.dumps(kwargs), False)


# ---------- Pruebas originales ----------


def test_tools_exposed():
    names = {tool["function"]["name"] for tool in tool_definitions()}

    assert names == {
        "lookup_ai_concept",
        "calculate_study_hours",
        "create_study_task",
        "estimate_learning_effort",
    }


def test_calculation():
    result = execute_tool(
        "calculate_study_hours",
        json.dumps({"hours_per_day": 1.5, "days": 4}),
        False,
    )

    assert result["data"]["total_hours"] == 6


def test_invalid_args():
    invalid_range = execute_tool(
        "calculate_study_hours",
        json.dumps({"hours_per_day": 50, "days": 2}),
        False,
    )
    assert invalid_range["error"] == "invalid_arguments"

    invalid_json = execute_tool("calculate_study_hours", "not-json", False)
    assert invalid_json["error"] == "invalid_arguments"


def test_unknown_tool():
    result = execute_tool("run_shell", "{}", True)

    assert result["error"] == "unknown_tool"


# ---------- estimate_learning_effort: argumentos válidos ----------


def test_estimate_enunciado():
    result = run_estimate(difficulty="intermedio", topics=5, weekly_hours=5)

    assert result["data"]["total_hours"] == 20
    assert result["data"]["weeks"] == 4
    assert result["data"]["effort_level"] == "medio"
    assert "20 h" in result["data"]["explanation"]


def test_estimate_rounds_weeks_up():
    # 6 h / 4 h por semana = 1.5 -> 2 semanas
    result = run_estimate(difficulty="basico", topics=3, weekly_hours=4)

    assert result["data"]["total_hours"] == 6
    assert result["data"]["weeks"] == 2


def test_estimate_float_precision():
    # 42 / 2.8 da 15.000000000000002 en Python; sin round() saldrían 16 semanas
    result = run_estimate(difficulty="basico", topics=21, weekly_hours=2.8)

    assert result["data"]["total_hours"] == 42
    assert result["data"]["weeks"] == 15


# ---------- estimate_learning_effort: valores límite ----------


@pytest.mark.parametrize(
    "difficulty, topics, expected",
    [
        ("basico", 5, "bajo"),  # 10 h: último valor de bajo
        ("basico", 6, "medio"),  # 12 h: primer valor de medio
        ("avanzado", 5, "medio"),  # 30 h: último valor de medio
        ("intermedio", 8, "alto"),  # 32 h: primer valor de alto
    ],
)
def test_estimate_effort_boundaries(difficulty, topics, expected):
    result = run_estimate(difficulty=difficulty, topics=topics, weekly_hours=10)

    assert result["data"]["effort_level"] == expected


@pytest.mark.parametrize(
    "topics, weekly_hours",
    [
        (1, 0.5),  # mínimos permitidos
        (50, 40),  # máximos permitidos
    ],
)
def test_estimate_limit_values_are_valid(topics, weekly_hours):
    result = run_estimate(
        difficulty="avanzado", topics=topics, weekly_hours=weekly_hours
    )

    assert "data" in result


# ---------- estimate_learning_effort: argumentos inválidos ----------


@pytest.mark.parametrize(
    "payload",
    [
        {"difficulty": "intermedio", "topics": 0, "weekly_hours": 5},
        {"difficulty": "intermedio", "topics": 51, "weekly_hours": 5},
        {"difficulty": "intermedio", "topics": 5, "weekly_hours": 0},
        {"difficulty": "intermedio", "topics": 5, "weekly_hours": 41},
        {"difficulty": "experto", "topics": 5, "weekly_hours": 5},
        {"difficulty": "intermedio", "topics": 2.5, "weekly_hours": 5},
        {"topics": 5, "weekly_hours": 5},
    ],
)
def test_estimate_invalid_args(payload):
    result = execute_tool("estimate_learning_effort", json.dumps(payload), False)

    assert result["error"] == "invalid_arguments"


def test_estimate_invalid_json():
    result = execute_tool("estimate_learning_effort", "no-es-json", False)

    assert result["error"] == "invalid_arguments"