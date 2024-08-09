from datetime import datetime
from typing import Any, Callable, Dict

import numpy as np

TIMESTAMP_FORMAT: str = "%Y-%m-%dT%H:%M:%S"

TYPE_FUNC_MAP: Dict[type, Callable[[str], Any]] = {
    bool: lambda string: string.lower() == "true",
    datetime: lambda string: datetime.strptime(string, TIMESTAMP_FORMAT),
}

TYPE_DEFAULTS: Dict[type, Any] = {
    int: np.nan_to_num(np.nan),
    float: np.nan,
    bool: "false",
    str: "",
}
