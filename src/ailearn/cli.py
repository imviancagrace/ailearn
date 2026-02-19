import typer
from rich.console import Console

from ailearn.commands.init import init

app = typer.Typer(
    name="ailearn",
    help="AI-assisted learning toolkit for junior developers.",
    add_completion=False,
    no_args_is_help=True,
)
console = Console()


@app.callback()
def main() -> None:
    """AILearn — AI-assisted learning toolkit for junior developers."""


app.command("init")(init)

if __name__ == "__main__":
    app()
