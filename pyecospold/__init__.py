"""pyecospold."""
__all__ = (
    "__version__",
    "parse_directory",
    "parse_directory_v1",
    "parse_directory_v2",
    "parse_file",
    "parse_file_v1",
    "parse_file_v2",
    "validate_file",
    "validate_file_v1",
    "validate_file_v2",
    "save_file",
    "Defaults",
    "validate_cas",
)


import importlib.metadata
from typing import Union

from .cas_validation import validate_cas
from .config import Defaults
from .core import (
    parse_directory,
    parse_directory_v1,
    parse_directory_v2,
    parse_file,
    parse_file_v1,
    parse_file_v2,
    save_file,
    validate_file,
    validate_file_v1,
    validate_file_v2,
)


def get_version_tuple() -> tuple:
    """Returns version as (major, minor, micro)."""

    def as_integer(version: str) -> Union[int, str]:
        """Tries parsing version else returns as is."""
        try:
            return int(version)
        except ValueError:  # pragma: no cover
            return version  # pragma: no cover

    return tuple(
        as_integer(v)
        for v in importlib.metadata.version("pyecospold").strip().split(".")
    )


__version__ = get_version_tuple()
