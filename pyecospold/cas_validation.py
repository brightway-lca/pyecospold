from numbers import Number
import math

"""All information from https://www.cas.org/support/documentation/chemical-substances/checkdig

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


VALID_CHARACTERS = {str(x) for x in range(10)}.union({"-"})


def validate_cas(s):
    """Return valid CAS number as a correctly validate string, or raise ``ValueError``.

    Will check the check digit, re-hyphenate, and convert from a number if necessary.

    """
    if isinstance(s, str):
        s = s.strip()
    elif isinstance(s, Number):
        s = convert_numeric_cas(s)

    invalid_characters = {c for c in s if c not in VALID_CHARACTERS}
    if invalid_characters:
        raise ValueError(f"CAS number includes invalid characters: {invalid_characters}")

    if not s:
        raise ValueError("Given CAS is empty")

    s = rehyphenate_cas(s)

    check_digit(s)
    return zero_pad_cas(s)


def check_digit(s):
    ERROR = "CAS Check Digit error: CAS '{}' has check digit of {}, but it should be {}"

    total = sum((a + 1) * int(b) for a, b in zip(range(9), s.replace("-", "")[-2::-1]))
    if not total % 10 == int(s[-1]):
        raise ValueError("CAS not valid: {} ({})".format(s, ERROR.format(s, s[-1], total % 10)))


def convert_numeric_cas(s):
    if math.isnan(s):
        raise ValueError("Given CAS value is Not-a-Number")
    s = str(int(s))
    return rehyphenate_cas(s)


def rehyphenate_cas(s):
    s = s.replace("-", "")
    return "{}-{}-{}".format(s[-10:-3], s[-3:-1], s[-1])


def zero_pad_cas(s):
    zeros = "0" * (12 - len(s))
    return zeros + s
