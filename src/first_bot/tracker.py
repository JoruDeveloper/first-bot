"""Detección de archivos ya procesados.

PASO 7: crea este módulo.
- get_unprocessed_files() -> list[Path]:
  lista los .xlsx/.xls/.csv de INPUT_PATH y excluye los que ya tienen
  su archivo resultado_*.csv en OUTPUT_PATH (compara nombres base).
"""


def get_unprocessed_files():
    """Retorna los archivos de entrada pendientes de procesar. Implementar."""
