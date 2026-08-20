Alumno: Guillermo Cedeño

# Asignación: Sistema de tracking por fechas con conjuntos

## Descripción de la tarea

El objetivo es reemplazar el mecanismo de seguimiento de archivos del bot por uno
basado en una jerarquía de directorios por fecha y en la diferencia de conjuntos.

Anteriormente el bot detectaba los archivos pendientes comparando los nombres de
los archivos planos de `data/input/` contra el prefijo `resultado_` en
`data/output/`. Ese enfoque es simple pero poco escalable.

La nueva solución organiza los archivos en directorios por fecha (`YYYY/MM/DD`) y
determina los pendientes calculando `entradas - salidas`.

## Estructura de directorios

```
data/input/
  2028/01/15/
    solicitudes_a.csv
    pedidos_b.xlsx
  2028/01/16/
    reclamos_c.csv

data/output/
  2028/01/15/
    solicitudes_a.csv
    pedidos_b.xlsx
  2028/01/16/
    (vacío → reclamos_c.csv está pendiente)
```

Los archivos de salida conservan el mismo nombre y la misma ruta relativa que los
de entrada. Si un archivo existe en ambas ramas con la misma ruta relativa, se
considera procesado.

## Implementación

### Clases `ProcessableInputFile` y `ProcessableOutputFile`

Ambas son `@dataclass(frozen=True)`, comparables entre sí e iguales si comparten
`path_dir` (ruta relativa dentro del directorio base), sin importar si una es de
entrada y la otra de salida.

| Atributo   | Tipo | Descripción                             |
| ---------- | ---- | --------------------------------------- |
| `year`     | int  | Año extraído de la ruta                 |
| `month`    | int  | Mes extraído de la ruta                 |
| `day`      | int  | Día extraído de la ruta                 |
| `date`     | date | Construido con `year`/`month`/`day`     |
| `path_dir` | str  | Ruta relativa desde el directorio base  |
| `full_path`| Path | Ruta absoluta real                      |

Implementan `__eq__` y `__hash__` en función de `path_dir`, lo que permite
comparar un objeto de entrada con uno de salida y usarlos en conjuntos.

### `get_unprocessed_files()`

Recorre recursivamente los directorios de entrada y de salida, crea objetos
`ProcessableInputFile` y `ProcessableOutputFile`, y devuelve los pendientes como
la diferencia de conjuntos `inputs - outputs`. Solo se consideran las extensiones
`.csv` y `.xlsx`.

### Cambios de integración

- `utils.output_filename()`: la salida refleja la ruta relativa del input
  (`OUTPUT_PATH / path_dir`), eliminando el prefijo `resultado_`.
- `reporter.guardar_resultados()`: escribe el resultado con la misma extensión del
  archivo de entrada (`.csv` o `.xlsx`).
- `orchestrator`: consume objetos `ProcessableInputFile`.
- `scripts/generate_input.py`: genera datos de prueba dentro de la estructura
  `YYYY/MM/DD`.

## Pruebas

Se reescribieron `tests/test_tracker.py` y `tests/test_orchestrator.py` y se
unificaron los imports de la suite al paquete `first_bot`.

Resultado: 48 pruebas superadas.

## Cómo ejecutar

```bash
pdm install                              # instala dependencias
pdm run python scripts/generate_input.py # genera datos de prueba
pdm run python -m src.first_bot.main     # ejecuta el bot
pdm run pytest tests/ -v                 # ejecuta las pruebas
```

## Herramientas utilizadas

El desarrollo se realizó con [opencode](https://opencode.ai) empleando una API
key privada de DeepSeek y el modelo DeepSeek V4 Pro.
