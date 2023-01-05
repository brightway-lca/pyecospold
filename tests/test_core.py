import os
import tempfile
from datetime import datetime
from io import StringIO

import numpy as np
import pytest
from lxml.etree import XMLSyntaxError

from pyecospold.core import parse_file, save_file
from pyecospold.model import (EcoSpold, Dataset, MetaInformation, FlowData,
                              ProcessInformation, ModellingAndValidation,
                              AdministrativeInformation, Exchange, Allocation,
                              ReferenceFunction, Geography, Technology,
                              DataSetInformation, TimePeriod, Representativeness,
                              Source, Validation, DataEntryBy,
                              DataGeneratorAndPublication, Person)


@pytest.fixture
def ecoSpold() -> EcoSpold:
    return parse_file("data/examples/00001.xml")


def test_parse_file_fail() -> None:
    with open("data/examples/00001.xml") as file:
        xml_str = file.read()
    xml_str = xml_str.replace('amount="1"', 'amount="abc"')
    xml_str = xml_str.replace("<?xml version='1.0' encoding='UTF-8'?>", "")

    with pytest.raises(XMLSyntaxError):
        parse_file(StringIO(xml_str))


def test_parse_file_ecoSpold(ecoSpold: EcoSpold) -> None:
    validationId = 0
    validationStatus = "validationStatus"

    assert type(ecoSpold) == EcoSpold
    assert type(ecoSpold.dataset) == Dataset
    assert ecoSpold.validationId == validationId
    assert ecoSpold.validationStatus == validationStatus


def test_parse_file_dataset(ecoSpold: EcoSpold) -> None:
    validCompanyCodes = "CompanyCodes.xml"
    validRegionalCodes = "RegionalCodes.xml"
    validCategories = "Categories.xml"
    validUnits = "Units.xml"
    number = 1
    timestamp = datetime(2006, 10, 31, 20, 34, 59)
    generator = "EcoAdmin 1.1.17.110"
    internalSchemaVersion = "1.0"
    dataset = ecoSpold.dataset

    assert type(dataset.metaInformation) == MetaInformation
    assert type(dataset.flowData) == FlowData
    assert dataset.validCompanyCodes == validCompanyCodes
    assert dataset.validRegionalCodes == validRegionalCodes
    assert dataset.validCategories == validCategories
    assert dataset.validUnits == validUnits
    assert dataset.number == number
    assert dataset.timestamp == timestamp
    assert dataset.generator == generator
    assert dataset.internalSchemaVersion == internalSchemaVersion


def test_parse_file_metaInformation(ecoSpold: EcoSpold) -> None:
    metaInformation = ecoSpold.dataset.metaInformation

    assert type(metaInformation.processInformation) == ProcessInformation
    assert type(metaInformation.modellingAndValidation) == ModellingAndValidation
    assert type(metaInformation.administrativeInformation) == AdministrativeInformation


def test_parse_file_flowData(ecoSpold: EcoSpold) -> None:
    flowData = ecoSpold.dataset.flowData

    assert type(flowData.exchanges[0]) == Exchange
    assert type(flowData.allocations[0]) == Allocation


def test_parse_file_processInformation(ecoSpold: EcoSpold) -> None:
    processInformation = ecoSpold.dataset.metaInformation.processInformation

    assert type(processInformation.referenceFunction) == ReferenceFunction
    assert type(processInformation.geography) == Geography
    assert type(processInformation.technology) == Technology
    assert type(processInformation.dataSetInformation) == DataSetInformation
    assert type(processInformation.timePeriod) == TimePeriod


def test_parse_file_modellingAndValidation(ecoSpold: EcoSpold) -> None:
    modellingAndValidation = ecoSpold.dataset.metaInformation.modellingAndValidation

    assert type(modellingAndValidation.representativeness) == Representativeness
    assert type(modellingAndValidation.source) == Source
    assert type(modellingAndValidation.validation) == Validation


def test_parse_file_administrativeInformation(ecoSpold: EcoSpold) -> None:
    metaInformation = ecoSpold.dataset.metaInformation
    administrativeInformation = metaInformation.administrativeInformation

    assert type(administrativeInformation.dataEntryBy) == DataEntryBy
    assert type(administrativeInformation.dataGeneratorAndPublication) == \
        DataGeneratorAndPublication
    assert type(administrativeInformation.persons[0]) == Person


def test_parse_file_exchange(ecoSpold: EcoSpold) -> None:
    number = 2156
    category = "waste management"
    subCategory = "recycling"
    localCategory = "Entsorgungssysteme"
    localSubCategory = "Recycling"
    CASNumber = "007439-89-6"
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
    exchange = ecoSpold.dataset.flowData.exchanges[1]
    output_exchange = ecoSpold.dataset.flowData.exchanges[0]

    assert exchange.number == number
    assert exchange.category == category
    assert exchange.subCategory == subCategory
    assert exchange.localCategory == localCategory
    assert exchange.localSubCategory == localSubCategory
    assert exchange.CASNumber == CASNumber
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
    assert exchange.inputGroups == inputGroups
    assert exchange.inputGroupsStr == inputGroupsStr
    assert output_exchange.outputGroups == outputGroups
    assert output_exchange.outputGroupsStr == outputGroupsStr


def test_parse_file_allocaiton(ecoSpold: EcoSpold) -> None:
    referenceToCoProduct = 1
    allocationMethod = -1
    allocationMethodStr = "Undefined"
    fraction = 97.6
    referenceToInputOutputs = [1]
    explanations = ""
    allocaiton = ecoSpold.dataset.flowData.allocations[0]

    assert allocaiton.referenceToCoProduct == referenceToCoProduct
    assert allocaiton.allocationMethod == allocationMethod
    assert allocaiton.allocationMethodStr == allocationMethodStr
    assert allocaiton.fraction == fraction
    assert allocaiton.referenceToInputOutputs == referenceToInputOutputs
    assert allocaiton.explanations == explanations


def test_parse_file_referenceFunction(ecoSpold: EcoSpold) -> None:
    name = "compost plant, open"
    localName = "Kompostieranlage, offen"
    unit = "unit"
    category = "agricultural means of production"
    subCategory = "buildings"
    localCategory = "Landwirtschaftliche Produktionsmittel"
    localSubCategory = "Gebäude"
    amount = 1
    includedProcesses = "Building materials required for a compost plant and its " + \
                        "construction as well as the disposal of these materials " + \
                        "were included. Land use during construction and use is " + \
                        "considered. The lifetime of the plant was assumed as 25 " + \
                        "years. Transport of the building materials to the " + \
                        "construction site were included."
    generalComment = "The inventory refers to a compost plant over the lifetime of " + \
                     "25 years. The compost plant is constructed for a treating " + \
                     "capactiy of 10‘000 tons biogenic waste per year. The total " + \
                     "turnover of the plant over the entire lifetime of 25 years " + \
                     "amounts thus 250‘000 tons biogenic waste."
    formula = "0"
    infrastructureIncluded = True
    CASNumber = ""
    statisticalClassification = 0
    datasetRelatesToProduct = True
    synonyms = ["0"]
    processInformation = ecoSpold.dataset.metaInformation.processInformation
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
    assert referenceFunction.infrastructureIncluded == \
        infrastructureIncluded
    assert referenceFunction.CASNumber == CASNumber
    assert referenceFunction.statisticalClassification == \
        statisticalClassification
    assert referenceFunction.datasetRelatesToProduct == \
        datasetRelatesToProduct
    assert referenceFunction.synonyms == synonyms


def test_parse_file_geography(ecoSpold: EcoSpold) -> None:
    location = "CH"
    text = "Values refer to the situtation in Switzerland."
    processInformation = ecoSpold.dataset.metaInformation.processInformation
    geography = processInformation.geography

    assert geography.location == location
    assert geography.text == text


def test_parse_file_technology(ecoSpold: EcoSpold) -> None:
    text = "Refer to open plant composting."
    processInformation = ecoSpold.dataset.metaInformation.processInformation
    technology = processInformation.technology

    assert technology.text == text


def test_parse_file_timePeriod(ecoSpold: EcoSpold) -> None:
    text = "Year when reference used for this inventory was published."
    startYear = "1999"
    startYearMonth = ""
    startDate = ""
    endYear = "1999"
    endYearMonth = ""
    endDate = ""
    processInformation = ecoSpold.dataset.metaInformation.processInformation
    timePeriod = processInformation.timePeriod

    assert timePeriod.dataValidForEntirePeriod
    assert timePeriod.text == text
    assert timePeriod.startYear == startYear
    assert timePeriod.startYearMonth == startYearMonth
    assert timePeriod.startDate == startDate
    assert timePeriod.endYear == endYear
    assert timePeriod.endYearMonth == endYearMonth
    assert timePeriod.endDate == endDate


def test_parse_file_dataSetInformation(ecoSpold: EcoSpold) -> None:
    type = 1
    typeStr = "Unit process"
    timestamp = datetime(2003, 9, 12, 10, 14, 36)
    version = 1.3
    internalVersion = 53.03
    energyValues = 0
    energyValuesStr = "Undefined"
    languageCode = "en"
    localLanguageCode = "de"
    processInformation = ecoSpold.dataset.metaInformation.processInformation
    dataSetInformation = processInformation.dataSetInformation

    assert dataSetInformation.type == type
    assert dataSetInformation.typeStr == typeStr
    assert not dataSetInformation.impactAssessmentResult
    assert dataSetInformation.timestamp == timestamp
    assert dataSetInformation.version == version
    assert dataSetInformation.internalVersion == internalVersion
    assert dataSetInformation.energyValues == energyValues
    assert dataSetInformation.energyValuesStr == energyValuesStr
    assert dataSetInformation.languageCode == languageCode
    assert dataSetInformation.localLanguageCode == localLanguageCode


def test_parse_file_representativeness(ecoSpold: EcoSpold) -> None:
    percent = np.nan
    productionVolume = ""
    samplingProcedure = "Data come from one compost plant in Switzerland."
    extrapolations = "none"
    uncertaintyAdjustments = "none"
    modellingAndValidation = ecoSpold.dataset.metaInformation.modellingAndValidation
    representativeness = modellingAndValidation.representativeness

    assert representativeness.percent is percent
    assert representativeness.productionVolume == productionVolume
    assert representativeness.samplingProcedure == samplingProcedure
    assert representativeness.extrapolations == extrapolations
    assert representativeness.uncertaintyAdjustments == uncertaintyAdjustments


def test_parse_file_source(ecoSpold: EcoSpold) -> None:
    number = 146
    sourceType = 4
    sourceTypeStr = "Measurement on site"
    firstAuthor = "Nemecek, T."
    additionalAuthors = "Heil A., Huguenin, O., Meier, S., Erzinger S., " + \
                        "Blaser S., Dux. D., Zimmermann A.,"
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
    modellingAndValidation = ecoSpold.dataset.metaInformation.modellingAndValidation
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


def test_parse_file_validation(ecoSpold: EcoSpold) -> None:
    proofReadingDetails = "Passed."
    proofReadingValidator = 291
    otherDetails = ""
    modellingAndValidation = ecoSpold.dataset.metaInformation.modellingAndValidation
    validation = modellingAndValidation.validation

    assert validation.proofReadingDetails == proofReadingDetails
    assert validation.proofReadingValidator == proofReadingValidator
    assert validation.otherDetails == otherDetails


def test_parse_file_dataEntryBy(ecoSpold: EcoSpold) -> None:
    person = 309
    qualityNetwork = 1
    metaInformation = ecoSpold.dataset.metaInformation
    dataEntryBy = metaInformation.administrativeInformation.dataEntryBy

    assert dataEntryBy.person == person
    assert dataEntryBy.qualityNetwork == qualityNetwork


def test_parse_file_dataGeneratorAndPublication(ecoSpold: EcoSpold) -> None:
    person = 309
    dataPublishedIn = 2
    dataPublishedInStr = \
        "Data has been published entirely in 'referenceToPublishedSource'"
    referenceToPublishedSource = 146
    accessRestrictedTo = 0
    accessRestrictedToStr = "Public"
    companyCode = ""
    countryCode = ""
    pageNumbers = ""
    metaInformation = ecoSpold.dataset.metaInformation
    administrativeInformation = metaInformation.administrativeInformation
    dataGeneratorAndPublication = administrativeInformation.dataGeneratorAndPublication

    assert dataGeneratorAndPublication.person == person
    assert dataGeneratorAndPublication.dataPublishedIn == dataPublishedIn
    assert dataGeneratorAndPublication.dataPublishedInStr == \
        dataPublishedInStr
    assert dataGeneratorAndPublication.referenceToPublishedSource == \
        referenceToPublishedSource
    assert dataGeneratorAndPublication.copyright
    assert dataGeneratorAndPublication.accessRestrictedTo == accessRestrictedTo
    assert dataGeneratorAndPublication.accessRestrictedToStr == accessRestrictedToStr
    assert dataGeneratorAndPublication.companyCode == companyCode
    assert dataGeneratorAndPublication.countryCode == countryCode
    assert dataGeneratorAndPublication.pageNumbers == pageNumbers


def test_parse_file_person(ecoSpold: EcoSpold) -> None:
    number = 309
    name = "name"
    address = "address"
    telephone = "telephone"
    telefax = "telefax"
    email = "email@domain.com"
    companyCode = "EMPA-SG"
    countryCode = "CH"
    metaInformation = ecoSpold.dataset.metaInformation
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


def test_save_file() -> None:
    input_path = "data/examples/00001.xml"
    metaInformation = parse_file(input_path)
    output_path = os.path.join(tempfile.gettempdir(), os.urandom(24).hex())
    save_file(metaInformation, output_path)

    with open(input_path) as input_file:
        with open(output_path) as output_file:
            mapping = {ord(c): "" for c in [" ", "\t", "\n"]}
            assert output_file.read().translate(mapping) == \
                input_file.read().translate(mapping)
