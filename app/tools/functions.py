import math
from uuid import uuid4

from app.tools.schemas import ConceptArgs, EstimateEffortArgs, HoursArgs, TaskArgs

CONCEPTS = {
    "llm": "Modelo de lenguaje grande entrenado con enormes volúmenes de texto.",
    "rag": "Técnica donde el modelo consulta documentos antes de responder.",
    "embedding": "Representación numérica de un texto que captura su significado.",
}

TASKS: list[dict] = []

HOURS_PER_TOPIC = {"basico": 2, "intermedio": 4, "avanzado": 6}
LOW_EFFORT_MAX = 10
MEDIUM_EFFORT_MAX = 30


def lookup_ai_concept(args: ConceptArgs) -> dict:
    key = args.concept.strip().lower()
    definition = CONCEPTS.get(key, "Concepto no encontrado en la base interna.")
    return {"concept": key, "definition": definition}


def calculate_study_hours(args: HoursArgs) -> dict:
    return {"total_hours": round(args.hours_per_day * args.days, 2)}


def create_study_task(args: TaskArgs) -> dict:
    item = {
        "id": str(uuid4()),
        "title": args.title,
        "estimated_hours": args.estimated_hours,
    }
    TASKS.append(item)
    return item


def _effort_level(total_hours: int) -> str:
    if total_hours <= LOW_EFFORT_MAX:
        return "bajo"
    if total_hours <= MEDIUM_EFFORT_MAX:
        return "medio"
    return "alto"


def estimate_learning_effort(args: EstimateEffortArgs) -> dict:
    hours_per_topic = HOURS_PER_TOPIC[args.difficulty]
    total_hours = args.topics * hours_per_topic
    weeks = math.ceil(round(total_hours / args.weekly_hours, 6))
    level = _effort_level(total_hours)

    explanation = (
        f"{args.topics} temas x {hours_per_topic} h por tema "
        f"(dificultad {args.difficulty}) = {total_hours} h en total. "
        f"{total_hours} h / {args.weekly_hours:g} h por semana = "
        f"{weeks} semana(s), redondeando hacia arriba. "
        f"Esfuerzo {level}: bajo hasta {LOW_EFFORT_MAX} h, "
        f"medio hasta {MEDIUM_EFFORT_MAX} h, alto por encima."
    )

    return {
        "total_hours": total_hours,
        "weeks": weeks,
        "effort_level": level,
        "explanation": explanation,
    }