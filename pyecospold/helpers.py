import logging

from lxml import etree


class DataTypesConverter:
    timestampFormat = "%Y-%m-%dT%H:%M:%S"

    @staticmethod
    def str_to_bool(string: str) -> bool:
        return string.lower() == "true"


class DataValidator:
    schema = etree.XMLSchema(file="data/schema/EcoSpold01Dataset.xsd")

    @staticmethod
    def try_set(element: etree.ElementBase, key: str, value: str) -> bool:
        current_value = getattr(element, key)
        element.set(key, str(value))

        validation = DataValidator.schema.validate(element.getroottree())
        if validation:
            return True

        element.set(key, str(current_value))
        logging.warning(
            f"Can't set property {element.__class__.__name__}.{key} "
            f"of type {type(current_value)} to: {value}"
        )
        return False
