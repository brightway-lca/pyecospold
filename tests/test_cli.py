"""Test cases for the __cli__ module."""

import pytest
from click.testing import CliRunner

from pyecospold import cli

@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def test_main_succeeds(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(cli.run)
    assert result.exit_code == 0
