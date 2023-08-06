import typer
from typing import Optional, List
from pathlib import Path

from ddot import lib
from devinstaller_core import exception as e
import anymarkup
import os.path
import os
from devinstaller_core import settings as s

app = typer.Typer()


DEFAULT_SPEC_FILES = ["devfile.toml", "devfile.yaml", "devfile.json"]
DEFAULT_SPEC_FILE = DEFAULT_SPEC_FILES[0]
DEFAULT_PROG_FILE = "devfile.py"


def get_spec_path(provided_path: Path) -> Path:
    if provided_path:
        return provided_path
    for i in DEFAULT_SPEC_FILES:
        if os.path.isfile(i):
            return Path(i)
    raise e.DevinstallerBaseException(
        "I wasn't able to find any spec file in the current directory, so you need to provide the path to a spec file."
    )


def goodbye() -> None:
    """Final callback function. Runs after the end of everything."""
    typer.secho("\nBye. Have a good day.", fg="green")


def get_path_relative_to_main(file_path: str):
    """Get the path relative to the script file
    """
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    full_path = os.path.join(script_dir, file_path)
    return Path(full_path).resolve()


def read_file(file_path: Path):
    """Read file
    """
    with open(str(file_path), "r") as _f:
        return _f.read()


def get_version():
    """Get the version using the `pyproject.toml` file
    """
    paths = ["../pyproject.toml", "pyproject.toml"]
    for p in paths:
        try:
            py_project_path = get_path_relative_to_main(p)
            data = read_file(py_project_path)
            data = anymarkup.parse(data, format="toml")
            return data["tool"]["poetry"]["version"]
        except Exception:
            pass
    return "N/A"


__version__ = get_version()


def version_callback(value: bool):
    """Callback function for version cli option
    """
    if value:
        typer.echo(f"Ddot Version: {__version__}")
        raise typer.Exit()


# @app.command()
# def install(
#     spec_file: Optional[Path] = typer.Option(DEFAULT_SPEC_FILE),
#     platform: Optional[str] = None,
#     module: Optional[str] = None,
# ) -> None:
#     """Install the default group and the modules which it requires"""
#     try:
#         req_list = [module] if isinstance(module, str) else None
#         d = lib.Devinstaller()
#         d.install(
#             spec_file_path=f"file: {spec_file}",
#             platform_codename=platform,
#             requirements_list=req_list,
#         )
#     except e.DevinstallerBaseException as err:
#         typer.secho(str(err), fg="red")


@app.command()
def show(spec_file: Optional[Path] = typer.Option(None)) -> None:
    """Show all the groups and modules available for your OS"""

    spec_file = get_spec_path(spec_file)
    d = lib.Devinstaller()
    d.show(spec_file_path=f"file: {spec_file}")


@app.command()
def run(
    module: Optional[List[str]] = typer.Option(None, "--module", "-m"),
    spec_file: Optional[Path] = typer.Option(None),
    verbose: bool = False,
):
    """Run commands"""

    s.settings.DDOT_VERBOSE = verbose
    spec_file = get_spec_path(spec_file)
    req_list = list(module)
    d = lib.Devinstaller()
    d.install(
        spec_file_path=f"file: {spec_file}",
        platform_codename=None,
        requirements_list=req_list,
    )


@app.callback()
def callback(
    ctx: typer.Context,
    _: Optional[bool] = typer.Option(
        None, "--version", callback=version_callback, is_eager=True
    ),
):
    pass


def main():
    try:
        app()
    except e.DevinstallerBaseException as err:
        typer.secho(str(err), fg="red")
    finally:
        goodbye()


if __name__ == "__main__":
    main()
