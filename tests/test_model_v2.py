"""Test cases for the __model_v2__ module."""

import pytest

from pyecospold.core import parse_file_v2
from pyecospold.model_v2 import (
    Activity,
    ActivityDataset,
    ActivityDescription,
    AdministrativeInformation,
    Classification,
    DataEntryBy,
    DataGeneratorAndPublication,
    EcoSpold,
    ElementaryExchange,
    FileAttributes,
    FlowData,
    Geography,
    IntermediateExchange,
    MacroEconomicScenario,
    ModellingAndValidation,
    Parameter,
    Representativeness,
    Technology,
    TimePeriod,
)


@pytest.fixture(name="eco_spold")
def _eco_spold() -> EcoSpold:
    return parse_file_v2("data/v2/v2_2.spold")


def test_parse_file_v2_eco_spold(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    assert isinstance(eco_spold, EcoSpold)
    assert isinstance(eco_spold.childActivityDataset, ActivityDataset)


def test_parse_file_v2_activity_dataset() -> None:
    """It parses attributes correctly."""
    ecoSpold = parse_file_v2("data/v2/v2_1.xml")
    activityDataset = ecoSpold.activityDataset

    assert isinstance(activityDataset.activityDescription, ActivityDescription)
    assert isinstance(
        activityDataset.administrativeInformation, AdministrativeInformation
    )
    assert isinstance(activityDataset.flowData, FlowData)
    assert isinstance(activityDataset.modellingAndValidation, ModellingAndValidation)


def test_parse_file_v2_child_activity_dataset(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    childActivityDataset = eco_spold.childActivityDataset

    assert isinstance(childActivityDataset.activityDescription, ActivityDescription)
    assert isinstance(
        childActivityDataset.administrativeInformation, AdministrativeInformation
    )
    assert isinstance(childActivityDataset.flowData, FlowData)
    assert isinstance(
        childActivityDataset.modellingAndValidation, ModellingAndValidation
    )


def test_parse_file_v2_activity_description(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    activityDescription = eco_spold.childActivityDataset.activityDescription

    assert isinstance(activityDescription.activity, Activity)
    assert isinstance(activityDescription.classification, Classification)
    assert isinstance(activityDescription.geography, Geography)
    assert isinstance(activityDescription.macroEconomicScenario, MacroEconomicScenario)
    assert isinstance(activityDescription.technology, Technology)
    assert isinstance(activityDescription.timePeriod, TimePeriod)


def test_parse_file_v2_flow_data(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    elementaryExchangesLen = 11
    intermediateExchangesLen = 41
    parametersLen = 6
    flowData = eco_spold.childActivityDataset.flowData

    assert isinstance(flowData.elementaryExchanges[0], ElementaryExchange)
    assert isinstance(flowData.intermediateExchanges[0], IntermediateExchange)
    assert isinstance(flowData.parameters[0], Parameter)

    assert len(flowData.elementaryExchanges) == elementaryExchangesLen
    assert len(flowData.intermediateExchanges) == intermediateExchangesLen
    assert len(flowData.parameters) == parametersLen


def test_parse_file_v2_modelling_and_validation(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    modellingAndValidation = eco_spold.childActivityDataset.modellingAndValidation

    assert isinstance(modellingAndValidation.representativeness, Representativeness)
    assert modellingAndValidation.review is None


def test_parse_file_v2_administrative_information(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    administrativeInformation = eco_spold.childActivityDataset.administrativeInformation

    assert isinstance(administrativeInformation.dataEntryBy, DataEntryBy)
    assert isinstance(
        administrativeInformation.dataGeneratorAndPublication,
        DataGeneratorAndPublication,
    )
    assert isinstance(administrativeInformation.fileAttributes, FileAttributes)


def test_parse_file_v2_activity(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    activityNames = ["formic acid production, methyl formate route"]
    allocationComments = []
    includedActivitiesEnds = [
        "This activity ends with 1 kg of formic acid, 100% af the factory gate. "
        "The dataset includes the input materials, energy uses, "
        "infrastructure and emissions."
    ]
    includedActivitiesStarts = [
        "From the reception of methyl formate at the factory gate."
    ]
    synonyms = ["methanoic acid"]
    tags = ["ConvertedDataset"]
    activity = eco_spold.childActivityDataset.activityDescription.activity

    assert activity.activityNames == activityNames
    assert activity.allocationComments == allocationComments
    # assert activity.generalComments == generalComments
    assert activity.includedActivitiesEnds == includedActivitiesEnds
    assert activity.includedActivitiesStarts == includedActivitiesStarts
    assert activity.synonyms == synonyms
    assert activity.tags == tags
