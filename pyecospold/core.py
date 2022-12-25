from lxml import etree, objectify

from pyecospold.model import (EcoSpold, Dataset, MetaInformation, FlowData,
                              ProcessInformation, ModellingAndValidation,
                              AdministrativeInformation, ReferenceFunction,
                              Geography, Technology, TimePeriod,
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


def parse_file(path: str) -> EcoSpold:
    parser = objectify.makeparser()
    parser.set_element_class_lookup(EcospoldLookup())
    return objectify.parse(path, parser).getroot()


def save_file(root: etree.ElementBase, path: str) -> None:
    etree.ElementTree(root).write(path, pretty_print=True)
