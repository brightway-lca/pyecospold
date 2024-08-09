"""Fixtures for pyecospold"""

import os
import zipfile
from pathlib import Path
from typing import List

import pytest
from lxml import etree

DIR_DATA = os.path.join(Path(__file__).parent.parent.resolve(), "data", "lxmlh")
FILE_NAME_ZIP = "data.zip"
FILE_SAMPLE = Path(os.path.join(DIR_DATA, "sample.xml"))
FILE_SAMPLE_DEFAULTS = Path(os.path.join(DIR_DATA, "sample_defaults.xml"))
FILE_SAMPLE_INVALID = Path(os.path.join(DIR_DATA, "sample.xml.invalid"))
FILE_SCHEMA = Path(os.path.join(DIR_DATA, "schema.xsd"))
ERROR_STR = (
    "ERROR:SCHEMASV:SCHEMAV_CVC_COMPLEX_TYPE_4: Element 'shiporder': "
    "The attribute 'orderid' is required but missing."
)


from io import BytesIO
from typing import Callable

from pyecospold.core import parse_file_v1
from pyecospold.lxmlh import (
    create_attribute,
    create_attribute_list,
    create_element_text,
    get_element,
    get_element_list,
    get_inner_text_list,
    parse_file,
)
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


class ShipTo(etree.ElementBase):
    """ShipTo element."""

    name = create_element_text("name", str, FILE_SCHEMA)
    address = create_element_text("address", str, FILE_SCHEMA)
    city = create_element_text("city", str, FILE_SCHEMA)
    country = create_element_text("country", str, FILE_SCHEMA)


class Item(etree.ElementBase):
    """Item element."""

    @property
    def notes(self) -> List[str]:
        """Notes."""
        return get_inner_text_list(self, "note")


class ShipOrder(etree.ElementBase):
    """ShipOrder element."""

    orderId = create_attribute("orderid", str, FILE_SCHEMA, lambda orderId: orderId)
    orderStatus = create_attribute("orderstatus", str, FILE_SCHEMA, None)
    orderTime = create_attribute("ordertime", str, FILE_SCHEMA, None)
    orderPerson = create_element_text("orderperson", str, FILE_SCHEMA)
    discounts = create_attribute_list("discount", int, FILE_SCHEMA)

    @property
    def shipTo(self) -> "ShipTo":
        """Inner shipto element"""
        return get_element(self, "shipto")

    @property
    def itemsList(self) -> List["Item"]:
        "Items."
        return get_element_list(self, "item")


class Lookup(etree.CustomElementClassLookup):
    """Cutom lookup."""

    def lookup(self, unused_node_type, unused_document, unused_namespace, name):
        """Maps XML elements to custom classes."""
        lookupMap = {
            "item": Item,
            "shiporder": ShipOrder,
            "shipto": ShipTo,
        }
        try:
            return lookupMap[name]
        except KeyError:
            return None


@pytest.fixture(name="ship_order")
def __ship_order() -> etree.ElementTree:
    return parse_file(FILE_SAMPLE, FILE_SCHEMA, Lookup())


@pytest.fixture(name="random_file_name")
def __random_file_name() -> str:
    return os.urandom(24).hex()


@pytest.fixture(name="zip_data")
def __zip_data(tmpdir) -> str:
    zipFilePath = os.path.join(tmpdir, FILE_NAME_ZIP)
    with zipfile.ZipFile(zipFilePath, "w", zipfile.ZIP_DEFLATED) as zipFile:
        for root, _, files in os.walk(DIR_DATA):
            for file in files:
                zipFile.write(os.path.join(root, file), file)
    return zipFilePath


def compare_files(file1: str, file2: str) -> bool:
    """Compares two files ignoring whitespace."""
    with open(file1, encoding="utf-8") as inputFile:
        with open(file2, encoding="utf-8") as outputFile:
            mapping = {ord(c): "" for c in [" ", "\t", "\n"]}
            translatedOutput = outputFile.read().translate(mapping)
            translatedInput = inputFile.read().translate(mapping)
            return translatedOutput == translatedInput


def confirm_validation_results(validation_results: List) -> None:
    """Tests validation results."""
    for validationResult in validation_results:
        if validationResult[0].name == FILE_SAMPLE_INVALID.name:
            assert str(validationResult[1][0]).find(ERROR_STR) != -1
        else:
            assert validationResult[1] is None
