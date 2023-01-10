import pytest
from lxml.etree import DocumentInvalid

from pyecospold.core import parse_file
from pyecospold.model import ReferenceFunction


@pytest.fixture
def referenceFunction() -> ReferenceFunction:
    ecoSpold = parse_file("data/examples/00001.xml")
    processInformation = ecoSpold.dataset.metaInformation.processInformation
    return processInformation.referenceFunction


def test_set_attribute_fail(referenceFunction: ReferenceFunction) -> None:
    with pytest.raises(DocumentInvalid):
        referenceFunction.amount = "abc"


def test_set_attribute_success(referenceFunction: ReferenceFunction) -> None:
    amount = 2.0
    referenceFunction.amount = amount

    assert referenceFunction.amount == amount


def test_set_attribute_list_success(referenceFunction: ReferenceFunction) -> None:
    synonyms = ["0", "1", "2"]
    referenceFunction.synonyms = synonyms

    assert referenceFunction.synonyms == synonyms
