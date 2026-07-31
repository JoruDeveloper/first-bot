# Template — Bot Procesador de Solicitudes (RPA)

Plantilla para construir el proyecto **poco a poco**. Cada módulo tiene su
docstring con el `PASO n` indicando qué implementar. El resultado final es el
bot completo de la rama `main`.

## Orden de construcción

| Paso | Módulo | Responsabilidad |
|------|--------|-----------------|
| 0 | `.env` + `pyproject.toml` | Configuración y dependencias |
| 1 | `config.py` | Leer `.env` (INPUT_PATH, OUTPUT_PATH, WEB_FORM_URL, HEADLESS) |
| 2 | `exceptions.py` | Excepciones personalizadas |
| 3 | `models.py` | `Persona` + `Solicitud` con Pydantic |
| 4 | `readers.py` | Strategy + Factory para CSV/XLSX |
| 5 | `services.py` | `validate`, `deduplicate`, `classify` |
| 6 | `submitter.py` | Envío web (stub → Playwright) |
| 7 | `tracker.py` | Detección de archivos ya procesados |
| 8 | `reporter.py` | CSV de salida + bitácora + resumen |
| 9 | `utils.py` | Helpers de ruta |
| 10 | `orchestrator.py` | Pipeline completo |
| 11 | `main.py` | Entrypoint |

Tras cada paso: escribe sus tests en `tests/` y corre `pytest tests/`.

## Dependencias

```bash
pip install pandas openpyxl "pydantic[email]" loguru python-dotenv playwright pytest pytest-cov
```

## Datos de prueba

Genera 20 filas en `data/input` (ver `scripts/generate_input.py` en la rama `main`).

## Columnas del archivo

```
First Name, Last Name, Company Name, Role in Company, Address,
Email, Phone Number, tipo_solicitud, fecha, prioridad,
identificador, descripcion, estado
```

## Reglas de negocio

- Validación con Pydantic (email RFC, prioridad alta/media/baja, estado pendiente/en_proceso/completada, fecha parseable).
- Deduplicación por `Email`.
- Clasificación por `tipo_solicitud`.
- Archivos con `resultado_*.csv` en output no se reprocesan.
