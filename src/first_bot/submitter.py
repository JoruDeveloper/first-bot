"""Envío de solicitudes al formulario web (Playwright).

PASO 6: crea este módulo.
- WebSubmitter con __init__(form_url, headless).
- submit(solicitudes) -> list[dict] con {identificador, resultado, error}.
- Ahora: stub que simula el registro.
- Después: Playwright sync abriendo navegador, navegando al form_url,
  llenando los campos de Persona y enviando una por una.
"""


class WebSubmitter:
    """Registra solicitudes en el formulario web. Implementar."""
