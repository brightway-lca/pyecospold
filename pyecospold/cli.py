"""Command-line interface."""
import click


@click.command()
@click.version_option()
def run() -> None:
    """pyecospold."""
    pass


if __name__ == "__main__":
    run(prog_name="pyecospold")  # pragma: no cover
