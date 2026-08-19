import tempfile
from datetime import date
from pathlib import Path

import pytest

from first_bot.tracker import (
    ProcessableInputFile,
    ProcessableOutputFile,
    get_unprocessed_files,
)


@pytest.fixture
def tracker_env():
    with tempfile.TemporaryDirectory() as input_dir, tempfile.TemporaryDirectory() as output_dir:
        import first_bot.config as cfg
        old_input, old_output = cfg.INPUT_PATH, cfg.OUTPUT_PATH
        cfg.INPUT_PATH = Path(input_dir)
        cfg.OUTPUT_PATH = Path(output_dir)
        yield Path(input_dir), Path(output_dir)
        cfg.INPUT_PATH = old_input
        cfg.OUTPUT_PATH = old_output


def _fecha_dir(base: Path, rel: str) -> Path:
    d = base / rel
    d.mkdir(parents=True, exist_ok=True)
    return d


class TestDataclasses:
    def test_extrae_atributos_de_la_ruta(self, tracker_env):
        input_dir, _ = tracker_env
        f = input_dir / "2028" / "01" / "15" / "solicitudes.csv"
        f.parent.mkdir(parents=True, exist_ok=True)
        f.touch()

        obj = ProcessableInputFile.from_path(f, input_dir)

        assert obj.year == 2028
        assert obj.month == 1
        assert obj.day == 15
        assert obj.date == date(2028, 1, 15)
        assert obj.path_dir == "2028/01/15/solicitudes.csv"
        assert obj.full_path == f.resolve()

    def test_igualdad_input_output_misma_ruta(self):
        inp = ProcessableInputFile(
            2028, 1, 15, date(2028, 1, 15),
            "2028/01/15/a.csv", Path("/abs/in/2028/01/15/a.csv"),
        )
        out = ProcessableOutputFile(
            2028, 1, 15, date(2028, 1, 15),
            "2028/01/15/a.csv", Path("/abs/out/2028/01/15/a.csv"),
        )
        assert inp == out

    def test_hash_consistente_entre_input_output(self):
        inp = ProcessableInputFile(
            2028, 1, 15, date(2028, 1, 15),
            "2028/01/15/a.csv", Path("/abs/in/2028/01/15/a.csv"),
        )
        out = ProcessableOutputFile(
            2028, 1, 15, date(2028, 1, 15),
            "2028/01/15/a.csv", Path("/abs/out/2028/01/15/a.csv"),
        )
        assert hash(inp) == hash(out)

    def test_distinto_path_dir_no_es_igual(self):
        a = ProcessableInputFile(
            2028, 1, 15, date(2028, 1, 15),
            "2028/01/15/a.csv", Path("/abs/in/2028/01/15/a.csv"),
        )
        b = ProcessableOutputFile(
            2028, 1, 15, date(2028, 1, 15),
            "2028/01/15/b.csv", Path("/abs/out/2028/01/15/b.csv"),
        )
        assert a != b

    def test_diferencia_de_conjuntos_elimina_iguales(self):
        inp = ProcessableInputFile(
            2028, 1, 15, date(2028, 1, 15),
            "2028/01/15/a.csv", Path("/abs/in/2028/01/15/a.csv"),
        )
        out = ProcessableOutputFile(
            2028, 1, 15, date(2028, 1, 15),
            "2028/01/15/a.csv", Path("/abs/out/2028/01/15/a.csv"),
        )
        assert len({inp} - {out}) == 0


class TestGetUnprocessedFiles:
    def test_sin_archivos(self, tracker_env):
        assert get_unprocessed_files() == []

    def test_archivos_pendientes_sin_output(self, tracker_env):
        input_dir, _ = tracker_env
        _fecha_dir(input_dir, "2028/01/15")
        (input_dir / "2028/01/15/a.csv").touch()
        (input_dir / "2028/01/15/b.xlsx").touch()

        pendientes = get_unprocessed_files()

        assert len(pendientes) == 2

    def test_archivo_procesado_se_omite(self, tracker_env):
        input_dir, output_dir = tracker_env
        _fecha_dir(input_dir, "2028/01/15")
        _fecha_dir(output_dir, "2028/01/15")
        (input_dir / "2028/01/15/a.csv").touch()
        (input_dir / "2028/01/15/b.xlsx").touch()
        (output_dir / "2028/01/15/a.csv").touch()

        pendientes = get_unprocessed_files()

        assert len(pendientes) == 1
        assert pendientes[0].path_dir == "2028/01/15/b.xlsx"

    def test_ignora_extensiones_no_soportadas(self, tracker_env):
        input_dir, _ = tracker_env
        _fecha_dir(input_dir, "2028/01/15")
        (input_dir / "2028/01/15/nota.txt").touch()
        (input_dir / "2028/01/15/imagen.png").touch()
        (input_dir / "2028/01/15/valido.csv").touch()

        pendientes = get_unprocessed_files()

        assert len(pendientes) == 1
        assert pendientes[0].path_dir == "2028/01/15/valido.csv"

    def test_ignora_archivos_fuera_del_patron_fecha(self, tracker_env):
        input_dir, _ = tracker_env
        (input_dir / "plano.csv").touch()
        _fecha_dir(input_dir, "2028/01/15")
        (input_dir / "2028/01/15/valido.csv").touch()

        pendientes = get_unprocessed_files()

        assert len(pendientes) == 1
        assert pendientes[0].path_dir == "2028/01/15/valido.csv"
