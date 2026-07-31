"""Excepciones personalizadas del bot.

PASO 2: crea este módulo.
- Define una excepción base BotException.
- Hereda: FileReadError, ValidationFailedError, SubmissionError.
"""


class BotException(Exception):
    """Base exception del bot. Implementar."""
