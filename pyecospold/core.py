"""Core Ecospold module containing parsing and saving functionalities."""
from lxml import etree, objectify

from .config import Defaults
from .model import (
    AdministrativeInformation,
    Allocation,
    DataEntryBy,
    DataGeneratorAndPublication,
    Dataset,
    DataSetInformation,
    EcoSpold,
    Exchange,
    FlowData,
    Geography,
    MetaInformation,
    ModellingAndValidation,
    Person,
    ProcessInformation,
    ReferenceFunction,
    Representativeness,
    Source,
    Technology,
    TimePeriod,
    Validation,
)


class EcospoldLookup(etree.CustomElementClassLookup):
    """Custom XML lookup class for Ecospold files."""

    def lookup(self, unused_node_type, unused_document, unused_namespace, name):
        """Maps Ecospold XML elements to custom Ecospold classes."""
        lookupmap = {
            "ecoSpold": EcoSpold,
            "dataset": Dataset,
            "metaInformation": MetaInformation,
            "flowData": FlowData,
            "processInformation": ProcessInformation,
            "modellingAndValidation": ModellingAndValidation,
            "administrativeInformation": AdministrativeInformation,
            "exchange": Exchange,
            "allocation": Allocation,
            "referenceFunction": ReferenceFunction,
            "geography": Geography,
            "technology": Technology,
            "timePeriod": TimePeriod,
            "dataSetInformation": DataSetInformation,
            "representativeness": Representativeness,
            "source": Source,
            "validation": Validation,
            "dataEntryBy": DataEntryBy,
            "dataGeneratorAndPublication": DataGeneratorAndPublication,
            "person": Person,
        }
        try:
            return lookupmap[name]
        except KeyError:
            return None


def parse_file(
    file_path: str, schema_path: str = Defaults.SCHEMA_FILE
) -> EcoSpold:
    """Parses an Ecospold XML file to custom Ecospold classes.

    Parameters:
    file_path: the path to the Ecospold XML file.
    schema_path: the path to the Ecospold XSD schema file.

    Returns and EcoSpold class representing the root of the XML file.
    """
    schema = etree.XMLSchema(file=schema_path)
    parser = objectify.makeparser(schema=schema)
    parser.set_element_class_lookup(EcospoldLookup())
    return objectify.parse(file_path, parser).getroot()


def save_file(root: EcoSpold, path: str) -> None:
    """Saves an Ecospold class to an XML file.

    Parameters:
    root: the EcoSpold class representing the root of the XML file.
    path: the path to save the Ecospold XML file.
    """
    root = etree.ElementTree(root)
    root.write(path, pretty_print=True, xml_declaration=True, encoding="UTF-8")
