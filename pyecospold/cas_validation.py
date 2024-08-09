"""All information from
https://www.cas.org/support/documentation/chemical-substances/checkdig

CAS numbers have the form A-B-C, where:

    A has between 2 and 7 integers
    B has 2 integers
    C is a single check digit integer

To calculate the check digit:

Each integer starting from the right, and ignoring hyphens, is given a
weight corresponding to its ordinal position (1-indexed). The check is
calculated from the sum of the weighted values, taking the values in
the ones digit. For example for 107-07-3, the sum would be:

    1 * 7 + 2 * 0 + 3 * 7 + 4 * 0 + 5 * 1 = 33

And the check digit would be 3 (the values in the ones position.
Similarly, for 110-63-4:

    1 * 3 + 2 * 6 + 3 * 0 + 4 * 1 + 5 * 1 = 24

"""
import math
from typing import Union


def validate_cas(cas: Union[str, int, float]) -> str:
    """Return valid CAS number as a correctly validate string, or raise ``ValueError``.

    Will check the check digit, re-hyphenate, and convert from a number if necessary.

    """
    if isinstance(cas, str):
        casStr = cas.strip()
    elif isinstance(cas, (int, float)):
        casStr = _convert_numeric_cas(cas)

    validCharacters = {str(x) for x in range(10)}.union({"-"})
    invalidCharacters = {c for c in casStr if c not in validCharacters}
    if invalidCharacters:
        raise ValueError(f"CAS number includes invalid characters: {invalidCharacters}")

    if not casStr:
        raise ValueError("Given CAS is empty: {cas}.")

    casStr = _rehyphenate_cas(casStr)

    _check_digit(casStr)
    return _zero_pad_cas(casStr)


def _check_digit(cas_str: str) -> None:
    total = sum(
        (a + 1) * int(b) for a, b in zip(range(9), cas_str.replace("-", "")[-2::-1])
    )
    error = (
        f"CAS Check Digit error: CAS '{cas_str}' has check digit of {cas_str[-1]}, "
        f"but it should be {total % 10}"
    )
    if not total % 10 == int(cas_str[-1]):
        raise ValueError(f"CAS not valid: {cas_str} ({error})")


def _convert_numeric_cas(cas: Union[int, float]) -> str:
    if math.isnan(cas):
        raise ValueError("Given CAS value is Not-a-Number")
    casStr = str(int(cas))
    return _rehyphenate_cas(casStr)


def _rehyphenate_cas(cas_str: str) -> str:
    cas_str = cas_str.replace("-", "")
    return f"{cas_str[-10:-3]}-{ cas_str[-3:-1]}-{cas_str[-1]}"


def _zero_pad_cas(cas_str: str) -> str:
    zeros = "0" * (12 - len(cas_str))
    return zeros + cas_str
