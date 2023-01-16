"""Test cases for the __core__ module."""

import os
from pathlib import Path

from pyecospold.core import parse_directory_v1


def test_parse_directory_v1() -> None:
    """It reads all files successfully."""
    dirPath = os.path.join(Path(__file__).parent.parent.resolve(), "data", "v1")
    ecospoldList = parse_directory_v1(dirPath)

    assert len(ecospoldList) == 2
    assert ecospoldList[0][0] == Path(os.path.join(dirPath, "v1_1.xml"))
    assert ecospoldList[1][0] == Path(os.path.join(dirPath, "v1_2.spold"))
    assert ecospoldList[0][1].dataset.generator == "EcoAdmin 1.1.17.110"
    assert ecospoldList[1][1].dataset.generator == "EcoAdmin 1.1.17.110"
