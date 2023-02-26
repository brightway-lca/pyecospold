from pyecospold.cas_validation import validate_cas, check_digit, convert_numeric_cas, rehyphenate_cas, zero_pad_cas
import math
import pytest


def test_nan():
    with pytest.raises(ValueError):
        convert_numeric_cas(math.nan)


def test_valid_int():
    s = 110634
    assert validate_cas(s) == "0000110-63-4"


def test_valid_float():
    s = 110634.0
    assert validate_cas(s) == "0000110-63-4"


def test_extra_whitespace():
    a = "  0000110-63-4"
    b = "0000110-63-4  "
    c = "0000110-63-4\n"

    assert validate_cas(a) == "0000110-63-4"
    assert validate_cas(b) == "0000110-63-4"
    assert validate_cas(c) == "0000110-63-4"


def test_invalid_characters():
    with pytest.raises(ValueError):
        validate_cas("0000110-63-4a")

    with pytest.raises(ValueError):
        validate_cas("ε0000110-63-4")


def test_empty_cas():
    with pytest.raises(ValueError):
        validate_cas("")


def test_hyphenation():
    a = "0000110634"
    b = "0-00011-063-4"
    # Two hyphens but in wrong place
    c = "0-00011063-4"

    assert validate_cas(a) == "0000110-63-4"
    assert validate_cas(b) == "0000110-63-4"
    assert validate_cas(c) == "0000110-63-4"


def test_checK_digit():
    a = "0000110634"
    b = "0000120634"
    c = "0000110635"

    assert validate_cas(a)
    with pytest.raises(ValueError):
        validate_cas(b)
    with pytest.raises(ValueError):
        validate_cas(c)


def test_zero_padding():
    assert validate_cas("110-63-4") == "0000110-63-4"
    assert validate_cas("00000000000000110-63-4") == "0000110-63-4"
