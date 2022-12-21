import argparse
import configparser

from lxml import etree, objectify

from .config import Defaults
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input_file", help="Path to the xml input file.",
        type=str, required=True
    )
    parser.add_argument(
        "-c", "--config_file", help="Path to the ini config file.",
        type=str, default="config.ini"
    )
    pargs = parser.parse_args()

    config = configparser.ConfigParser()
    config.read(pargs.config_file)
    defaults = dict(config["defaults"])
    Defaults.set_defaults(defaults)

    parse_file(pargs.input_file)
