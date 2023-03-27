"""Test cases for the __core__ module."""

import os
import tempfile
from io import StringIO
from pathlib import Path

from pyecospold.core import (
    parse_directory_v1,
    parse_directory_v2,
    parse_file_v1,
    save_ecopsold_file,
    validate_file_v1,
    validate_file_v2,
)


def test_validate_file_v1_success() -> None:
    """It validates file successfully."""
    assert validate_file_v1("data/v1/v1_1.xml") is None


def test_validate_file_v1_fail() -> None:
    """It validates file successfully."""
    xml = StringIO("<ecoSpold></ecoSpold>")
    errorExpected = (
        "<string>:1:0:ERROR:SCHEMASV:SCHEMAV_CVC_ELT_1: Element 'ecoSpold': "
        "No matching global declaration available for the validation root."
    )
    errorActual = validate_file_v1(xml)
    assert errorActual is not None
    assert str(errorActual[0]) == errorExpected


def test_validate_file_v2_success() -> None:
    """It validates file successfully."""
    assert validate_file_v2("data/v2/v2_1.xml") is None


def test_parse_directory_v1() -> None:
    """It reads all files successfully."""
    dirPath = os.path.join(Path(__file__).parent.parent.resolve(), "data", "v1")
    files = [os.path.join(dirPath, "v1_1.xml"), os.path.join(dirPath, "v1_2.spold")]
    ecospoldList = sorted(
        parse_directory_v1(dirPath, valid_suffixes=[".xml", ".spold"])
    )

    assert len(ecospoldList) == 2
    assert ecospoldList[0][0] == Path(files[0])
    assert ecospoldList[1][0] == Path(files[1])
    assert ecospoldList[0][1].datasets[0].generator == "EcoAdmin 1.1.17.110"
    assert ecospoldList[1][1].datasets[0].generator == "EcoAdmin 1.1.17.110"


def test_parse_directory_v2() -> None:
    """It reads all files successfully."""
    dirPath = os.path.join(Path(__file__).parent.parent.resolve(), "data", "v2")
    files = [os.path.join(dirPath, "v2_1.xml"), os.path.join(dirPath, "v2_2.spold")]
    ecospoldList = sorted(
        parse_directory_v2(dirPath, valid_suffixes=[".xml", ".spold"])
    )
    activity1 = ecospoldList[0][1].activityDataset.activityDescription.activity[0]
    activity2 = ecospoldList[1][1].activityDataset.activityDescription.activity[0]

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
    save_ecopsold_file(metaInformation, outputPath, fill_defaults=False)

    with open(inputPath, encoding="utf-8") as inputFile:
        with open(outputPath, encoding="utf-8") as outputFile:
            mapping = {ord(c): "" for c in [" ", "\t", "\n"]}
            translatedOutput = outputFile.read().translate(mapping)
            translatedInput = inputFile.read().translate(mapping)
            assert translatedOutput == translatedInput


def test_save_file_defaults() -> None:
    """It saves read file correctly."""
    inputPath = "data/v1/v1_1.xml"
    expectedOutputPath = "data/tests/v1_1_defaults.xml"
    metaInformation = parse_file_v1(inputPath)
    outputPath = os.path.join(tempfile.gettempdir(), os.urandom(24).hex())
    save_ecopsold_file(metaInformation, outputPath, fill_defaults=True)

    with open(expectedOutputPath, encoding="utf-8") as inputFile:
        with open(outputPath, encoding="utf-8") as outputFile:
            mapping = {ord(c): "" for c in [" ", "\t", "\n"]}
            translatedOutput = outputFile.read().translate(mapping)
            translatedInput = inputFile.read().translate(mapping)
            assert translatedOutput == translatedInput
