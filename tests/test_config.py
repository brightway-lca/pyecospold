"""Test cases for the __config__ module."""

from pyecospold.config import Defaults


def test_set_defaults() -> None:
    """It overrides defaults variables."""
    defaults = {"qualityNetwork": "2"}
    Defaults.set_defaults(defaults)

    assert Defaults.qualityNetwork == defaults["qualityNetwork"]
