"""Test cases for the __config__ module."""

from pyecospold.config import Defaults


def test_config_defaults() -> None:
    """It overrides defaults variables."""
    configFile = "config.ini"
    Defaults.config_defaults(configFile)

    assert Defaults.qualityNetwork == "1"


def test_set_defaults() -> None:
    """It overrides defaults variables."""
    defaults = {"qualityNetwork": "2"}
    Defaults.set_defaults(defaults)

    assert Defaults.qualityNetwork == defaults["qualityNetwork"]
