"""Test cases for the __config__ module."""

from pyecospold.config import Defaults
from pyecospold.version import __version__


def test_config_defaults() -> None:
    """It overrides defaults variables."""
    configFile = "config.ini"
    Defaults.config_defaults(configFile)

    assert (
        Defaults.STATIC_DEFAULTS["Dataset"]["validCompanyCodes"] == "CompanyCodes.xml"
    )
    assert (
        Defaults.DYNAMIC_DEFAULTS["Dataset"]["generator"] == f"pyecospold.{__version__}"
    )
