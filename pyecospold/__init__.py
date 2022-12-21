__all__ = (
    "__version__",
    "parse_file",
)

__version__ = get_version_tuple()

from .core import parse_file
from .utils import get_version_tuple