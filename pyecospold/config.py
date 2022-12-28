from dataclasses import dataclass
from typing import Any, Dict, ClassVar


@dataclass
class Defaults:
    qualityNetwork: ClassVar[str] = "1"
    uncertaintyType: ClassVar[str] = "1"

    @classmethod
    def set_defaults(cls, defaults: Dict[str, Any]) -> None:
        for key, value in defaults.items():
            setattr(cls, key, value)
