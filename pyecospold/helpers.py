import logging
from typing import Any, Dict, List

import numpy as np
from lxml import etree

from .config import Defaults


class DataHelper:
    SCHEMA: etree.XMLSchema = etree.XMLSchema(file="data/schema/EcoSpold01Dataset.xsd")
    TIMESTAMP_FORMAT: str = "%Y-%m-%dT%H:%M:%S"

    @staticmethod
    def str_to_bool(string: str) -> bool:
        return string.lower() == "true"

    TYPE_FUNC_MAP: Dict[type, Any] = {
        bool: str_to_bool
    }
    TYPE_FUNC_DEFAULTS: Dict[type, Any] = {
        int: np.nan,
        float: np.nan,
        bool: False,
        str: ""
    }

    @staticmethod
    def try_set(element: etree.ElementBase, key: str, value: str) -> bool:
        current_value = getattr(element, key)
        element.set(key, str(value))

        validation = DataHelper.SCHEMA.validate(element.getroottree())
        if validation:
            return True

        element.set(key, str(current_value))
        logging.warning(
            f"Can't set property {element.__class__.__name__}.{key} "
            f"of type {type(current_value)} to: {value}"
        )
        return False

    @staticmethod
    def get_element(parent: etree.ElementBase, element: str) -> Any:
        return parent.find(element, namespaces=parent.nsmap)

    @staticmethod
    def get_element_list(parent: etree.ElementBase, element: str) -> List[Any]:
        return parent.findall(element, namespaces=parent.nsmap)

    @staticmethod
    def get_attribute(
        parent: etree.ElementBase, attribute: str, attr_type: type = str
    ) -> Any:
        return DataHelper.TYPE_FUNC_MAP.get(attr_type, attr_type)(
            parent.get(
                attribute,
                getattr(
                    Defaults, attribute,
                    DataHelper.TYPE_FUNC_DEFAULTS.get(attr_type, None)
                )
            )
        )

    @staticmethod
    def get_attribute_list(
        parent: etree.ElementBase, attribute: str, attr_type: type = str
    ) -> List[Any]:
        return list(
            map(
                lambda x:
                    DataHelper.TYPE_FUNC_MAP.get(attr_type, attr_type)(x.text),
                DataHelper.get_element_list(parent, attribute)
            )
        )
