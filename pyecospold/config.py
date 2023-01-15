"""Defaults configuration."""
import configparser
from dataclasses import dataclass
from pathlib import Path
from typing import Any, ClassVar, Dict

import numpy as np


SCHEMA_DIR = Path(__file__).parent.resolve() / "schemas"


@dataclass
class Defaults:
    """Stores default values for Ecospold attributes used when no value exists.
    Defaults can be fully/ partially overridden by providing a config file through
    cli or by using set_defaults method"""

    qualityNetwork: ClassVar[str] = "1"
    uncertaintyType: ClassVar[str] = "1"
    allocationMethod: ClassVar[str] = "-1"

    TYPE_DEFAULTS: ClassVar[Dict[type, Any]] = {
        int: np.nan_to_num(np.nan),
        float: np.nan,
        bool: False,
        str: "",
    }
    SCHEMA_FILE: ClassVar[str] = str(SCHEMA_DIR / "EcoSpold01Dataset.xsd")

    @classmethod
    def config_defaults(cls, config_file: str) -> None:
        """Fully/ partially overrides defaults.

        Parameters:
        config_file: path for config file.
        """
        config = configparser.ConfigParser()
        config.read(config_file)
        defaults = dict(config["defaults"])
        Defaults.set_defaults(defaults)

    @classmethod
    def set_defaults(cls, defaults: Dict[str, Any]) -> None:
        """Fully/ partially overrides defaults.

        Parameters:
        defaults: attribute-value dictionary.
        """
        for key, value in defaults.items():
            setattr(cls, key, value)
