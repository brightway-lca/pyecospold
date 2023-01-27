"""Test cases for the __model_v2__ module."""

import pytest

from pyecospold.core import parse_file_v2
from pyecospold.model_v2 import (
    Activity,
    ActivityDataset,
    ActivityDescription,
    AdministrativeInformation,
    Classification,
    Comment,
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

    assert isinstance(activityDescription.activity[0], Activity)
    assert isinstance(activityDescription.classification[0], Classification)
    assert isinstance(activityDescription.geography[0], Geography)
    assert isinstance(
        activityDescription.macroEconomicScenario[0], MacroEconomicScenario
    )
    assert isinstance(activityDescription.technology[0], Technology)
    assert isinstance(activityDescription.timePeriod[0], TimePeriod)


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
    generalCommentTexts = [
        "This data represents the production of 1 kg of formic acid "
        + "from methyl formate. Raw materials and energy consumptions are "
        + "modelled with literature data. The emissions are estimated. "
        + "Infrastructure is included with a default value.",
        "[This dataset was already contained in the ecoinvent database version 2. "
        + "It was not individually updated during the transfer to ecoinvent version 3. "
        + "Life Cycle Impact Assessment results may still have changed, as they are "
        + "affected by changes in the supply chain, i.e. in other datasets. This "
        + "dataset was generated following the ecoinvent quality guidelines for "
        + "version 2. It may have been subject to central changes described in the "
        + "ecoinvent version 3 change report "
        + "(http://www.ecoinvent.org/database/ecoinvent-version-3/reports-of-changes/),"
        + " and the results of the central updates were reviewed extensively. The "
        + "changes added e.g. consistent water flows and other information throughout "
        + "the database. The documentation of this dataset can be found in the "
        + "ecoinvent reports of version 2, which are still available via the ecoinvent "
        + "website. The change report linked above covers all central changes that were"
        + " made during the conversion process.]",
    ]
    generalCommentImageUrls = []
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
    activityId = "ffed8e5b-8ecb-4a93-bc79-a1404afd9fcd"
    activityNameId = "8b542688-aa36-45d5-b2f0-3b15ade03700"
    parentActivityId = "dca19657-6614-4b1d-98aa-0658dd2ced39"
    inheritanceDepth = 0
    inheritanceDepthStr = "not a child"
    activityType = 1
    typeStr = "Unit process"
    specialActivityType = 0
    specialActivityTypeStr = "ordinary transforming activity (default)"
    energyValues = 0
    energyValuesStr = "Undefined (default)"
    masterAllocationPropertyId = ""
    masterAllocationPropertyIdOverwrittenByChild = False
    masterAllocationPropertyContextId = ""
    datasetIcon = ""
    activity = eco_spold.childActivityDataset.activityDescription.activity[0]

    assert activity.allocationComment is None
    assert isinstance(activity.generalComment, Comment)
    assert activity.activityNames == activityNames
    assert activity.generalComment.texts == generalCommentTexts
    assert activity.generalComment.imageUrls == generalCommentImageUrls
    assert activity.includedActivitiesEnds == includedActivitiesEnds
    assert activity.includedActivitiesStarts == includedActivitiesStarts
    assert activity.synonyms == synonyms
    assert activity.tags == tags
    assert activity.id == activityId
    assert activity.activityNameId == activityNameId
    assert activity.parentActivityId == parentActivityId
    assert activity.inheritanceDepth == inheritanceDepth
    assert activity.inheritanceDepthStr == inheritanceDepthStr
    assert activity.type == activityType
    assert activity.typeStr == typeStr
    assert activity.specialActivityType == specialActivityType
    assert activity.specialActivityTypeStr == specialActivityTypeStr
    assert activity.energyValues == energyValues
    assert activity.energyValuesStr == energyValuesStr
    assert activity.masterAllocationPropertyId == masterAllocationPropertyId
    assert (
        activity.masterAllocationPropertyIdOverwrittenByChild
        == masterAllocationPropertyIdOverwrittenByChild
    )
    assert (
        activity.masterAllocationPropertyContextId == masterAllocationPropertyContextId
    )
    assert activity.datasetIcon == datasetIcon


def test_parse_file_v2_classification(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    classificationId = "7ac1cbc6-1385-4a68-8647-ed7aa78db201"
    classificationContextId = ""
    classificationSystem = "EcoSpold01Categories"
    classificationValue = "chemicals/organics"
    activityDescription = eco_spold.childActivityDataset.activityDescription
    classification = activityDescription.classification[0]

    assert classification.classificationId == classificationId
    assert classification.classificationContextId == classificationContextId
    assert classification.classificationSystem == classificationSystem
    assert classification.classificationValue == classificationValue


def test_parse_file_v2_geography(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    geographyId = "0723d252-7e2a-11de-9820-0019e336be3a"
    geographyContextId = ""
    shortNames = ["RER"]
    commentsTexts = ["The inventory is modelled for Europe."]
    commentsImageUrls = []
    activityDescription = eco_spold.childActivityDataset.activityDescription
    geography = activityDescription.geography[0]

    assert geography.geographyId == geographyId
    assert geography.geographyContextId == geographyContextId
    assert geography.shortNames == shortNames
    assert geography.comments[0].texts == commentsTexts
    assert geography.comments[0].imageUrls == commentsImageUrls


def test_parse_file_v2_technology(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    technologyLevel = 3
    technologyLevelStr = "Current (default)"
    commentsTexts = [
        "To keep undesirable reesterification as low as possible, the time of "
        + "direct contact between methanol and formic acid must be as short as "
        + "possible, and separation must be carried out at the lowest possible "
        + "temperature. Introduction of methyl formate into the lower part of "
        + "the column in which lower boiling methyl formate and methanol are "
        + "separated from water and formic acid, has also been suggested. This "
        + "largely prevents reesterification because of the excess methyl formate "
        + "present in the critical region of the column."
    ]
    commentsImageUrl = (
        "https://db3.ecoinvent.org/images/2ddc19c0-905f-42c3-b14c-e68332befec9"
    )
    activityDescription = eco_spold.childActivityDataset.activityDescription
    technology = activityDescription.technology[0]

    assert technology.technologyLevel == technologyLevel
    assert technology.technologyLevelStr == technologyLevelStr
    assert technology.comments[0].texts[0] == commentsTexts[0]
    assert technology.comments[0].imageUrls[0] == commentsImageUrl
