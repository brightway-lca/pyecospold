"""Test cases for the __config__ module."""

import os
from pathlib import Path

from pyecospold.config import Defaults


def test_config_defaults() -> None:
    """It overrides defaults variables."""
    rootDir = Path(__file__).parent.parent.resolve()

    configFileDir = os.path.join(rootDir, "out", "tests")
    configFilePath = os.path.join(configFileDir, "config.ini")
    os.makedirs(configFileDir, exist_ok=True)

    schemaDir = os.path.join(rootDir, "pyecospold", "schemas")
    schemaV1File = os.path.join(schemaDir, "v1", "EcoSpold01Dataset.xsd")
    schemaV2File = os.path.join(schemaDir, "v2", "EcoSpold02.xsd")
    validCompanyCodes = "CompanyCodes.xml"

    with open(configFilePath, "w", encoding="utf-8") as configFile:
        configFile.write("[parameters]\n")
        configFile.write(f"SCHEMA_V1_FILE={schemaV1File}\n")
        configFile.write(f"SCHEMA_V2_FILE={schemaV2File}\n\n")
        configFile.write(f"[Dataset]\nvalidCompanyCodes={validCompanyCodes}\n")

    Defaults.config_defaults(configFilePath)

    assert Defaults.STATIC_DEFAULTS["Dataset"]["validCompanyCodes"] == validCompanyCodes

    Defaults.config_defaults("config.init")
