from lxml import etree, objectify

# TODO: sort me
from pyecospold.model import (EcoSpold, Dataset, FlowData, MetaInformation,
                              ProcessInformation,
                              ReferenceFunction, Geography, Technology,
                              DataSetInformation, Validation, Source,
                              DataGeneratorAndPublication, Representativeness,
                              TimePeriod, DataEntryBy, ModellingAndValidation,
                              AdministrativeInformation, Person)


class EcospoldLookup(etree.CustomElementClassLookup):
    def lookup(self, node_type, document, namespace, name):
        # TODO: sort me
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
            "dataSetInformation": DataSetInformation,
            "validation": Validation,
            "source": Source,
            "dataGeneratorAndPublication": DataGeneratorAndPublication,
            "representativeness": Representativeness,
            "timePeriod": TimePeriod,
            "dataEntryBy": DataEntryBy,
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
