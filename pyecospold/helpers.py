"""Internal helper classes."""
import re
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

from lxml import etree

from .config import Defaults


class DataHelper:
    """Helper class for reading and writing Ecospold custom classes attributes."""

    TIMESTAMP_FORMAT: str = "%Y-%m-%dT%H:%M:%S"
    TYPE_FUNC_MAP: Dict[type, Callable[[str], Any]] = {
        bool: lambda string: string.lower() == "true",
        datetime: lambda string: datetime.strptime(string, DataHelper.TIMESTAMP_FORMAT),
    }

    @staticmethod
    def set_attribute(
        element: etree.ElementBase,
        key: str,
        value: str,
        schema_file: str,
        validator: Optional[Callable],
    ) -> None:
        """Helper method for setting XML attributes. Raises DocumentInvalid
        exception on inappropriate setting according to XSD schema."""
        if validator is not None:
            value = validator(value)
        element.set(key, str(value))
        schema = etree.XMLSchema(file=schema_file)
        schema.assertValid(element.getroottree())

    @staticmethod
    def set_attribute_list(
        element: etree.ElementBase, key: str, values: List[str], schema_file: str
    ) -> None:
        """Helper method for setting XML list attributes. Raises DocumentInvalid
        exception on inappropriate setting according to XSD schema."""
        for oldValue in DataHelper.get_element_list(element, key):
            element.remove(oldValue)
        elements = []
        for value in values:
            elements.append(
                etree.SubElement(element, f"{{{element.nsmap[None]}}}{key}")
            )
            elements[-1].text = value
        element.extend(elements)
        schema = etree.XMLSchema(file=schema_file)
        schema.assertValid(element.getroottree())

    @staticmethod
    def set_element_text(
        parent: etree.ElementBase, element: str, value: str, schema_file: str
    ) -> None:
        """Helper method for setting XML element text. Raises DocumentInvalid exception
        on inappropriate setting according to XSD schema."""
        DataHelper.get_element(parent, element).text = str(value)
        schema = etree.XMLSchema(file=schema_file)
        schema.assertValid(parent.getroottree())

    @staticmethod
    def get_element(parent: etree.ElementBase, element: str) -> etree.ElementBase:
        """Helper wrapper method for retrieving XML elements as custom
        Ecospold classes."""
        return parent.find(element, namespaces=parent.nsmap)

    @staticmethod
    def get_element_list(
        parent: etree.ElementBase, element: str
    ) -> List[etree.ElementBase]:
        """Helper wrapper method for retrieving XML list elements as a list
        of custom Ecospold classes."""
        return parent.findall(element, namespaces=parent.nsmap)

    @staticmethod
    def get_element_text(
        parent: etree.ElementBase, element: str, element_type: type = str
    ) -> str:
        """Helper wrapper method for retrieving XML element text as a string.
        Returns Defaults.TYPE_DEFAULTS[str] if no text exists or element is None."""
        return DataHelper.TYPE_FUNC_MAP.get(element_type, element_type)(
            getattr(
                DataHelper.get_element(parent, element),
                "text",
                str(Defaults.TYPE_DEFAULTS[str]),
            )
        )

    @staticmethod
    def get_inner_text_list(parent: etree.ElementBase, element: str):
        """Helper wrapper method for retrieving the list of last nodes in a chain
        of XML elements."""
        innerElements = DataHelper.get_element_list(parent, element)
        return [
            re.sub("[ ]{2,}", "", str(innerElement.text)).replace("\n", " ")
            for innerElement in innerElements
        ]

    @staticmethod
    def get_attribute(
        parent: etree.ElementBase, attribute: str, attr_type: type = str
    ) -> Any:
        """Helper wrapper method for retrieving XML attributes. Returns
        Defaults.TYPE_DEFAULTS[type] if attribute doesn't exist."""
        return DataHelper.TYPE_FUNC_MAP.get(attr_type, attr_type)(
            parent.get(attribute, Defaults.TYPE_DEFAULTS.get(attr_type, None))
        )

    @staticmethod
    def get_attribute_list(
        parent: etree.ElementBase, attribute: str, attr_type: type = str
    ) -> List[Any]:
        """Helper wrapper method for retrieving XML list attributes.
        Returns empty list if attributes don't exist."""
        return list(
            map(
                lambda x: DataHelper.TYPE_FUNC_MAP.get(attr_type, attr_type)(
                    re.sub("[\n]{1,}", " ", re.sub("[ ]{2,}", "", x.text))
                ),
                DataHelper.get_element_list(parent, attribute),
            )
        )

    @staticmethod
    def create_attribute_v1(
        name: str, attr_type: type, validator: Optional[Callable] = None
    ) -> property:
        """Helper wrapper method for creating setters and getters for a V1 attribute"""
        return DataHelper.create_attribute(
            name, attr_type, Defaults.SCHEMA_V1_FILE, validator
        )

    @staticmethod
    def create_attribute_v2(
        name: str, attr_type: type, validator: Optional[Callable] = None
    ) -> property:
        """Helper wrapper method for creating setters and getters for a V2 attribute"""
        return DataHelper.create_attribute(
            name, attr_type, Defaults.SCHEMA_V2_FILE, validator
        )

    @staticmethod
    def create_attribute(
        name: str,
        attr_type: type,
        schema_file: str,
        validator: Optional[Callable] = None,
    ) -> property:
        """Helper wrapper method for creating setters and getters for an attribute"""
        return property(
            fget=lambda self: DataHelper.get_attribute(self, name, attr_type),
            fset=lambda self, value: DataHelper.set_attribute(
                self, name, value, schema_file, validator
            ),
        )

    @staticmethod
    def create_attribute_list_v1(name: str, attr_type: type) -> property:
        """Helper wrapper method for creating setters and getters for
        a V1 attribute list"""
        return DataHelper.create_attribute_list(
            name, attr_type, Defaults.SCHEMA_V1_FILE
        )

    @staticmethod
    def create_attribute_list_v2(name: str, attr_type: type) -> property:
        """Helper wrapper method for creating setters and getters for
        a V2 attribute list"""
        return DataHelper.create_attribute_list(
            name, attr_type, Defaults.SCHEMA_V2_FILE
        )

    @staticmethod
    def create_attribute_list(name: str, attr_type: type, schema_file: str) -> property:
        """Helper wrapper method for creating setters and getters for
        an attribute list."""
        return property(
            fget=lambda self: DataHelper.get_attribute_list(self, name, attr_type),
            fset=lambda self, values: DataHelper.set_attribute_list(
                self, name, values, schema_file
            ),
        )

    @staticmethod
    def create_element_text_v1(name: str, element_type: type) -> property:
        """Helper wrapper method for creating setters and getters for
        a V1 element text"""
        return DataHelper.create_element_text(
            name, element_type, Defaults.SCHEMA_V1_FILE
        )

    @staticmethod
    def create_element_text_v2(name: str, element_type: type) -> property:
        """Helper wrapper method for creating setters and getters for
        a V2 element text"""
        return DataHelper.create_element_text(
            name, element_type, Defaults.SCHEMA_V2_FILE
        )

    @staticmethod
    def create_element_text(
        name: str, element_type: type, schema_file: str
    ) -> property:
        """Helper wrapper method for creating setters and getters for
        an element text."""
        return property(
            fget=lambda self: DataHelper.get_element_text(self, name, element_type),
            fset=lambda self, value: DataHelper.set_element_text(
                self, name, value, schema_file
            ),
        )

    @staticmethod
    def fill_in_defaults(node: etree.ElementBase) -> None:
        """Helper method for filling in defaults in all tree given any node."""
        root = node.getroottree()
        for child in root.iter():
            for defaults in [Defaults.STATIC_DEFAULTS, Defaults.DYNAMIC_DEFAULTS]:
                for key, value in defaults.get(child.__class__.__name__, {}).items():
                    if (
                        getattr(child, key, Defaults.TYPE_DEFAULTS[str])
                        in Defaults.TYPE_DEFAULTS.values()
                    ):
                        if isinstance(value, str):
                            setattr(child, key, value)
                        else:
                            setattr(child, key, value(child))
