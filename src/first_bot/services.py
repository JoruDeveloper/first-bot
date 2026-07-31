"""Lógica de negocio: validación, deduplicación y clasificación.

PASO 5: crea este módulo.
- validate(df) -> (validos: list[Solicitud], errores: list[dict]):
  convierte cada fila a Solicitud y captura errores de validación.
- deduplicate(validos, key="email") -> (unicos, duplicados):
  primera ocurrencia se mantiene, el resto se marca duplicado.
- classify(unicos, by="tipo_solicitud") -> dict[tipo, list[Solicitud]].
"""


def validate(df):
    """Valida cada fila del DataFrame. Implementar."""


def deduplicate(validos, key="email"):
    """Elimina solicitudes duplicadas por clave. Implementar."""


def classify(unicos, by="tipo_solicitud"):
    """Agrupa solicitudes por campo. Implementar."""
