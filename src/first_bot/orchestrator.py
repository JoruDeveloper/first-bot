"""Orquestador del pipeline.

PASO 10: crea este módulo.
- Orchestrator con método run().
- Orden: setup_logging -> get_unprocessed_files -> por archivo:
  leer -> validar -> deduplicar -> clasificar -> enviar -> guardar resultados.
- Usa loguru para registrar cada paso.
"""


class Orchestrator:
    """Coordina el pipeline completo. Implementar."""

    def run(self):
        """Ejecuta el proceso completo. Implementar."""
