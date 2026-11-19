import re


class GuardrailViolation(Exception):
    pass


class OutputGuardrailViolation(GuardrailViolation):
    pass


class GuardrailService:
    """
    Controles deterministas educativos.
    No sustituyen una moderación de seguridad avanzada.
    """

    _injection_patterns = (
        re.compile(
            r"\bignora\s+(?:todas\s+)?las\s+instrucciones\b",
            re.I,
        ),
        re.compile(
            r"\brevela\s+(?:la\s+)?(?:clave|api[ -]?key|contraseña)\b",
            re.I,
        ),
    )

    _secret_pattern = re.compile(
        r"\bOPENROUTER_API_KEY\s*[:=]\s*\S+"
        r"|\bsk-[A-Za-z0-9_-]{20,}",
        re.I,
    )

    def check_input(self, text: str) -> str:
        value = text.strip()

        if not value or len(value) > 2000:
            raise GuardrailViolation(
                "Entrada vacía o demasiado extensa"
            )

        if any(
            pattern.search(value)
            for pattern in self._injection_patterns
        ):
            raise GuardrailViolation(
                "Solicitud bloqueada por la política del laboratorio"
            )

        return value

    def check_output(self, text: str) -> str:
        if not text.strip():
            raise OutputGuardrailViolation(
                "El modelo devolvió una respuesta vacía"
            )

        if self._secret_pattern.search(text):
            raise OutputGuardrailViolation(
                "La respuesta contiene un posible secreto"
            )

        return text