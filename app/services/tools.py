# app/services/tools.py

# A. La función de Python real que se ejecutará en tu servidor
def consultar_base_interna(termino: str) -> str:
    """Busca datos internos de la empresa según el término indicado."""
    # Aquí puedes conectar luego tu lógica o base de datos real
    return f"Resultado interno encontrado para: '{termino}'"


# B. El esquema JSON que describe la herramienta para la IA
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
                        "description": "Concepto o palabra clave a buscar."
                    }
                },
                "required": ["termino"]
            }
        }
    }
]