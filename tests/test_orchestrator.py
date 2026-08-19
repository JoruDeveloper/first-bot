import tempfile
from pathlib import Path

import pytest

from first_bot.orchestrator import Orchestrator

CSV_VALIDO = (
    "First Name,Last Name,Company Name,Role in Company,Address,Email,Phone Number,"
    "tipo_solicitud,fecha,prioridad,identificador,descripcion,estado\n"
    "Juan,Pérez,TechCorp,Developer,Calle 123,juan@example.com,+1-555-1234,"
    "soporte,2024-06-15,alta,SOL-001,Problema con el sistema,pendiente\n"
)


@pytest.fixture
def orch_env():
    with tempfile.TemporaryDirectory() as input_dir, tempfile.TemporaryDirectory() as output_dir:
        import first_bot.config as cfg
        old_input, old_output = cfg.INPUT_PATH, cfg.OUTPUT_PATH
        cfg.INPUT_PATH = Path(input_dir)
        cfg.OUTPUT_PATH = Path(output_dir)
        yield Path(input_dir), Path(output_dir)
        cfg.INPUT_PATH = old_input
        cfg.OUTPUT_PATH = old_output


def _copiar_csv(input_dir: Path) -> Path:
    dest_dir = input_dir / "2028" / "01" / "15"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / "valido.csv"
    dest.write_text(CSV_VALIDO, encoding="utf-8")
    return dest


def test_orchestrator_sin_archivos(orch_env):
    orch = Orchestrator()
    orch.run()


def test_orchestrator_procesa_csv_valido(orch_env):
    input_dir, output_dir = orch_env
    _copiar_csv(input_dir)

    orch = Orchestrator()
    orch.run()

    output_files = list(output_dir.rglob("*.csv"))
    assert len(output_files) == 1
    assert output_files[0].relative_to(output_dir).as_posix() == "2028/01/15/valido.csv"


def test_orchestrator_no_reprocesa(orch_env):
    input_dir, output_dir = orch_env
    _copiar_csv(input_dir)

    orch = Orchestrator()
    orch.run()

    output_count_before = len(list(output_dir.rglob("*.csv")))

    orch.run()

    output_count_after = len(list(output_dir.rglob("*.csv")))
    assert output_count_after == output_count_before
