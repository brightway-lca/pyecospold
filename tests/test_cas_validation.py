"""Test cases for the __cas_validation__ module."""
import math

import pytest

from pyecospold.cas_validation import validate_cas


def test_nan():
    """It raises ValueError."""
    with pytest.raises(ValueError):
        validate_cas(math.nan)


def test_valid_int():
    """It validates int CAS."""
    cas = 110634
    assert validate_cas(cas) == "0000110-63-4"


def test_valid_float():
    """It validates float CAS."""
    cas = 110634.0
    assert validate_cas(cas) == "0000110-63-4"


def test_extra_whitespace():
    """It validates CAS with extra whitespaces."""
    casPre = "  0000110-63-4"
    casPost = "0000110-63-4  "
    casNewLine = "0000110-63-4\n"

    assert validate_cas(casPre) == "0000110-63-4"
    assert validate_cas(casPost) == "0000110-63-4"
    assert validate_cas(casNewLine) == "0000110-63-4"


def test_invalid_characters():
    """It validates CAS with invalid characters."""
    with pytest.raises(ValueError):
        validate_cas("0000110-63-4a")

    with pytest.raises(ValueError):
        validate_cas("ε0000110-63-4")


def test_empty_cas():
    """It validates empty CAS."""
    with pytest.raises(ValueError):
        validate_cas("")


def test_hyphenation():
    """It validates CAS with hyphens."""
    casNoHyphen = "0000110634"
    casFourHyphens = "0-00011-063-4"
    # Two hyphens but in wrong place
    casTwoHyphens = "0-00011063-4"

    assert validate_cas(casNoHyphen) == "0000110-63-4"
    assert validate_cas(casFourHyphens) == "0000110-63-4"
    assert validate_cas(casTwoHyphens) == "0000110-63-4"


def test_check_digit():
    """It validates CAS digits."""
    casValid = "0000110634"
    casInvalid1 = "0000120634"
    casInvalid12 = "0000110635"

    assert validate_cas(casValid)
    with pytest.raises(ValueError):
        validate_cas(casInvalid1)
    with pytest.raises(ValueError):
        validate_cas(casInvalid12)


def test_zero_padding():
    """It validates zero padding."""
    casNoPadding = "110-63-4"
    casExtraPadding = "00000000000000110-63-4"

    assert validate_cas(casNoPadding) == "0000110-63-4"
    assert validate_cas(casExtraPadding) == "0000110-63-4"
