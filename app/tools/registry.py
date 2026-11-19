from collections.abc import Callable
from dataclasses import dataclass

from pydantic import BaseModel, ValidationError

from app.tools import functions
from app.tools.schemas import ConceptArgs, EstimateEffortArgs, HoursArgs, TaskArgs


@dataclass(frozen=True)
class ToolSpec:
    name: str
    description: str
    args_model: type[BaseModel]
    handler: Callable
    requires_confirmation: bool = False


REGISTRY: dict[str, ToolSpec] = {
    spec.name: spec
    for spec in [
        ToolSpec(
            name="lookup_ai_concept",
            description="Busca la definición de un concepto de IA (por ejemplo LLM, RAG, embedding).",
            args_model=ConceptArgs,
            handler=functions.lookup_ai_concept,
        ),
        ToolSpec(
            name="calculate_study_hours",
            description="Calcula el total de horas de estudio a partir de horas por día y número de días.",
            args_model=HoursArgs,
            handler=functions.calculate_study_hours,
        ),
        ToolSpec(
            name="create_study_task",
            description="Crea una tarea de estudio con título y horas estimadas. Requiere confirmación del usuario.",
            args_model=TaskArgs,
            handler=functions.create_study_task,
            requires_confirmation=True,
        ),
        ToolSpec(
            name="estimate_learning_effort",
            description=(
                "Estima el esfuerzo para completar una actividad formativa: "
                "horas totales de estudio, semanas necesarias y nivel de esfuerzo "
                "(bajo, medio o alto), con la explicación del cálculo. "
                "Requiere la dificultad (basico, intermedio o avanzado), "
                "la cantidad de temas y las horas disponibles por semana. "
                "Si el usuario no indica alguno de estos datos, pídeselo antes de usar la herramienta."
            ),
            args_model=EstimateEffortArgs,
            handler=functions.estimate_learning_effort,
        ),
    ]
}


def tool_definitions() -> list[dict]:
    return [
        {
            "type": "function",
            "function": {
                "name": spec.name,
                "description": spec.description,
                "parameters": spec.args_model.model_json_schema(),
            },
        }
        for spec in REGISTRY.values()
    ]


def execute_tool(name: str, arguments: str, confirmed: bool = False) -> dict:
    spec = REGISTRY.get(name)
    if spec is None:
        return {"error": "unknown_tool"}

    try:
        args = spec.args_model.model_validate_json(arguments)
    except ValidationError:
        return {"error": "invalid_arguments"}

    if spec.requires_confirmation and not confirmed:
        return {"error": "confirmation_required"}

    return {"data": spec.handler(args)}