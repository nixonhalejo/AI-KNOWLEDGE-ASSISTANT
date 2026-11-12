# app/services/tools.py
import json

MAX_HOURS_PER_DAY = 24

_CONCEPTS = {
    "llm": "Modelo de lenguaje grande entrenado con grandes volúmenes de texto.",
    "rag": "Generación aumentada por recuperación: el modelo consulta documentos antes de responder.",
    "embedding": "Representación numérica de un texto que captura su significado.",
}


def tool_definitions() -> list[dict]:
    return [
        {
            "type": "function",
            "function": {
                "name": "lookup_ai_concept",
                "description": "Busca la definición de un concepto de IA.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "concept": {"type": "string", "description": "Concepto a buscar."}
                    },
                    "required": ["concept"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "calculate_study_hours",
                "description": "Calcula el total de horas de estudio.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "hours_per_day": {"type": "number"},
                        "days": {"type": "integer"},
                    },
                    "required": ["hours_per_day", "days"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "create_study_task",
                "description": "Crea una tarea de estudio.",
                "parameters": {
                    "type": "object",
                    "properties": {"title": {"type": "string"}},
                    "required": ["title"],
                },
            },
        },
    ]


def _lookup_ai_concept(args: dict) -> dict:
    concept = str(args["concept"]).strip().lower()
    definition = _CONCEPTS.get(concept)
    if definition is None:
        return {"error": "not_found"}
    return {"data": {"concept": concept, "definition": definition}}


def _calculate_study_hours(args: dict) -> dict:
    hours = float(args["hours_per_day"])
    days = int(args["days"])
    if not (0 < hours <= MAX_HOURS_PER_DAY) or days <= 0:
        return {"error": "invalid_arguments"}
    return {"data": {"total_hours": hours * days}}


def _create_study_task(args: dict, allow_write: bool) -> dict:
    if not allow_write:
        return {"error": "write_not_allowed"}
    title = str(args["title"]).strip()
    if not title:
        return {"error": "invalid_arguments"}
    return {"data": {"title": title, "status": "created"}}


def execute_tool(name: str, arguments: str, allow_write: bool = False) -> dict:
    handlers = {"lookup_ai_concept", "calculate_study_hours", "create_study_task"}
    if name not in handlers:
        return {"error": "unknown_tool"}

    try:
        args = json.loads(arguments)
        if not isinstance(args, dict):
            return {"error": "invalid_arguments"}

        if name == "lookup_ai_concept":
            return _lookup_ai_concept(args)
        if name == "calculate_study_hours":
            return _calculate_study_hours(args)
        return _create_study_task(args, allow_write)
    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        return {"error": "invalid_arguments"}