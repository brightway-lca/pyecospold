"""pyecospold."""
__all__ = (
    "__version__",
    "parse_file",
    "save_file",
    "Defaults"
)


import importlib.metadata
from typing import Union

from .config import Defaults
from .core import parse_file, save_file


def get_version_tuple() -> tuple:
    """Returns version as (major, minor, micro)."""
    def as_integer(x: str) -> Union[int, str]:
        """Tries parsing version else returns as is."""
        try:
            return int(x)
        except ValueError:  # pragma: no cover
            return x  # pragma: no cover

    return tuple(
        as_integer(v)
        for v in importlib.metadata.version("pyecospold")
        .strip()
        .split(".")
    )


__version__ = get_version_tuple()
