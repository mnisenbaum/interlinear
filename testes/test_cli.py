"""Testes da linha de comando."""

import tomllib
from pathlib import Path

from typer.testing import CliRunner

from interlinear.cli import app

PYPROJECT = Path(__file__).parent.parent / "pyproject.toml"


def test_version_mostra_a_versao_do_pyproject():
    versao = tomllib.loads(PYPROJECT.read_text(encoding="utf-8"))["project"]["version"]

    resultado = CliRunner().invoke(app, ["--version"])

    assert resultado.exit_code == 0
    assert resultado.output.strip() == f"interlinear {versao}"
