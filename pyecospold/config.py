"""Defaults configuration."""
import configparser
from dataclasses import dataclass
from typing import Any, Dict, ClassVar

import numpy as np


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
        str: ""
    }
    SCHEMA_FILE: ClassVar[str] = "data/schema/EcoSpold01Dataset.xsd"

    @classmethod
    def config_defaults(cls, config_file: str) -> None:
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
