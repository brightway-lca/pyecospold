"""Internal helper classes."""
from typing import Callable, Optional

from lxmlh import create_attribute, create_attribute_list, create_element_text

from .config import Defaults


def create_attribute_v1(
    name: str, attr_type: type, validator: Optional[Callable] = None
) -> property:
    """Helper wrapper method for creating setters and getters for a V1 attribute"""
    return create_attribute(name, attr_type, Defaults.SCHEMA_V1_FILE, validator)


def create_attribute_v2(
    name: str, attr_type: type, validator: Optional[Callable] = None
) -> property:
    """Helper wrapper method for creating setters and getters for a V2 attribute"""
    return create_attribute(name, attr_type, Defaults.SCHEMA_V2_FILE, validator)


def create_attribute_list_v1(name: str, attr_type: type) -> property:
    """Helper wrapper method for creating setters and getters for
    a V1 attribute list"""
    return create_attribute_list(name, attr_type, Defaults.SCHEMA_V1_FILE)


def create_attribute_list_v2(name: str, attr_type: type) -> property:
    """Helper wrapper method for creating setters and getters for
    a V2 attribute list"""
    return create_attribute_list(name, attr_type, Defaults.SCHEMA_V2_FILE)


def create_element_text_v1(name: str, element_type: type) -> property:
    """Helper wrapper method for creating setters and getters for
    a V1 element text"""
    return create_element_text(name, element_type, Defaults.SCHEMA_V1_FILE)


def create_element_text_v2(name: str, element_type: type) -> property:
    """Helper wrapper method for creating setters and getters for
    a V2 element text"""
    return create_element_text(name, element_type, Defaults.SCHEMA_V2_FILE)
