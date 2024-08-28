import importlib

import typer
import anyio

app = typer.Typer()


def launch_app(module: str):
    target_module = importlib.import_module(f"omniamni.{module}")

    if hasattr(target_module, 'start'):
        anyio.run(target_module.start)
    else:
        raise RuntimeError(f"Module {app} does not have a start function")


@app.command()
def main(module: str = typer.Argument(...)):
    launch_app(module)


if __name__ == "__main__":
    app()
