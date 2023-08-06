from sym.cli.helpers.updater import SymUpdater

from .symflow import symflow


@symflow.command(short_help="Update the Sym Flow CLI")
def update() -> None:
    SymUpdater().manual_update()
