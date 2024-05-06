"""Fixtures for pyecospold"""

from io import BytesIO
from pathlib import Path
from typing import Callable

import pytest

from pyecospold.core import parse_file_v1
from pyecospold.model_v1 import EcoSpold, TimePeriod

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def fixtures_dir() -> Path:
    """Easy access to fixtures directory"""
    return FIXTURES_DIR


@pytest.fixture
def eco_spold() -> EcoSpold:
    """Single access to parsed ecospold1 file"""
    return parse_file_v1(FIXTURES_DIR / "v1" / "v1_1.xml")


@pytest.fixture
def v1_timeperiod_fixture() -> Callable:
    """Substitute the `timePeriod` section of XML file"""
    with open(FIXTURES_DIR / "templates" / "v1-timeperiod.xml", encoding="utf-8") as f:
        long_string = f.read()

    def f(timeperiod_xml: str) -> TimePeriod:
        string = long_string.format(timeperiod=timeperiod_xml)
        parsed = parse_file_v1(BytesIO(string.encode("utf-8")))
        return parsed.datasets[0].metaInformation.processInformation.timePeriod

    return f
