"""Test cases for the __parsers__ module."""

import os

from lxml import etree
from pyecospold.lxmlh.parsers import (
    parse_zip_file,
    save_file,
    validate_directory,
    validate_zip_file,
)

from .conftest import (
    DIR_DATA,
    FILE_SAMPLE,
    FILE_SAMPLE_DEFAULTS,
    FILE_SCHEMA,
    Lookup,
    compare_files,
    confirm_validation_results,
)


def test_parse_zip_file(zip_data) -> None:
    """It reads all files successfully."""
    roots = sorted(parse_zip_file(zip_data, FILE_SCHEMA, Lookup()))

    assert len(roots) == 2
    assert roots[0][0].name == FILE_SAMPLE.name
    assert roots[0][1].shipTo.name == "Ola Nordmann"


def test_save_file(ship_order: etree.ElementTree, tmpdir, random_file_name) -> None:
    """It saves file correctly."""
    outputPath = os.path.join(tmpdir, random_file_name)
    save_file(ship_order, outputPath)

    assert compare_files(FILE_SAMPLE, outputPath)


def test_save_file_defaults(
    ship_order: etree.ElementTree, tmpdir, random_file_name
) -> None:
    """It saves file correctly."""

    def _get_order_time(element: etree.ElementBase) -> str:
        return element.orderId

    staticDefaults = {"ShipOrder": {"orderStatus": "wip"}}
    dynamicDefaults = {"ShipOrder": {"orderTime": _get_order_time}}
    outputPath = os.path.join(tmpdir, random_file_name)
    save_file(
        ship_order,
        outputPath,
        static_defaults=staticDefaults,
        dynamic_defaults=dynamicDefaults,
    )
    assert compare_files(FILE_SAMPLE_DEFAULTS, outputPath)


def test_validate_directory() -> None:
    """It validates directory correctly."""
    validationResults = validate_directory(DIR_DATA, FILE_SCHEMA)
    confirm_validation_results(validationResults)


def test_validate_zip_file_with_fail(zip_data) -> None:
    """It validates zip file correctly."""
    validSuffixes = [".xml", ".invalid"]
    validationResults = validate_zip_file(
        zip_data, FILE_SCHEMA, valid_suffixes=validSuffixes
    )
    confirm_validation_results(validationResults)
