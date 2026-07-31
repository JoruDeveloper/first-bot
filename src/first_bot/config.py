"""Configuración del bot desde .env.

PASO 1: crea este módulo.
- Carga variables de entorno con python-dotenv.
- Expone INPUT_PATH, OUTPUT_PATH, WEB_FORM_URL, HEADLESS como constantes.
- Usa rutas relativas con defaults razonables.
"""


def leer_config():
    """Lee y expone la configuración desde .env. Implementar."""
