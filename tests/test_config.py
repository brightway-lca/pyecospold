"""Test cases for the __config__ module."""

from pyecospold.config import Defaults


def test_config_defaults() -> None:
    """It overrides defaults variables."""
    configFile = "config.ini"
    Defaults.config_defaults(configFile)

    assert (
        Defaults.STATIC_DEFAULTS["Dataset"]["validCompanyCodes"] == "CompanyCodes.xml"
    )
