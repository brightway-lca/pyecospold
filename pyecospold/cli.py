"""Command-line interface."""
import configparser

import click

from .config import Defaults
from .core import parse_file


@click.group()
@click.version_option()
def run() -> None:
    """pyecospold: convert ecospold XML formats to their Python equivalents and
    export the same data back to XML."""
    pass


@click.command("parse")
@click.argument("input_file", type=click.Path())
@click.option(
    "-c",
    "--config_file",
    default="config.ini",
    help="-cPath to the ini config file.",
    type=click.Path()
)
def parse(input_file, config_file):
    """ input_file: Path to the xml input file. """
    config = configparser.ConfigParser()
    config.read(config_file)
    defaults = dict(config["defaults"])
    Defaults.set_defaults(defaults)
    parse_file(input_file)


run.add_command(parse)


if __name__ == "__main__":
    run(prog_name="pyecospold")  # pragma: no cover
