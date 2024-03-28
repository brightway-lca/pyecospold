"""Test cases for the __core__ module."""

import os
import zipfile
from io import StringIO
from pathlib import Path
from typing import Callable, List, Tuple, Union

from lxml import etree

from pyecospold import (
    parse_directory_v1,
    parse_directory_v2,
    parse_file_v1,
    parse_zip_file_v1,
    parse_zip_file_v2,
    save_ecospold_file,
    validate_directory_v1,
    validate_directory_v2,
    validate_file_v1,
    validate_file_v2,
    validate_zip_file_v1,
    validate_zip_file_v2,
)
from pyecospold.model_v1 import EcoSpold as EcoSpoldV1
from pyecospold.model_v2 import EcoSpold as EcoSpoldV2


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
    ecospoldList = sorted(parse_directory_v1(dirPath))

    assert len(ecospoldList) == 2
    assert ecospoldList[0][0] == Path(files[0])
    assert ecospoldList[1][0] == Path(files[1])
    assert ecospoldList[0][1].datasets[0].generator == "EcoAdmin 1.1.17.110"
    assert ecospoldList[1][1].datasets[0].generator == "EcoAdmin 1.1.17.110"


def test_parse_directory_v2() -> None:
    """It reads all files successfully."""
    dirPath = os.path.join(Path(__file__).parent.parent.resolve(), "data", "v2")
    files = [os.path.join(dirPath, "v2_1.xml"), os.path.join(dirPath, "v2_2.spold")]
    ecospoldList = sorted(parse_directory_v2(dirPath))
    activity1 = ecospoldList[0][1].activityDataset.activityDescription.activity[0]
    activity2 = ecospoldList[1][1].activityDataset.activityDescription.activity[0]

    assert len(ecospoldList) == 2
    assert ecospoldList[0][0] == Path(files[0])
    assert ecospoldList[1][0] == Path(files[1])
    assert activity1.inheritanceDepth == 0
    assert activity2.inheritanceDepth == 0


def test_save_file(tmpdir) -> None:
    """It saves read file correctly."""
    inputPath = "data/v1/v1_1.xml"
    metaInformation = parse_file_v1(inputPath)
    outputPath = os.path.join(tmpdir, os.urandom(24).hex())
    save_ecospold_file(metaInformation, outputPath, fill_defaults=False)

    with open(inputPath, encoding="utf-8") as inputFile:
        with open(outputPath, encoding="utf-8") as outputFile:
            mapping = {ord(c): "" for c in [" ", "\t", "\n"]}
            translatedOutput = outputFile.read().translate(mapping)
            translatedInput = inputFile.read().translate(mapping)
            assert translatedOutput == translatedInput


def test_save_file_defaults(tmpdir) -> None:
    """It saves read file correctly."""
    inputPath = "data/v1/v1_1.xml"
    expectedOutputPath = "data/tests/v1_1_defaults.xml"
    metaInformation = parse_file_v1(inputPath)
    outputPath = os.path.join(tmpdir, os.urandom(24).hex())
    save_ecospold_file(metaInformation, outputPath, fill_defaults=True)

    with open(expectedOutputPath, encoding="utf-8") as inputFile:
        with open(outputPath, encoding="utf-8") as outputFile:
            mapping = {ord(c): "" for c in [" ", "\t", "\n"]}
            translatedOutput = outputFile.read().translate(mapping)
            translatedInput = inputFile.read().translate(mapping)
            assert translatedOutput == translatedInput


def _validate_directory(
    dataset_version: int,
    validator: Callable[
        [Union[str, Path], Union[List[str], None]], List[Tuple[Path, etree.ElementBase]]
    ],
) -> None:
    """It reads all files successfully."""
    dirPath = os.path.join(Path(__file__).parents[1], "data", f"v{dataset_version}")
    files = [
        os.path.join(dirPath, f"v{dataset_version}_1.xml"),
        os.path.join(dirPath, f"v{dataset_version}_2.spold"),
    ]
    result = sorted(validator(dirPath))

    assert len(result) == len(files)
    for i in range(2):
        assert str(result[i][0]) == str(files[i])
        assert result[i][1] is None


def test_validate_directory_v1() -> None:
    """It validates directory successfully."""
    _validate_directory(1, validate_directory_v1)


def test_validate_directory_v2() -> None:
    """It validates directory successfully."""
    _validate_directory(2, validate_directory_v2)


def __zip_data(tmpdir, data_dir: str, file_name: str = "data.zip") -> str:
    zipFilePath = os.path.join(tmpdir, file_name)
    with zipfile.ZipFile(zipFilePath, "w", zipfile.ZIP_DEFLATED) as zipFile:
        for root, _, files in os.walk(data_dir):
            for file in files:
                zipFile.write(os.path.join(root, file), file)
    return zipFilePath


def _parse_zip_file(
    file_path: str,
    parser: Callable[
        [Union[str, Path], Union[List[str], None]], List[Tuple[Path, etree.ElementBase]]
    ],
    root_class: etree.ElementBase,
) -> None:
    """It reads zip file successfully."""
    results = parser(file_path)

    for result in results:
        assert isinstance(result[1], root_class)


def test_parse_zip_file_v1(tmpdir) -> None:
    """It reads zip file successfully."""
    zipFilePath = __zip_data(tmpdir, os.path.join("data", "v1"))
    _parse_zip_file(zipFilePath, parse_zip_file_v1, EcoSpoldV1)


def test_parse_zip_file_v2(tmpdir) -> None:
    """It reads zip file successfully."""
    zipFilePath = __zip_data(tmpdir, os.path.join("data", "v2"))
    _parse_zip_file(zipFilePath, parse_zip_file_v2, EcoSpoldV2)


def test_validate_zip_file_v1(tmpdir) -> None:
    """It validates zip file successfully."""
    zipFilePath = __zip_data(tmpdir, os.path.join("data", "v1"))
    for result in validate_zip_file_v1(zipFilePath):
        assert result[1] is None


def test_validate_zip_file_v2(tmpdir) -> None:
    """It validates zip file successfully."""
    zipFilePath = __zip_data(tmpdir, os.path.join("data", "v2"))
    for result in validate_zip_file_v2(zipFilePath):
        assert result[1] is None
