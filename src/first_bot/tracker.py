from dataclasses import dataclass
from datetime import date
from pathlib import Path

from loguru import logger

import first_bot.config as cfg

EXTENSIONES = {".csv", ".xlsx"}


@dataclass(frozen=True, eq=False)
class ProcessableFileBase:
    """Base común para archivos procesables.

    Dos archivos son iguales si comparten ``path_dir`` (ruta relativa
    dentro de su directorio base), sin importar si uno es de entrada y
    el otro de salida.
    """

    year: int
    month: int
    day: int
    date: date
    path_dir: str
    full_path: Path

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ProcessableFileBase):
            return NotImplemented
        return self.path_dir == other.path_dir

    def __hash__(self) -> int:
        return hash(self.path_dir)

    @classmethod
    def from_path(cls, full_path: Path, base_dir: Path) -> "ProcessableFileBase":
        rel = full_path.relative_to(base_dir)
        parts = rel.parts
        if len(parts) < 4:
            raise ValueError(f"Ruta fuera del patrón YYYY/MM/DD/archivo: {rel}")
        year = int(parts[0])
        month = int(parts[1])
        day = int(parts[2])
        return cls(
            year=year,
            month=month,
            day=day,
            date=date(year, month, day),
            path_dir=rel.as_posix(),
            full_path=full_path.resolve(),
        )


@dataclass(frozen=True, eq=False)
class ProcessableInputFile(ProcessableFileBase):
    """Archivo de entrada dentro de INPUT_PATH/YYYY/MM/DD/..."""


@dataclass(frozen=True, eq=False)
class ProcessableOutputFile(ProcessableFileBase):
    """Archivo de salida dentro de OUTPUT_PATH/YYYY/MM/DD/..."""


def _collect(
    base_dir: Path, cls: type[ProcessableFileBase]
) -> set[ProcessableFileBase]:
    base = base_dir.resolve()
    if not base.exists():
        return set()
    files: set[ProcessableFileBase] = set()
    for p in base.rglob("*"):
        if not p.is_file():
            continue
        if p.suffix.lower() not in EXTENSIONES:
            continue
        try:
            files.add(cls.from_path(p, base))
        except (ValueError, IndexError) as e:
            logger.warning(f"Archivo ignorado (no cumple YYYY/MM/DD): {p} — {e}")
    return files


def get_unprocessed_files() -> list[ProcessableInputFile]:
    inputs = _collect(cfg.INPUT_PATH, ProcessableInputFile)
    outputs = _collect(cfg.OUTPUT_PATH, ProcessableOutputFile)
    pendientes = inputs - outputs
    return sorted(pendientes, key=lambda f: f.path_dir)
