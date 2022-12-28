from lxml import etree, objectify

from .model import (EcoSpold, Dataset, MetaInformation, FlowData,
                    ProcessInformation, ModellingAndValidation,
                    AdministrativeInformation, Exchange, Allocation,
                    ReferenceFunction, Geography, Technology, TimePeriod,
                    DataSetInformation, Representativeness,
                    Source, Validation, DataEntryBy,
                    DataGeneratorAndPublication, Person)


class EcospoldLookup(etree.CustomElementClassLookup):
    def lookup(self, node_type, document, namespace, name):
        lookupmap = {
            "ecoSpold": EcoSpold,
            "dataset": Dataset,
            "metaInformation": MetaInformation,
            "flowData": FlowData,
            "processInformation" : ProcessInformation,
            "modellingAndValidation": ModellingAndValidation,
            "administrativeInformation": AdministrativeInformation,
            "exchange": Exchange,
            "allocation": Allocation,
            "referenceFunction" : ReferenceFunction,
            "geography": Geography,
            "technology": Technology,
            "timePeriod": TimePeriod,
            "dataSetInformation": DataSetInformation,
            "representativeness": Representativeness,
            "source": Source,
            "validation": Validation,
            "dataEntryBy": DataEntryBy,
            "dataGeneratorAndPublication": DataGeneratorAndPublication,
            "person": Person
        }
        try:
            return lookupmap[name]
        except KeyError:
            return None


def parse_file(
    file_path: str, schema_path: str = "data/schema/EcoSpold01Dataset.xsd"
) -> EcoSpold:
    schema = etree.XMLSchema(file=schema_path)
    parser = objectify.makeparser(schema=schema)
    parser.set_element_class_lookup(EcospoldLookup())
    return objectify.parse(file_path, parser).getroot()


def save_file(root: etree.ElementBase, path: str) -> None:
    root = etree.ElementTree(root)
    root.write(path, pretty_print=True, xml_declaration=True, encoding="UTF-8")
