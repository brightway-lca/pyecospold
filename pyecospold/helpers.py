import logging
from typing import Any, Dict, List

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
    def get_element_text(parent: etree.ElementBase, element: str) -> str:
        return getattr(
            DataHelper.get_element(parent, element),
            "text",
            Defaults.TYPE_DEFAULTS[str]
        )

    @staticmethod
    def get_attribute(
        parent: etree.ElementBase, attribute: str, attr_type: type = str
    ) -> Any:
        return DataHelper.TYPE_FUNC_MAP.get(attr_type, attr_type)(
            parent.get(
                attribute,
                getattr(
                    Defaults, attribute,
                    Defaults.TYPE_DEFAULTS.get(attr_type, None)
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
