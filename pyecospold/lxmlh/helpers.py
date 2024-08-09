import re
from typing import Any, Callable, Dict, List, Optional

from lxml import etree

from .config import TYPE_DEFAULTS, TYPE_FUNC_MAP


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


def set_attribute_list(
    element: etree.ElementBase, key: str, values: List[Any], schema_file: str
) -> None:
    """Helper method for setting XML list attributes. Raises DocumentInvalid
    exception on inappropriate setting according to XSD schema."""
    for oldValue in get_element_list(element, key):
        element.remove(oldValue)
    elements = []
    nameSpace = element.nsmap.get(None, "")
    for value in values:
        elements.append(etree.SubElement(element, f"{{{nameSpace}}}{key}"))
        elements[-1].text = str(value)
    element.extend(elements)
    schema = etree.XMLSchema(file=schema_file)
    schema.assertValid(element.getroottree())


def set_element_text(
    parent: etree.ElementBase, element: str, value: str, schema_file: str
) -> None:
    """Helper method for setting XML element text. Raises DocumentInvalid exception
    on inappropriate setting according to XSD schema."""
    get_element(parent, element).text = str(value)
    schema = etree.XMLSchema(file=schema_file)
    schema.assertValid(parent.getroottree())


def get_element(parent: etree.ElementBase, element: str) -> etree.ElementBase:
    """Helper wrapper method for retrieving XML elements as custom XML classes."""
    return parent.find(element, namespaces=parent.nsmap)


def get_element_list(
    parent: etree.ElementBase, element: str
) -> List[etree.ElementBase]:
    """Helper wrapper method for retrieving XML list elements as a list
    of custom XML classes."""
    return parent.findall(element, namespaces=parent.nsmap)


def get_element_text(
    parent: etree.ElementBase, element: str, element_type: type = str
) -> str:
    """Helper wrapper method for retrieving XML element text as a string.
    Returns TYPE_DEFAULTS[str] if no text exists or element is None."""
    return TYPE_FUNC_MAP.get(element_type, element_type)(
        getattr(
            get_element(parent, element),
            "text",
            str(TYPE_DEFAULTS[str]),
        )
    )


def get_inner_text_list(parent: etree.ElementBase, element: str):
    """Helper wrapper method for retrieving the list of last nodes in a chain
    of XML elements."""
    innerElements = get_element_list(parent, element)
    return [
        re.sub("[ ]{2,}", "", str(innerElement.text)).replace("\n", " ")
        for innerElement in innerElements
    ]


def get_attribute(
    parent: etree.ElementBase, attribute: str, attr_type: type = str
) -> Any:
    """Helper wrapper method for retrieving XML attributes. Returns
    TYPE_DEFAULTS[type] if attribute doesn't exist."""
    return TYPE_FUNC_MAP.get(attr_type, attr_type)(
        parent.get(attribute, TYPE_DEFAULTS.get(attr_type, None))
    )


def get_attribute_list(
    parent: etree.ElementBase, attribute: str, attr_type: type = str
) -> List[Any]:
    """Helper wrapper method for retrieving XML list attributes.
    Returns empty list if attributes don't exist."""
    return list(
        map(
            lambda x: TYPE_FUNC_MAP.get(attr_type, attr_type)(
                re.sub("[\n]{1,}", " ", re.sub("[ ]{2,}", "", x.text))
            ),
            get_element_list(parent, attribute),
        )
    )


def create_attribute(
    name: str,
    attr_type: type,
    schema_file: str,
    validator: Optional[Callable] = None,
) -> property:
    """Helper wrapper method for creating setters and getters for an attribute"""
    return property(
        fget=lambda self: get_attribute(self, name, attr_type),
        fset=lambda self, value: set_attribute(
            self, name, value, schema_file, validator
        ),
    )


def create_element_text(name: str, element_type: type, schema_file: str) -> property:
    """Helper wrapper method for creating setters and getters for an element text."""
    return property(
        fget=lambda self: get_element_text(self, name, element_type),
        fset=lambda self, value: set_element_text(self, name, value, schema_file),
    )


def create_attribute_list(name: str, attr_type: type, schema_file: str) -> property:
    """Helper wrapper method for creating setters and getters for an attribute list."""
    return property(
        fget=lambda self: get_attribute_list(self, name, attr_type),
        fset=lambda self, values: set_attribute_list(self, name, values, schema_file),
    )


def fill_in_defaults(
    node: etree.ElementBase,
    static_defaults: Dict[str, Dict[str, str]],
    dynamic_defaults: Dict[str, Dict[str, Callable[[etree.ElementBase], str]]],
) -> None:
    """Helper method for filling in defaults in all tree given any node."""
    root = node.getroottree()
    for child in root.iter():
        for defaults in [static_defaults, dynamic_defaults]:
            for key, value in defaults.get(child.__class__.__name__, {}).items():
                if getattr(child, key, TYPE_DEFAULTS[str]) in TYPE_DEFAULTS.values():
                    if isinstance(value, str):
                        setattr(child, key, value)
                    else:
                        setattr(child, key, value(child))
