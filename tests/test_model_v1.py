"""Test cases for the __model_v1__ module."""

from datetime import datetime
from io import StringIO

import numpy as np
import pytest
from lxml.etree import XMLSyntaxError

from pyecospold.core import parse_file_v1
from pyecospold.model_v1 import (
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


@pytest.fixture(name="eco_spold")
def _eco_spold() -> EcoSpold:
    return parse_file_v1("data/v1/v1_1.xml")


def test_parse_file_v1_fail() -> None:
    """It fails on schema violation."""
    with open("data/v1/v1_1.xml", encoding="utf-8") as file:
        xmlStr = file.read()
    xmlStr = xmlStr.replace('amount="1"', 'amount="abc"')
    xmlStr = xmlStr.replace("<?xml version='1.0' encoding='UTF-8'?>", "")

    with pytest.raises(XMLSyntaxError):
        parse_file_v1(StringIO(xmlStr))


def test_parse_file_v1_eco_spold(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    validationId = 0
    validationStatus = "validationStatus"

    assert isinstance(eco_spold, EcoSpold)
    assert isinstance(eco_spold.datasets[0], Dataset)
    assert eco_spold.validationId == validationId
    assert eco_spold.validationStatus == validationStatus


def test_parse_file_v1_dataset(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    validCompanyCodes = "CompanyCodes.xml"
    validRegionalCodes = "RegionalCodes.xml"
    validCategories = "Categories.xml"
    validUnits = "Units.xml"
    number = 1
    timestamp = datetime(2006, 10, 31, 20, 34, 59)
    generator = "EcoAdmin 1.1.17.110"
    internalSchemaVersion = "1.0"
    dataset = eco_spold.datasets[0]

    assert isinstance(dataset.metaInformation, MetaInformation)
    assert isinstance(dataset.flowData, FlowData)
    assert dataset.validCompanyCodes == validCompanyCodes
    assert dataset.validRegionalCodes == validRegionalCodes
    assert dataset.validCategories == validCategories
    assert dataset.validUnits == validUnits
    assert dataset.number == number
    assert dataset.timestamp == timestamp
    assert dataset.generator == generator
    assert dataset.internalSchemaVersion == internalSchemaVersion


def test_parse_file_v1_meta_information(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    metaInformation = eco_spold.datasets[0].metaInformation

    assert isinstance(metaInformation.processInformation, ProcessInformation)
    assert isinstance(metaInformation.modellingAndValidation, ModellingAndValidation)
    assert isinstance(
        metaInformation.administrativeInformation, AdministrativeInformation
    )


def test_parse_file_v1_flow_data(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    flowData = eco_spold.datasets[0].flowData

    assert isinstance(flowData.exchanges[0], Exchange)
    assert isinstance(flowData.allocations[0], Allocation)


def test_parse_file_v1_process_information(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    processInformation = eco_spold.datasets[0].metaInformation.processInformation

    assert isinstance(processInformation.referenceFunction, ReferenceFunction)
    assert isinstance(processInformation.geography, Geography)
    assert isinstance(processInformation.technology, Technology)
    assert isinstance(processInformation.dataSetInformation, DataSetInformation)
    assert isinstance(processInformation.timePeriod, TimePeriod)


def test_parse_file_v1_modelling_and_validation(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    dataset = eco_spold.datasets[0]
    modellingAndValidation = dataset.metaInformation.modellingAndValidation

    assert isinstance(modellingAndValidation.representativeness, Representativeness)
    assert isinstance(modellingAndValidation.source, Source)
    assert isinstance(modellingAndValidation.validation, Validation)


def test_parse_file_v1_administrative_information(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    metaInformation = eco_spold.datasets[0].metaInformation
    administrativeInformation = metaInformation.administrativeInformation

    assert isinstance(administrativeInformation.dataEntryBy, DataEntryBy)
    assert isinstance(
        administrativeInformation.dataGeneratorAndPublication,
        DataGeneratorAndPublication,
    )
    assert isinstance(administrativeInformation.persons[0], Person)


def test_parse_file_v1_exchange(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    number = 2156
    category = "waste management"
    subCategory = "recycling"
    localCategory = "Entsorgungssysteme"
    localSubCategory = "Recycling"
    casNumber = "007439-89-6"
    name = "disposal, building, reinforcement steel, to recycling"
    location = "CH"
    unit = "kg"
    uncertaintyType = 1
    uncertaintyTypeStr = "lognormal"
    meanValue = 21200
    standardDeviation95 = 1.22
    formula = "Fe"
    referenceToSource = 0
    pageNumbers = ""
    generalComment = "(2,3,1,1,1,5)"
    localName = "Entsorgung, Gebäude, Armierungseisen, ins Recycling"
    infrastructureProcess = False
    minValue = np.nan
    maxValue = np.nan
    mostLikelyValue = np.nan
    inputGroups = [5]
    inputGroupsStr = ["FromTechnosphere"]
    outputGroups = [0]
    outputGroupsStr = ["ReferenceProduct"]
    exchange = eco_spold.datasets[0].flowData.exchanges[1]
    outputExchange = eco_spold.datasets[0].flowData.exchanges[0]

    assert exchange.number == number
    assert exchange.category == category
    assert exchange.subCategory == subCategory
    assert exchange.localCategory == localCategory
    assert exchange.localSubCategory == localSubCategory
    assert exchange.CASNumber == casNumber
    assert exchange.name == name
    assert exchange.location == location
    assert exchange.unit == unit
    assert exchange.uncertaintyType == uncertaintyType
    assert exchange.uncertaintyTypeStr == uncertaintyTypeStr
    assert exchange.meanValue == meanValue
    assert exchange.standardDeviation95 == standardDeviation95
    assert exchange.formula == formula
    assert exchange.referenceToSource == referenceToSource
    assert exchange.pageNumbers == pageNumbers
    assert exchange.generalComment == generalComment
    assert exchange.localName == localName
    assert exchange.infrastructureProcess == infrastructureProcess
    assert exchange.minValue is minValue
    assert exchange.maxValue is maxValue
    assert exchange.mostLikelyValue is mostLikelyValue
    assert exchange.groups == inputGroups
    assert exchange.groupsStr == inputGroupsStr
    assert outputExchange.groups == outputGroups
    assert outputExchange.groupsStr == outputGroupsStr


def test_parse_file_v1_allocation(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    referenceToCoProduct = 1
    allocationMethod = -1
    allocationMethodStr = "Undefined"
    fraction = 97.6
    referenceToInputOutputs = [1]
    explanations = ""
    allocaiton = eco_spold.datasets[0].flowData.allocations[0]

    assert allocaiton.referenceToCoProduct == referenceToCoProduct
    assert allocaiton.allocationMethod == allocationMethod
    assert allocaiton.allocationMethodStr == allocationMethodStr
    assert allocaiton.fraction == fraction
    assert allocaiton.referenceToInputOutputs == referenceToInputOutputs
    assert allocaiton.explanations == explanations


def test_parse_file_v1_reference_function(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    name = "compost plant, open"
    localName = "Kompostieranlage, offen"
    unit = "unit"
    category = "agricultural means of production"
    subCategory = "buildings"
    localCategory = "Landwirtschaftliche Produktionsmittel"
    localSubCategory = "Gebäude"
    amount = 1
    includedProcesses = (
        "Building materials required for a compost plant and its "
        + "construction as well as the disposal of these materials "
        + "were included. Land use during construction and use is "
        + "considered. The lifetime of the plant was assumed as 25 "
        + "years. Transport of the building materials to the "
        + "construction site were included."
    )
    generalComment = (
        "The inventory refers to a compost plant over the lifetime of "
        + "25 years. The compost plant is constructed for a treating "
        + "capactiy of 10‘000 tons biogenic waste per year. The total "
        + "turnover of the plant over the entire lifetime of 25 years "
        + "amounts thus 250‘000 tons biogenic waste."
    )
    formula = "0"
    infrastructureIncluded = True
    casNumber = ""
    statisticalClassification = 0
    datasetRelatesToProduct = True
    synonyms = ["0"]
    processInformation = eco_spold.datasets[0].metaInformation.processInformation
    referenceFunction = processInformation.referenceFunction

    assert referenceFunction.name == name
    assert referenceFunction.localName == localName
    assert referenceFunction.infrastructureProcess
    assert referenceFunction.unit == unit
    assert referenceFunction.category == category
    assert referenceFunction.subCategory == subCategory
    assert referenceFunction.localCategory == localCategory
    assert referenceFunction.localSubCategory == localSubCategory
    assert referenceFunction.amount == amount
    assert referenceFunction.includedProcesses == includedProcesses
    assert referenceFunction.generalComment == generalComment
    assert referenceFunction.formula == formula
    assert referenceFunction.infrastructureIncluded == infrastructureIncluded
    assert referenceFunction.CASNumber == casNumber
    assert referenceFunction.statisticalClassification == statisticalClassification
    assert referenceFunction.datasetRelatesToProduct == datasetRelatesToProduct
    assert referenceFunction.synonyms == synonyms


def test_parse_file_v1_geography(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    location = "CH"
    text = "Values refer to the situtation in Switzerland."
    processInformation = eco_spold.datasets[0].metaInformation.processInformation
    geography = processInformation.geography

    assert geography.location == location
    assert geography.text == text


def test_parse_file_v1_technology(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    text = "Refer to open plant composting."
    processInformation = eco_spold.datasets[0].metaInformation.processInformation
    technology = processInformation.technology

    assert technology.text == text


def test_parse_file_v1_time_period(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    text = "Year when reference used for this inventory was published."
    startDate = datetime(1999, 1, 1)
    endDate = datetime(1999, 1, 1)
    modifiedEndDate = datetime(2000, 3, 4)
    processInformation = eco_spold.datasets[0].metaInformation.processInformation
    timePeriod = processInformation.timePeriod

    assert timePeriod.dataValidForEntirePeriod
    assert timePeriod.text == text
    assert timePeriod.startDate == startDate
    assert timePeriod.endDate == endDate

    timePeriod.endDate = modifiedEndDate
    assert timePeriod.endDate == modifiedEndDate


def test_parse_file_v1_dataset_information(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    _type = 1
    typeStr = "Unit process"
    timestamp = datetime(2003, 9, 12, 10, 14, 36)
    version = 1.3
    internalVersion = 53.03
    energyValues = 0
    energyValuesStr = "Undefined"
    languageCode = "en"
    localLanguageCode = "de"
    processInformation = eco_spold.datasets[0].metaInformation.processInformation
    dataSetInformation = processInformation.dataSetInformation

    assert dataSetInformation.type == _type
    assert dataSetInformation.typeStr == typeStr
    assert not dataSetInformation.impactAssessmentResult
    assert dataSetInformation.timestamp == timestamp
    assert dataSetInformation.version == version
    assert dataSetInformation.internalVersion == internalVersion
    assert dataSetInformation.energyValues == energyValues
    assert dataSetInformation.energyValuesStr == energyValuesStr
    assert dataSetInformation.languageCode == languageCode
    assert dataSetInformation.localLanguageCode == localLanguageCode


def test_parse_file_v1_representativeness(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    percent = np.nan
    productionVolume = ""
    samplingProcedure = "Data come from one compost plant in Switzerland."
    extrapolations = "none"
    uncertaintyAdjustments = "none"
    modellingAndValidation = eco_spold.datasets[
        0
    ].metaInformation.modellingAndValidation
    representativeness = modellingAndValidation.representativeness

    assert representativeness.percent is percent
    assert representativeness.productionVolume == productionVolume
    assert representativeness.samplingProcedure == samplingProcedure
    assert representativeness.extrapolations == extrapolations
    assert representativeness.uncertaintyAdjustments == uncertaintyAdjustments


def test_parse_file_v1_source(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    number = 146
    sourceType = 4
    sourceTypeStr = "Measurement on site"
    firstAuthor = "Nemecek, T."
    additionalAuthors = (
        "Heil A., Huguenin, O., Meier, S., Erzinger S., "
        + "Blaser S., Dux. D., Zimmermann A.,"
    )
    year = 2003
    title = "Life Cycle Inventories of Agricultural Production Systems"
    pageNumbers = ""
    nameOfEditors = ""
    titleOfAnthology = "Final report ecoinvent 2000"
    placeOfPublications = "Dübendorf, CH"
    publisher = "Swiss Centre for LCI, FAL & FAT"
    journal = ""
    volumeNo = 15
    issueNo = ""
    text = "CD-ROM"
    modellingAndValidation = eco_spold.datasets[
        0
    ].metaInformation.modellingAndValidation
    source = modellingAndValidation.source

    assert source.number == number
    assert source.sourceType == sourceType
    assert source.sourceTypeStr == sourceTypeStr
    assert source.firstAuthor == firstAuthor
    assert source.additionalAuthors == additionalAuthors
    assert source.year == year
    assert source.title == title
    assert source.pageNumbers == pageNumbers
    assert source.nameOfEditors == nameOfEditors
    assert source.titleOfAnthology == titleOfAnthology
    assert source.placeOfPublications == placeOfPublications
    assert source.publisher == publisher
    assert source.journal == journal
    assert source.volumeNo == volumeNo
    assert source.issueNo == issueNo
    assert source.text == text


def test_parse_file_v1_validation(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    proofReadingDetails = "Passed."
    proofReadingValidator = 291
    otherDetails = ""
    modellingAndValidation = eco_spold.datasets[
        0
    ].metaInformation.modellingAndValidation
    validation = modellingAndValidation.validation

    assert validation.proofReadingDetails == proofReadingDetails
    assert validation.proofReadingValidator == proofReadingValidator
    assert validation.otherDetails == otherDetails


def test_parse_file_v1_data_entry_by(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    person = 309
    qualityNetwork = 1
    metaInformation = eco_spold.datasets[0].metaInformation
    dataEntryBy = metaInformation.administrativeInformation.dataEntryBy

    assert dataEntryBy.person == person
    assert dataEntryBy.qualityNetwork == qualityNetwork


def test_parse_file_v1_data_generator_and_publication(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    person = 309
    dataPublishedIn = 2
    dataPublishedInStr = (
        "Data has been published entirely in 'referenceToPublishedSource'"
    )
    referenceToPublishedSource = 146
    accessRestrictedTo = 0
    accessRestrictedToStr = "Public"
    companyCode = ""
    countryCode = ""
    pageNumbers = ""
    metaInformation = eco_spold.datasets[0].metaInformation
    administrativeInformation = metaInformation.administrativeInformation
    dataGeneratorAndPublication = administrativeInformation.dataGeneratorAndPublication

    assert dataGeneratorAndPublication.person == person
    assert dataGeneratorAndPublication.dataPublishedIn == dataPublishedIn
    assert dataGeneratorAndPublication.dataPublishedInStr == dataPublishedInStr
    assert (
        dataGeneratorAndPublication.referenceToPublishedSource
        == referenceToPublishedSource
    )
    assert dataGeneratorAndPublication.copyright
    assert dataGeneratorAndPublication.accessRestrictedTo == accessRestrictedTo
    assert dataGeneratorAndPublication.accessRestrictedToStr == accessRestrictedToStr
    assert dataGeneratorAndPublication.companyCode == companyCode
    assert dataGeneratorAndPublication.countryCode == countryCode
    assert dataGeneratorAndPublication.pageNumbers == pageNumbers


def test_parse_file_v1_person(eco_spold: EcoSpold) -> None:
    """It parses attributes correctly."""
    number = 309
    name = "name"
    address = "address"
    telephone = "telephone"
    telefax = "telefax"
    email = "email@domain.com"
    companyCode = "EMPA-SG"
    countryCode = "CH"
    metaInformation = eco_spold.datasets[0].metaInformation
    administrativeInformation = metaInformation.administrativeInformation
    person = administrativeInformation.persons[0]

    assert person.number == number
    assert person.name == name
    assert person.address == address
    assert person.telephone == telephone
    assert person.telefax == telefax
    assert person.email == email
    assert person.companyCode == companyCode
    assert person.countryCode == countryCode
