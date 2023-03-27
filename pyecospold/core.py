"""Core Ecospold module containing parsing and saving functionalities."""
from io import StringIO
from pathlib import Path
from typing import List, Tuple, Union

from lxml import etree
from lxmlh.parsers import parse_directory, parse_file, save_file, validate_file

from .config import Defaults
from .model_v1 import AdministrativeInformation as AdministrativeInformationV1
from .model_v1 import Allocation
from .model_v1 import DataEntryBy as DataEntryByV1
from .model_v1 import DataGeneratorAndPublication as DataGeneratorAndPublicationV1
from .model_v1 import Dataset, DataSetInformation
from .model_v1 import EcoSpold as EcoSpoldV1
from .model_v1 import Exchange
from .model_v1 import FlowData as FlowDataV1
from .model_v1 import Geography as GeographyV1
from .model_v1 import MetaInformation
from .model_v1 import ModellingAndValidation as ModellingAndValidationV1
from .model_v1 import Person, ProcessInformation, ReferenceFunction
from .model_v1 import Representativeness as RepresentativenessV1
from .model_v1 import Source
from .model_v1 import Technology as TechnologyV1
from .model_v1 import TimePeriod as TimePeriodV1
from .model_v1 import Validation
from .model_v2 import Activity, ActivityDataset, ActivityDescription
from .model_v2 import AdministrativeInformation as AdministrativeInformationV2
from .model_v2 import Beta, Classification, Compartment
from .model_v2 import DataEntryBy as DataEntryByV2
from .model_v2 import DataGeneratorAndPublication as DataGeneratorAndPublicationV2
from .model_v2 import EcoSpold as EcoSpoldV2
from .model_v2 import ElementaryExchange, FileAttributes
from .model_v2 import FlowData as FlowDataV2
from .model_v2 import Gamma
from .model_v2 import Geography as GeographyV2
from .model_v2 import (
    ImpactIndicator,
    IntermediateExchange,
    Lognormal,
    MacroEconomicScenario,
)
from .model_v2 import ModellingAndValidation as ModellingAndValidationV2
from .model_v2 import Normal, Parameter, PedigreeMatrix, Property
from .model_v2 import Representativeness as RepresentativenessV2
from .model_v2 import RequiredContextReference, Review
from .model_v2 import Technology as TechnologyV2
from .model_v2 import TextAndImage
from .model_v2 import TimePeriod as TimePeriodV2
from .model_v2 import TransferCoefficient, Triangular, Uncertainty, Uniform


class EcospoldLookupV1(etree.CustomElementClassLookup):
    """Custom XML lookup class for Ecospold V1 files."""

    def lookup(self, unused_node_type, unused_document, unused_namespace, name):
        """Maps Ecospold XML elements to custom Ecospold classes."""
        lookupmap = {
            "administrativeInformation": AdministrativeInformationV1,
            "allocation": Allocation,
            "dataEntryBy": DataEntryByV1,
            "dataGeneratorAndPublication": DataGeneratorAndPublicationV1,
            "dataset": Dataset,
            "dataSetInformation": DataSetInformation,
            "ecoSpold": EcoSpoldV1,
            "exchange": Exchange,
            "flowData": FlowDataV1,
            "geography": GeographyV1,
            "metaInformation": MetaInformation,
            "modellingAndValidation": ModellingAndValidationV1,
            "person": Person,
            "processInformation": ProcessInformation,
            "referenceFunction": ReferenceFunction,
            "representativeness": RepresentativenessV1,
            "source": Source,
            "technology": TechnologyV1,
            "timePeriod": TimePeriodV1,
            "validation": Validation,
        }
        try:
            return lookupmap[name]
        except KeyError:
            return None


class EcospoldLookupV2(etree.CustomElementClassLookup):
    """Custom XML lookup class for Ecospold V2 files."""

    def lookup(self, unused_node_type, unused_document, unused_namespace, name):
        """Maps Ecospold XML elements to custom Ecospold classes."""
        lookupmap = {
            "activity": Activity,
            "activityDataset": ActivityDataset,
            "activityDescription": ActivityDescription,
            "administrativeInformation": AdministrativeInformationV2,
            "allocationComment": TextAndImage,
            "childActivityDataset": ActivityDataset,
            "beta": Beta,
            "classification": Classification,
            "comment": TextAndImage,
            "compartment": Compartment,
            "dataEntryBy": DataEntryByV2,
            "dataGeneratorAndPublication": DataGeneratorAndPublicationV2,
            "ecoSpold": EcoSpoldV2,
            "elementaryExchange": ElementaryExchange,
            "fileAttributes": FileAttributes,
            "flowData": FlowDataV2,
            "generalComment": TextAndImage,
            "gamma": Gamma,
            "geography": GeographyV2,
            "impactIndicator": ImpactIndicator,
            "intermediateExchange": IntermediateExchange,
            "lognormal": Lognormal,
            "macroEconomicScenario": MacroEconomicScenario,
            "modellingAndValidation": ModellingAndValidationV2,
            "normal": Normal,
            "parameter": Parameter,
            "pedigreeMatrix": PedigreeMatrix,
            "property": Property,
            "representativeness": RepresentativenessV2,
            "requiredContexts": RequiredContextReference,
            "review": Review,
            "technology": TechnologyV2,
            "timePeriod": TimePeriodV2,
            "transferCoefficient": TransferCoefficient,
            "triangular": Triangular,
            "uncertainty": Uncertainty,
            "uniform": Uniform,
        }
        try:
            return lookupmap[name]
        except KeyError:
            return None


def parse_file_v1(file: Union[str, Path, StringIO]) -> EcoSpoldV1:
    """Parses an Ecospold V1 XML file to custom Ecospold classes.

    Parameters:
    file: the str|Path path to the Ecospold XML file or its StringIO representation.

    Returns an EcoSpold class representing the root of the XML file.
    """
    return parse_file(file, Defaults.SCHEMA_V1_FILE, EcospoldLookupV1())


def parse_file_v2(file: Union[str, Path, StringIO]) -> EcoSpoldV2:
    """Parses an Ecospold V2 XML file to custom Ecospold classes.

    Parameters:
    file: the str|Path path to the Ecospold XML file or its StringIO representation.

    Returns an EcoSpold class representing the root of the XML file.
    """
    return parse_file(file, Defaults.SCHEMA_V2_FILE, EcospoldLookupV2())


def validate_file_v1(file: Union[str, Path, StringIO]) -> Union[None, List[str]]:
    """Validates an Ecospold V1 XML file to custom Ecospold classes.

    Parameters:
    file: the str|Path path to the Ecospold XML file or its StringIO representation.

    Returns ``None`` if valid or a list of error strings.
    """
    return validate_file(file, Defaults.SCHEMA_V1_FILE)


def validate_file_v2(file: Union[str, Path, StringIO]) -> Union[None, List[str]]:
    """Parses an Ecospold V2 XML file to custom Ecospold classes.

    Parameters:
    file: the str|Path path to the Ecospold XML file or its StringIO representation.

    Returns ``None`` if valid or a list of error strings.
    """
    return validate_file(file, Defaults.SCHEMA_V2_FILE)


def parse_directory_v1(
    dir_path: Union[str, Path], valid_suffixes: Union[List[str], None] = None
) -> List[Tuple[Path, EcoSpoldV1]]:
    """Parses a directory of Ecospold XML files to a list of custom Ecospold classes.

    Parameters:
    dir_path: the directory path, should contain files of version 1 of EcoSpold.
    valid_suffixes: a list of valid file suffixes which will only be considered for
    parsing. If None, defaults to [".xml", ".spold"].

    Returns a list of tuples of file paths and corresponding EcoSpold classes
    representing the root of the XML file.
    """
    return parse_directory(
        dir_path=dir_path,
        schema_path=Defaults.SCHEMA_V1_FILE,
        lookup=EcospoldLookupV1(),
        valid_suffixes=valid_suffixes,
    )


def parse_directory_v2(
    dir_path: Union[str, Path], valid_suffixes: Union[List[str], None] = None
) -> List[Tuple[Path, EcoSpoldV2]]:
    """Parses a directory of Ecospold XML files to a list of custom Ecospold classes.

    Parameters:
    dir_path: the directory path, should contain files of version 2 of EcoSpold.
    valid_suffixes: a list of valid file suffixes which will only be considered for
    parsing. If None, defaults to [".xml", ".spold"].

    Returns a list of tuples of file paths and corresponding EcoSpold classes
    representing the root of the XML file.
    """
    return parse_directory(
        dir_path=dir_path,
        schema_path=Defaults.SCHEMA_V2_FILE,
        lookup=EcospoldLookupV2(),
        valid_suffixes=valid_suffixes,
    )


def save_ecopsold_file(
    root: etree.ElementBase, path: str, fill_defaults: bool = False
) -> None:
    """Saves an Ecospold class to an XML file.

    Parameters:
    root: the EcoSpold class representing the root of the XML file.
    path: the path to save the Ecospold XML file.
    fill_defaults: whether to fill defaults values for attributes or not.
    """
    if not fill_defaults:
        staticDefaults = None
        dynamicDefaults = None
    else:
        staticDefaults = Defaults.STATIC_DEFAULTS
        dynamicDefaults = Defaults.DYNAMIC_DEFAULTS

    save_file(
        root, path, static_defaults=staticDefaults, dynamic_defaults=dynamicDefaults
    )
