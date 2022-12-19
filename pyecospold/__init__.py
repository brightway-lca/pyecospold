__all__ = (
    "__version__",
    "parse_file",
)

import importlib.metadata
from typing import Union


def get_version_tuple() -> tuple:
    def as_integer(x: str) -> Union[int, str]:
        try:
            return int(x)
        except ValueError:
            return x

    return tuple(
        as_integer(v)
        for v in importlib.metadata.version("pyecospold")
        .strip()
        .split(".")
    )

__version__ = get_version_tuple()

from .core import parse_file