"""Test cases for the __helpers__ module."""

import pytest
from lxml.etree import DocumentInvalid

from pyecospold.core import parse_file
from pyecospold.model_v1 import ReferenceFunction


@pytest.fixture(name="reference_function")
def _reference_function() -> ReferenceFunction:
    """Fixture for getting ReferenceFunction element."""
    ecoSpold = parse_file("data/v1.xml")
    processInformation = ecoSpold.dataset.metaInformation.processInformation
    return processInformation.referenceFunction


def test_set_attribute_fail(reference_function: ReferenceFunction) -> None:
    "It raises DocumentInvalid error."
    with pytest.raises(DocumentInvalid):
        reference_function.amount = "abc"


def test_set_attribute_success(reference_function: ReferenceFunction) -> None:
    "It sets attribute correctly."
    amount = 2.0
    reference_function.amount = amount

    assert reference_function.amount == amount


def test_set_attribute_list_success(reference_function: ReferenceFunction) -> None:
    "It sets attribute list correctly."
    synonyms = ["0", "1", "2"]
    reference_function.synonyms = synonyms

    assert reference_function.synonyms == synonyms
