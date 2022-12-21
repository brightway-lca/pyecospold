from lxml import etree, objectify

from .model import (MetaInformation, ProcessInformation, ReferenceFunction,
                    Geography, Technology, DataSetInformation, Validation,
                    Source, DataGeneratorAndPublication, Representativeness,
                    TimePeriod, DataEntryBy)


class EcospoldLookup(etree.CustomElementClassLookup):
    def lookup(self, node_type, document, namespace, name):
        lookupmap = {
            "metaInformation": MetaInformation,
            "processInformation" : ProcessInformation,
            "referenceFunction" : ReferenceFunction,
            "geography": Geography,
            "technology": Technology,
            "dataSetInformation": DataSetInformation,
            "validation": Validation,
            "source": Source,
            "dataGeneratorAndPublication": DataGeneratorAndPublication,
            "representativeness": Representativeness,
            "timePeriod": TimePeriod,
            "dataEntryBy": DataEntryBy
        }
        try:
            return lookupmap[name]
        except KeyError:
            return None


def parse_file(path: str) -> ProcessInformation:
    parser = objectify.makeparser()
    parser.set_element_class_lookup(EcospoldLookup())
    return objectify.parse(path, parser).getroot()


def save_file(root: etree.ElementBase, path: str) -> None:
    etree.ElementTree(root).write(path, pretty_print=True)
