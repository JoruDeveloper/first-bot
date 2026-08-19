from pathlib import Path

import first_bot.config as cfg
from first_bot.tracker import ProcessableInputFile


def output_filename(input_file: ProcessableInputFile) -> Path:
    """Devuelve la ruta de salida reflejando la ruta relativa del input."""
    return cfg.OUTPUT_PATH / input_file.path_dir
