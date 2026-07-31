"""Lectura de archivos con pandas (patrón Strategy + Factory).

PASO 4: crea este módulo.
- BaseReader (ABC) con método abstracto read(filepath) -> DataFrame.
- CsvReader: pd.read_csv.
- XlsxReader: pd.read_excel(engine="openpyxl").
- reader_factory(extension) -> BaseReader según .csv/.xlsx/.xls.
- Lanza FileReadError si el archivo no se puede leer.
"""


class BaseReader:
    """Clase abstracta de lector de archivos. Implementar."""


def reader_factory(extension):
    """Retorna el lector según la extensión. Implementar."""
