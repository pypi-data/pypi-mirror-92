from ..helpers.updater import SymUpdater
from .sym import sym


@sym.command(short_help="Update the Sym CLI")
def update() -> None:
    SymUpdater().manual_update()
