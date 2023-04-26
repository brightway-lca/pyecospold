"""Test cases for the __model_v2__ module."""

from datetime import datetime

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
    TextAndImage,
    TimePeriod,
    Uncertainty,
)


@pytest.fixture(name="eco_spold")
def _eco_spold() -> EcoSpold:
    return parse_file_v2("data/v2/v2_2.spold")


def test_parse_file_v2_eco_spold(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    assert isinstance(eco_spold, EcoSpold)
    assert isinstance(eco_spold.activityDataset, ActivityDataset)


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
    activityDataset = eco_spold.activityDataset

    assert isinstance(activityDataset.activityDescription, ActivityDescription)
    assert isinstance(
        activityDataset.administrativeInformation, AdministrativeInformation
    )
    assert isinstance(activityDataset.flowData, FlowData)
    assert isinstance(activityDataset.modellingAndValidation, ModellingAndValidation)


def test_parse_file_v2_activity_description(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    activityDescription = eco_spold.activityDataset.activityDescription

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
    impactIndicatorsLen = 0
    flowData = eco_spold.activityDataset.flowData

    assert isinstance(flowData.elementaryExchanges[0], ElementaryExchange)
    assert isinstance(flowData.intermediateExchanges[0], IntermediateExchange)
    assert isinstance(flowData.parameters[0], Parameter)

    assert len(flowData.elementaryExchanges) == elementaryExchangesLen
    assert len(flowData.intermediateExchanges) == intermediateExchangesLen
    assert len(flowData.parameters) == parametersLen
    assert len(flowData.impactIndicators) == impactIndicatorsLen


def test_parse_file_v2_modelling_and_validation(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    modellingAndValidation = eco_spold.activityDataset.modellingAndValidation

    assert isinstance(modellingAndValidation.representativeness, Representativeness)
    assert modellingAndValidation.review is None


def test_parse_file_v2_administrative_information(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    administrativeInformation = eco_spold.activityDataset.administrativeInformation

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
    activity = eco_spold.activityDataset.activityDescription.activity[0]

    assert activity.allocationComment is None
    assert isinstance(activity.generalComment, TextAndImage)
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
    activityDescription = eco_spold.activityDataset.activityDescription
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
    activityDescription = eco_spold.activityDataset.activityDescription
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
    activityDescription = eco_spold.activityDataset.activityDescription
    technology = activityDescription.technology[0]

    assert technology.technologyLevel == technologyLevel
    assert technology.technologyLevelStr == technologyLevelStr
    assert technology.comments[0].texts[0] == commentsTexts[0]
    assert technology.comments[0].imageUrls[0] == commentsImageUrl


def test_parse_file_v2_time_period(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    startDate = "1984-01-01"
    endDate = "2014-12-31"
    isDataValidForEntirePeriod = True
    commentsTexts = ["Time of publications"]
    imageUrls = []
    activityDescription = eco_spold.activityDataset.activityDescription
    timePeriod = activityDescription.timePeriod[0]

    assert timePeriod.startDate == startDate
    assert timePeriod.endDate == endDate
    assert timePeriod.isDataValidForEntirePeriod == isDataValidForEntirePeriod
    assert timePeriod.comments[0].texts == commentsTexts
    assert timePeriod.comments[0].imageUrls == imageUrls


def test_parse_file_v2_macro_economic_scenario(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    macroEconomicScenarioId = "d9f57f0a-a01f-42eb-a57b-8f18d6635801"
    macroEconomicScenarioContextId = ""
    names = ["Business-as-Usual"]
    comments = []
    activityDescription = eco_spold.activityDataset.activityDescription
    macroEconomicScenario = activityDescription.macroEconomicScenario[0]

    assert macroEconomicScenario.macroEconomicScenarioId == macroEconomicScenarioId
    assert (
        macroEconomicScenario.macroEconomicScenarioContextId
        == macroEconomicScenarioContextId
    )
    assert macroEconomicScenario.names == names
    assert macroEconomicScenario.comments == comments


def test_parse_file_v2_intermediate_exchange(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    exchangeID = "336dd4ef-cece-4c49-b412-5fe565ec8b8f"
    unitId = "980b811e-3905-4797-82a5-173f5568bc7e"
    amount = 0
    productionVolumeAmount = 0
    names = ["heat, district or industrial, natural gas"]
    unitNames = ["MJ"]
    comments = ["Literature value."]
    intermediateExchangeId = "1125e767-7b5d-442e-81d6-9b0d3e1919ac"
    group = 5
    groupStr = "From Technosphere (unspecified)"
    outGroup = 0
    outGroupStr = "ReferenceProduct"
    classificationsLen = 1
    productionVolumeUncertaintiesLen = 0
    intermediateExchanges = eco_spold.activityDataset.flowData.intermediateExchanges
    intermediateExchange = intermediateExchanges[1]
    intermediateExchangeOut = intermediateExchanges[6]

    assert intermediateExchange.id == exchangeID
    assert intermediateExchange.unitId == unitId
    assert intermediateExchange.amount == amount
    assert intermediateExchange.productionVolumeAmount == productionVolumeAmount
    assert intermediateExchange.intermediateExchangeId == intermediateExchangeId
    assert intermediateExchange.group == group
    assert intermediateExchange.groupStr == groupStr
    assert intermediateExchange.names == names
    assert intermediateExchange.unitNames == unitNames
    assert intermediateExchange.comments == comments

    assert intermediateExchangeOut.group == outGroup
    assert intermediateExchangeOut.groupStr == outGroupStr

    assert isinstance(intermediateExchange.uncertainties[0], Uncertainty)
    assert len(intermediateExchange.classifications) == classificationsLen
    assert (
        len(intermediateExchange.productionVolumeUncertainties)
        == productionVolumeUncertaintiesLen
    )


def test_parse_file_v2_elementary_exchange(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    exchangeID = "719770d0-4b1e-4c44-bd9e-72c4687a6ee0"
    unitId = "487df68b-4994-4027-8fdc-a4dc298257b7"
    amount = 0.0011
    isCalculatedAmount = False
    sourceIdOverwrittenByChild = False
    specificAllocationPropertyId = ""
    specificAllocationPropertyIdOverwrittenByChild = False
    specificAllocationPropertyContextId = ""
    elementaryExchangeId = "70d467b6-115e-43c5-add2-441de9411348"
    names = ["BOD5, Biological Oxygen Demand"]
    unitNames = ["kg"]
    comments = [
        "Calculation. This value was calculated from the amount of methyl formate in "
        + "the treated waste water assuming a carbon conversion of 96% for COD. "
        + "The worst case scenario, BOD=COD, was used. "
        + "It is assumed that the manufacturing plant is located in an "
        + "urban/industrial area and consequently the emissions are categorised as "
        + "emanating in a high population density area. The emissions into water are "
        + "assumed to be emitted into rivers."
    ]
    group = 4
    groupStr = "ToEnvironment"
    inGroup = 4
    inGroupStr = "FromEnvironment"
    synonyms = []
    tags = []
    propertiesLen = 0
    transferCoefficientsLen = 0
    elementaryExchanges = eco_spold.activityDataset.flowData.elementaryExchanges
    elementaryExchange = elementaryExchanges[0]
    elementaryExchangeIn = elementaryExchanges[1]

    assert elementaryExchange.id == exchangeID
    assert elementaryExchange.unitId == unitId
    assert elementaryExchange.amount == amount
    assert elementaryExchange.isCalculatedAmount == isCalculatedAmount
    assert elementaryExchange.sourceIdOverwrittenByChild == sourceIdOverwrittenByChild
    assert (
        elementaryExchange.specificAllocationPropertyId == specificAllocationPropertyId
    )
    assert (
        elementaryExchange.specificAllocationPropertyIdOverwrittenByChild
        == specificAllocationPropertyIdOverwrittenByChild
    )
    assert (
        elementaryExchange.specificAllocationPropertyContextId
        == specificAllocationPropertyContextId
    )
    assert elementaryExchange.elementaryExchangeId == elementaryExchangeId
    assert elementaryExchange.names == names
    assert elementaryExchange.unitNames == unitNames
    assert elementaryExchange.comments == comments
    assert elementaryExchange.group == group
    assert elementaryExchange.groupStr == groupStr
    assert elementaryExchange.synonyms == synonyms
    assert elementaryExchange.tags == tags

    assert elementaryExchangeIn.group == inGroup
    assert elementaryExchangeIn.groupStr == inGroupStr

    assert isinstance(elementaryExchange.uncertainties[0], Uncertainty)
    assert len(elementaryExchange.properties) == propertiesLen
    assert len(elementaryExchange.transferCoefficients) == transferCoefficientsLen


def test_parse_file_v2_uncertainty(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    flowData = eco_spold.activityDataset.flowData
    uncertainty = flowData.intermediateExchanges[1].uncertainties[0]

    assert uncertainty.triangular is None
    assert uncertainty.uniform is None
    assert uncertainty.beta is None
    assert uncertainty.gamma is None
    assert uncertainty.binomial is None
    assert uncertainty.undefined is None


def test_parse_file_v2_normal(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    meanValue = 0
    variance = 0
    varianceWithPedigreeUncertainty = 0
    flowData = eco_spold.activityDataset.flowData
    uncertainty = flowData.intermediateExchanges[1].uncertainties[0]
    normal = uncertainty.normal

    assert normal.meanValue == meanValue
    assert normal.variance == variance
    assert normal.varianceWithPedigreeUncertainty == varianceWithPedigreeUncertainty


def test_parse_file_v2_lognormal(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    meanValue = 0.6
    _mu = -0.51
    variance = 0.03
    varianceWithPedigreeUncertainty = 0.0707
    flowData = eco_spold.activityDataset.flowData
    uncertainty = flowData.intermediateExchanges[0].uncertainties[0]
    lognormal = uncertainty.lognormal

    assert lognormal.meanValue == meanValue
    assert lognormal.mu == _mu
    assert lognormal.variance == variance
    assert lognormal.varianceWithPedigreeUncertainty == varianceWithPedigreeUncertainty


def test_parse_file_v2_property(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    propertyId = "c74c3729-e577-4081-b572-a283d2561a75"
    amount = 0.4
    isDefiningValue = True
    unitId = "577e242a-461f-44a7-922c-d8e1c3d2bf45"
    names = ["carbon content, fossil"]
    unitNames = ["dimensionless"]
    comments = ["CH2O"]
    uncertaintiesLen = 0
    flowData = eco_spold.activityDataset.flowData
    prop = flowData.intermediateExchanges[6].properties[0]

    assert prop.propertyId == propertyId
    assert prop.amount == amount
    assert prop.isDefiningValue == isDefiningValue
    assert prop.unitId == unitId
    assert prop.names == names
    assert prop.unitNames == unitNames
    assert prop.comments == comments
    assert len(prop.uncertainties) == uncertaintiesLen


def test_parse_file_v2_compartment(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    subCompartmentId = "963f8022-3e2e-4be9-ad4d-b3b7a2282099"
    compartments = ["water"]
    subCompartments = ["surface water"]
    flowData = eco_spold.activityDataset.flowData
    compartment = flowData.elementaryExchanges[0].compartment

    assert compartment.subCompartmentId == subCompartmentId
    assert compartment.compartments == compartments
    assert compartment.subCompartments == subCompartments


def test_parse_file_v2_parameter(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    parameterId = "e952df4c-1ca5-4710-9f53-be47be9191c1"
    variableName = "fraction_CW_R_to_air"
    amount = 0.771
    names = ["fraction, cooling water, recirculating system, to air"]
    comments = [
        "Calculated based on literature value (Scown, C.D., 2011, Water Footprint "
        + "of U.S. Transportation Fuels and supplying information of the article) "
        + "(Vionnet, S., Quantis Water Database - Technical Report, 2012). "
    ]
    meanValue = 0.771
    _mu = -0.26
    variance = 0.04
    varianceWithPedigreeUncertainty = 0.0413
    flowData = eco_spold.activityDataset.flowData
    parameter = flowData.parameters[0]
    lognormal = parameter.uncertainties[0].lognormal

    assert parameter.parameterId == parameterId
    assert parameter.variableName == variableName
    assert parameter.amount == amount
    assert parameter.names == names
    assert parameter.comments == comments

    assert lognormal.meanValue == meanValue
    assert lognormal.mu == _mu
    assert lognormal.variance == variance
    assert lognormal.varianceWithPedigreeUncertainty == varianceWithPedigreeUncertainty


def test_parse_file_v2_representativeness(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    percent = 100
    systemModelId = "06590a66-662a-4885-8494-ad0cf410f956"
    systemModelNames = ["Allocation, ecoinvent default"]
    samplingProcedures = ["Literature data"]
    extrapolations = [
        "This dataset has been extrapolated from year 2006 to the year of the "
        "calculation (2014). The uncertainty has been adjusted accordingly."
    ]
    modellingAndValidation = eco_spold.activityDataset.modellingAndValidation
    representativeness = modellingAndValidation.representativeness

    assert representativeness.percent == percent
    assert representativeness.systemModelId == systemModelId
    assert representativeness.systemModelNames == systemModelNames
    assert representativeness.samplingProcedures == samplingProcedures
    assert representativeness.extrapolations == extrapolations


def test_parse_file_v2_data_entry_by(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    personId = "4e412379-4901-477d-bbc1-3e2797ab9350"
    isActiveAuthor = False
    personName = "personName"
    personEmail = "personEmail@domain.com"
    administrativeInformation = eco_spold.activityDataset.administrativeInformation
    dataEntryBy = administrativeInformation.dataEntryBy

    assert dataEntryBy.personId == personId
    assert dataEntryBy.isActiveAuthor == isActiveAuthor
    assert dataEntryBy.personName == personName
    assert dataEntryBy.personEmail == personEmail


def test_parse_file_v2_data_generator_and_publication(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    personId = "4e412379-4901-477d-bbc1-3e2797ab9350"
    personName = "personName"
    personEmail = "personEmail@domain.com"
    dataPublishedIn = 2
    dataPublishedInStr = (
        "Data has been published entirely in 'referenceToPublishedSource'."
    )
    publishedSourceId = "71272329-1b17-415b-9f9b-299ebfbce109"
    publishedSourceYear = "2007"
    publishedSourceFirstAuthor = "Sutter, J."
    isCopyrightProtected = True
    pageNumbers = "solvents"
    accessRestrictedTo = 1
    accessRestrictedToStr = "Licensees"
    administrativeInformation = eco_spold.activityDataset.administrativeInformation
    dataGeneratorAndPublication = administrativeInformation.dataGeneratorAndPublication

    assert dataGeneratorAndPublication.personId == personId
    assert dataGeneratorAndPublication.personName == personName
    assert dataGeneratorAndPublication.personEmail == personEmail
    assert dataGeneratorAndPublication.dataPublishedIn == dataPublishedIn
    assert dataGeneratorAndPublication.dataPublishedInStr == dataPublishedInStr
    assert dataGeneratorAndPublication.publishedSourceId == publishedSourceId
    assert dataGeneratorAndPublication.publishedSourceYear == publishedSourceYear
    assert (
        dataGeneratorAndPublication.publishedSourceFirstAuthor
        == publishedSourceFirstAuthor
    )
    assert dataGeneratorAndPublication.isCopyrightProtected == isCopyrightProtected
    assert dataGeneratorAndPublication.pageNumbers == pageNumbers
    assert dataGeneratorAndPublication.accessRestrictedTo == accessRestrictedTo
    assert dataGeneratorAndPublication.accessRestrictedToStr == accessRestrictedToStr


def test_parse_file_v2_file_attributes(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    majorRelease = 3
    minorRelease = 0
    majorRevision = 37
    minorRevision = 0
    internalSchemaVersion = "2.0.10"
    defaultLanguage = "en"
    creationTimestamp = datetime(2010, 7, 28, 18, 41, 6)
    lastEditTimestamp = datetime(2011, 9, 22, 18, 30, 49)
    fileGenerator = "EcoEditor 2.0.43.6348"
    fileTimestamp = datetime(2011, 9, 22, 18, 30, 49)
    contextId = "de659012-50c4-4e96-b54a-fc781bf987ab"
    contextNames = ["ecoinvent"]
    requiredContextsLen = 0
    administrativeInformation = eco_spold.activityDataset.administrativeInformation
    fileAttributes = administrativeInformation.fileAttributes

    assert fileAttributes.majorRelease == majorRelease
    assert fileAttributes.minorRelease == minorRelease
    assert fileAttributes.majorRevision == majorRevision
    assert fileAttributes.minorRevision == minorRevision
    assert fileAttributes.internalSchemaVersion == internalSchemaVersion
    assert fileAttributes.defaultLanguage == defaultLanguage
    assert fileAttributes.creationTimestamp == creationTimestamp
    assert fileAttributes.lastEditTimestamp == lastEditTimestamp
    assert fileAttributes.fileGenerator == fileGenerator
    assert fileAttributes.fileTimestamp == fileTimestamp
    assert fileAttributes.contextId == contextId
    assert fileAttributes.contextNames == contextNames
    assert len(fileAttributes.requiredContexts) == requiredContextsLen


def test_parse_file_v2_pedigree_matrix(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    reliability = 2
    reliabilityStr = (
        "Verified data partly based on assumptions OR nonverified data based on "
        "measurements"
    )
    completeness = 3
    completenessStr = (
        "Representative data from only some sites (<<50%) relevant for the market "
        "considered OR >50% of sites but from shorter periods"
    )
    temporalCorrelation = 1
    temporalCorrelationStr = (
        "Less than 3 years of difference to the time period of the dataset "
        "(fields 600-610)"
    )
    geographicalCorrelation = 3
    geographicalCorrelationStr = "Data from area with similar production conditions"
    furtherTechnologyCorrelation = 1
    furtherTechnologyCorrelationStr = (
        "Data from enterprises, processes and materials under study"
    )
    flowData = eco_spold.activityDataset.flowData
    parameter = flowData.parameters[0]
    pedigreeMatrix = parameter.uncertainties[0].pedigreeMatrices[0]

    assert pedigreeMatrix.reliability == reliability
    assert pedigreeMatrix.reliabilityStr == reliabilityStr
    assert pedigreeMatrix.completeness == completeness
    assert pedigreeMatrix.completenessStr == completenessStr
    assert pedigreeMatrix.temporalCorrelation == temporalCorrelation
    assert pedigreeMatrix.temporalCorrelationStr == temporalCorrelationStr
    assert pedigreeMatrix.geographicalCorrelation == geographicalCorrelation
    assert pedigreeMatrix.geographicalCorrelationStr == geographicalCorrelationStr
    assert pedigreeMatrix.furtherTechnologyCorrelation == furtherTechnologyCorrelation
    assert (
        pedigreeMatrix.furtherTechnologyCorrelationStr
        == furtherTechnologyCorrelationStr
    )
