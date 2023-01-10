"""Internal helper classes."""
from datetime import datetime
from typing import Any, Dict, List

from lxml import etree

from .config import Defaults


class DataHelper:
    """Helper class for reading and writing Ecospold custom classes attributes."""

    TIMESTAMP_FORMAT: str = "%Y-%m-%dT%H:%M:%S"
    TYPE_FUNC_MAP: Dict[type, Any] = {
        bool: lambda string: string.lower() == "true",
        datetime: lambda string: datetime.strptime(string, DataHelper.TIMESTAMP_FORMAT)
    }

    @staticmethod
    def set_attribute(element: etree.ElementBase, key: str, value: str) -> None:
        """Helper method for setting XML attributes. Raises DocumentInvalid
        exception on inappropriate setting according to XSD schema."""
        element.set(key, str(value))
        schema = etree.XMLSchema(file=Defaults.SCHEMA_FILE)
        schema.assertValid(element.getroottree())

    @staticmethod
    def set_attribute_list(
        element: etree.ElementBase, key: str, values: List[str]
    ) -> None:
        """Helper method for setting XML list attributes. Raises DocumentInvalid
        exception on inappropriate setting according to XSD schema."""
        for old_value in DataHelper.get_element_list(element, key):
            element.remove(old_value)
        elements = []
        for value in values:
            elements.append(
                etree.SubElement(
                    element,
                    f"{{{element.nsmap[None]}}}{key}"
                )
            )
            elements[-1].text = value
        element.extend(elements)
        schema = etree.XMLSchema(file=Defaults.SCHEMA_FILE)
        schema.assertValid(element.getroottree())

    @staticmethod
    def get_element(parent: etree.ElementBase, element: str) -> Any:
        """Helper wrapper method for retrieving XML elements as custom
        Ecospold classes."""
        return parent.find(element, namespaces=parent.nsmap)

    @staticmethod
    def get_element_list(parent: etree.ElementBase, element: str) -> List[Any]:
        """Helper wrapper method for retrieving XML list elements as a list
        of custom Ecospold classes."""
        return parent.findall(element, namespaces=parent.nsmap)

    @staticmethod
    def get_element_text(parent: etree.ElementBase, element: str) -> str:
        """Helper wrapper method for retrieving XML element text as a string.
        Returns Defaults.TYPE_DEFAULTS[str] if no text exists or element is None."""
        return getattr(
            DataHelper.get_element(parent, element),
            "text",
            Defaults.TYPE_DEFAULTS[str]
        )

    @staticmethod
    def get_attribute(
        parent: etree.ElementBase, attribute: str, attr_type: type = str
    ) -> Any:
        """Helper wrapper method for retrieving XML attributes. Returns
        Defaults.TYPE_DEFAULTS[type] if attribute doesn't exist."""
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
        """Helper wrapper method for retrieving XML list attributes.
        Returns empty list if attributes don't exist."""
        return list(
            map(
                lambda x:
                    DataHelper.TYPE_FUNC_MAP.get(attr_type, attr_type)(x.text),
                DataHelper.get_element_list(parent, attribute)
            )
        )

    @staticmethod
    def create_attribute(name: str, attr_type: type) -> property:
        """Helper wrapper method for creating setters and getters for an attribute"""
        return property(
            lambda self: DataHelper.get_attribute(self, name, attr_type),
            lambda self, value: DataHelper.set_attribute(self, name, value)
        )

    @staticmethod
    def create_attribute_list(name: str, attr_type: type) -> property:
        """Helper wrapper method for creating setters and getters for an attribute
        list"""
        return property(
            lambda self: DataHelper.get_attribute_list(self, name, attr_type),
            lambda self, values: DataHelper.set_attribute_list(self, name, values)
        )
