"""Linha de comando do interlinear."""

from typing import Annotated

import typer

from interlinear import __version__

app = typer.Typer(add_completion=False, no_args_is_help=True)


def _mostrar_versao(pedida: bool) -> None:
    if pedida:
        typer.echo(f"interlinear {__version__}")
        raise typer.Exit()


@app.callback()
def principal(
    versao: Annotated[
        bool,
        typer.Option(
            "--version",
            help="Mostra a versão e sai.",
            callback=_mostrar_versao,
            is_eager=True,
        ),
    ] = False,
) -> None:
    """Gera edições interlineares de textos hebraicos e aramaicos como sites estáticos."""
