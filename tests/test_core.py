"""Test cases for the __core__ module."""

import os
import tempfile
from pathlib import Path

from pyecospold.core import parse_directory_v1, parse_file_v1, save_file


def test_parse_directory_v1() -> None:
    """It reads all files successfully."""
    dirPath = os.path.join(Path(__file__).parent.parent.resolve(), "data", "v1")
    ecospoldList = parse_directory_v1(dirPath)

    assert len(ecospoldList) == 2
    assert ecospoldList[0][0] == Path(os.path.join(dirPath, "v1_1.xml"))
    assert ecospoldList[1][0] == Path(os.path.join(dirPath, "v1_2.spold"))
    assert ecospoldList[0][1].dataset.generator == "EcoAdmin 1.1.17.110"
    assert ecospoldList[1][1].dataset.generator == "EcoAdmin 1.1.17.110"


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
