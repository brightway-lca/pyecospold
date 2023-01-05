from pyecospold.core import parse_file
from pyecospold.model import ReferenceFunction

import pytest
from lxml.etree import DocumentInvalid


@pytest.fixture
def referenceFunction() -> ReferenceFunction:
    ecoSpold = parse_file("data/examples/00001.xml")
    processInformation = ecoSpold.dataset.metaInformation.processInformation
    return processInformation.referenceFunction


def test_try_set_fail(referenceFunction: ReferenceFunction) -> None:
    with pytest.raises(DocumentInvalid):
        referenceFunction.amount = "abc"


def test_try_set_success(referenceFunction: ReferenceFunction) -> None:
    amount = 2.0
    expected_amount = 2.0
    referenceFunction.amount = amount

    assert referenceFunction.amount == expected_amount
