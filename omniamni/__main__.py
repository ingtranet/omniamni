import importlib
import os

import typer
import anyio

from omniamni.config import AppContext

app = typer.Typer()


def launch_app(module: str):
    target_module = importlib.import_module(f"omniamni.{module}")
    context = AppContext(
        port=os.environ.get('APP_PORT', 8910)
    )

    if hasattr(target_module, 'start'):
        anyio.run(target_module.start, context)
    else:
        raise RuntimeError(f"Module {app} does not have a start function")


@app.command()
def main(module: str = typer.Argument(...)):
    launch_app(module)


if __name__ == "__main__":
    app()
