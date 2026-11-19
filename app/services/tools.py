from app.tools.registry import execute_tool, tool_definitions

__all__ = [
    "execute_tool",
    "tool_definitions",
    "consultar_base_interna",
    "tools_disponibles",
]


# --- Código del módulo anterior, lo sigue usando AssistantService ---
def consultar_base_interna(termino: str) -> str:
    """Busca datos internos de la empresa según el término indicado."""
    return f"Resultado interno encontrado en la base de conocimiento para el término: '{termino}'"


tools_disponibles = [
    {
        "type": "function",
        "function": {
            "name": "consultar_base_interna",
            "description": "Busca datos específicos en la base de conocimiento interna de la empresa.",
            "parameters": {
                "type": "object",
                "properties": {
                    "termino": {
                        "type": "string",
                        "description": "Concepto o palabra clave a buscar.",
                    }
                },
                "required": ["termino"],
            },
        },
    }
]