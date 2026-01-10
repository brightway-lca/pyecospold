"""Test cases for the lxmlh config module."""

from datetime import datetime

from pyecospold.lxmlh.config import TYPE_FUNC_MAP


def test_datetime_parsing_basic() -> None:
    """It parses basic ISO format datetime strings."""
    dt_string = "2023-03-29T18:04:18"
    result = TYPE_FUNC_MAP[datetime](dt_string)
    assert isinstance(result, datetime)
    assert result == datetime(2023, 3, 29, 18, 4, 18)


def test_datetime_parsing_with_timezone() -> None:
    """It parses ISO format datetime strings with timezone offset."""
    dt_string = "2023-03-29T18:04:18.534+02:00"
    result = TYPE_FUNC_MAP[datetime](dt_string)
    assert isinstance(result, datetime)
    # fromisoformat preserves timezone info
    assert result.year == 2023
    assert result.month == 3
    assert result.day == 29
    assert result.hour == 18
    assert result.minute == 4
    assert result.second == 18
    assert result.microsecond == 534000
    assert result.tzinfo is not None
