"""Test cases for the __core__ module."""

import os
import tempfile
from pathlib import Path

from pyecospold.core import (
    parse_directory_v1,
    parse_directory_v2,
    parse_file_v1,
    save_file,
)


def test_parse_directory_v1() -> None:
    """It reads all files successfully."""
    dirPath = os.path.join(Path(__file__).parent.parent.resolve(), "data", "v1")
    files = [os.path.join(dirPath, "v1_1.xml"), os.path.join(dirPath, "v1_2.spold")]
    ecospoldList = sorted(parse_directory_v1(dirPath))

    assert len(ecospoldList) == 2
    assert ecospoldList[0][0] == Path(files[0])
    assert ecospoldList[1][0] == Path(files[1])
    assert ecospoldList[0][1].dataset.generator == "EcoAdmin 1.1.17.110"
    assert ecospoldList[1][1].dataset.generator == "EcoAdmin 1.1.17.110"


def test_parse_directory_v2() -> None:
    """It reads all files successfully."""
    dirPath = os.path.join(Path(__file__).parent.parent.resolve(), "data", "v2")
    files = [os.path.join(dirPath, "v2_1.xml"), os.path.join(dirPath, "v2_2.spold")]
    ecospoldList = sorted(parse_directory_v2(dirPath))
    activity1 = ecospoldList[0][1].activityDataset.activityDescription.activity
    activity2 = ecospoldList[1][1].childActivityDataset.activityDescription.activity

    assert len(ecospoldList) == 2
    assert ecospoldList[0][0] == Path(files[0])
    assert ecospoldList[1][0] == Path(files[1])
    assert activity1.inheritanceDepth == 0
    assert activity2.inheritanceDepth == 0


def test_save_file() -> None:
    """It saves read file correctly."""
    inputPath = "data/v1/v1_1.xml"
    metaInformation = parse_file_v1(inputPath)
    outputPath = os.path.join(tempfile.gettempdir(), os.urandom(24).hex())
    save_file(metaInformation, outputPath)

    with open(inputPath, encoding="utf-8") as inputFile:
        with open(outputPath, encoding="utf-8") as outputFile:
            mapping = {ord(c): "" for c in [" ", "\t", "\n"]}
            translatedOutput = outputFile.read().translate(mapping)
            translatedInput = inputFile.read().translate(mapping)
            assert translatedOutput == translatedInput
