from pyecospold.config import Defaults


def test_set_defaults() -> None:
    defaults = {"qualityNetwork": "2"}
    Defaults.set_defaults(defaults)

    assert Defaults.qualityNetwork == defaults["qualityNetwork"]
