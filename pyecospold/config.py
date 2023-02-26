"""Defaults configuration."""
import configparser
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, ClassVar, Dict

import numpy as np

from .version import __version__


@dataclass
class Defaults:
    """Stores default values for Ecospold attributes used when no value exists.
    Defaults can be fully/ partially overridden by providing a config file or by
    using set_defaults method"""

    SCHEMA_DIR: ClassVar[str] = os.path.join(Path(__file__).parent.resolve(), "schemas")
    SCHEMA_V1_FILE: ClassVar[str] = os.path.join(
        SCHEMA_DIR, "v1", "EcoSpold01Dataset.xsd"
    )
    SCHEMA_V2_FILE: ClassVar[str] = os.path.join(SCHEMA_DIR, "v2", "EcoSpold02.xsd")

    TYPE_DEFAULTS: ClassVar[Dict[type, Any]] = {
        int: np.nan_to_num(np.nan),
        float: np.nan,
        bool: "false",
        str: "",
    }

    DYNAMIC_DEFAULTS: ClassVar[Dict[str, Dict[str, Any]]] = {
        "Dataset": {
            "generator": f"pyecospold.{__version__}",
        },
    }
    STATIC_DEFAULTS: ClassVar[Dict[str, Dict[str, str]]] = {
        "Allocation": {
            "allocationMethod": "-1",
        },
        "DataEntryBy": {
            "qualityNetwork": "1",
        },
        "Dataset": {
            "validCompanyCodes": "CompanyCodes.xml",
            "validRegionalCodes": "RegionalCodes.xml",
            "validCategories": "Categories.xml",
            "validUnits": "Units.xml",
        },
        "DataSetInformation": {
            "impactAssessmentResult": "false",
            "internalVersion": "1.0",
            "version": "1.0",
        },
        "Exchange": {
            "uncertaintyType": "1",
        },
        "ReferenceFunction": {
            "infrastructureProcess": "true",
        },
    }

    @classmethod
    def config_defaults(cls, config_file: str) -> None:
        """Fully/ partially overrides defaults.

        Parameters:
        config_file: path for config file.
        """
        config = configparser.ConfigParser()
        config.optionxform = lambda optionstr: optionstr
        config.read(config_file)

        if config.has_section("parameters"):
            for key, value in dict(config["parameters"]).items():
                setattr(cls, key, value)

        staticDefaults = {
            name: dict(section)
            for name, section in config.items()
            if name not in ["parameters", "defaults"]
        }
        cls.static_defaults = staticDefaults
