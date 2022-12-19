from datetime import datetime
from io import StringIO

from pyecospold.core import parse_file
from pyecospold.model import (ProcessInformation, ReferenceFunction, Geography,
                              Technology, DataSetInformation, TimePeriod)


def test_parse_file_metaInformation() -> None:
    metaInformation = parse_file(
        StringIO(
            """
            <metaInformation>
                <processInformation>
                    <referenceFunction name="compost plant, open"
                        localName="Kompostieranlage, offen"
                        infrastructureProcess="true" unit="unit"
                        category="agricultural means of production"
                        subCategory="buildings"
                        localCategory="Landwirtschaftliche Produktionsmittel"
                        localSubCategory="Gebäude" amount="1"
                        includedProcesses="Building materials required for a compost
                        plant and its construction as well as the disposal of these
                        materials were included. Land use during construction and use
                        is considered. The lifetime of the plant was assumed as 25
                        years. Transport of the building materials to the construction
                        site were included."
                        generalComment="The inventory refers to a compost plant over the
                        lifetime of 25 years. The compost plant is constructed for a
                        treating capactiy of 10‘000 tons biogenic waste per year. The
                        total turnover of the plant over the entire lifetime of 25 years
                        amounts thus 250‘000 tons biogenic waste."
                        formula="0" infrastructureIncluded="true"
                        datasetRelatesToProduct="true">
                        <synonym>0</synonym>
                    </referenceFunction>
                    <geography location="CH"
                    text="Values refer to the situtation in Switzerland." />
                    <technology text="Refer to open plant composting." />
                    <timePeriod dataValidForEntirePeriod="true"
                        text="Year when reference used for this inventory
                        was published.">
                        <startYear>1999</startYear>
                        <endYear>1999</endYear>
                    </timePeriod>
                    <dataSetInformation type="1"
                        impactAssessmentResult="false" timestamp="2003-09-12T10:14:36"
                        version="1.3" internalVersion="53.03" energyValues="0"
                        languageCode="en" localLanguageCode="de" />
                </processInformation>
            </metaInformation>
        """
        )
    )

    assert type(metaInformation.processInformation) == ProcessInformation


def test_parse_file_processInformation() -> None:
    processInformation = parse_file(
        StringIO(
            """
            <processInformation>
                <referenceFunction name="compost plant, open"
                    localName="Kompostieranlage, offen"
                    infrastructureProcess="true" unit="unit"
                    category="agricultural means of production" subCategory="buildings"
                    localCategory="Landwirtschaftliche Produktionsmittel"
                    localSubCategory="Gebäude" amount="1"
                    includedProcesses="Building materials required for a compost plant
                    and its construction as well as the disposal of these materials
                    were included. Land use during construction and use is considered.
                    The lifetime of the plant was assumed as 25 years. Transport of the
                    building materials to the construction site were included."
                    generalComment="The inventory refers to a compost plant over the
                    lifetime of 25 years. The compost plant is constructed for a
                    treating capactiy of 10‘000 tons biogenic waste per year. The
                    total turnover of the plant over the entire lifetime of 25
                    years amounts thus 250‘000 tons biogenic waste."
                    formula="0" infrastructureIncluded="true"
                    datasetRelatesToProduct="true">
                    <synonym>0</synonym>
                </referenceFunction>
                <geography location="CH"
                text="Values refer to the situtation in Switzerland." />
                <technology text="Refer to open plant composting." />
                <timePeriod dataValidForEntirePeriod="true"
                    text="Year when reference used for this inventory was published.">
                    <startYear>1999</startYear>
                    <endYear>1999</endYear>
                </timePeriod>
                <dataSetInformation type="1" impactAssessmentResult="false"
                    timestamp="2003-09-12T10:14:36" version="1.3"
                    internalVersion="53.03" energyValues="0" languageCode="en"
                    localLanguageCode="de" />
            </processInformation>
        """
        )
    )

    assert type(processInformation.referenceFunction) == ReferenceFunction
    assert type(processInformation.geography) == Geography
    assert type(processInformation.technology) == Technology
    assert type(processInformation.dataSetInformation) == DataSetInformation
    assert type(processInformation.timePeriod) == TimePeriod


def test_parse_file_referenceFunction() -> None:
    name = "compost plant, open"
    localName = "Kompostieranlage, offen"
    unit = "unit"
    category = "agricultural means of production"
    subCategory = "buildings"
    localCategory = "Landwirtschaftliche Produktionsmittel"
    localSubCategory = "Gebäude"
    includedProcesses = "Building materials required for a compost plant and its " + \
                        "construction as well as the disposal of these materials " + \
                        "were included. Land use during construction and use is " + \
                        "considered. The lifetime of the plant was assumed as 25 " + \
                        "years. Transport of the building materials to the " + \
                        "construction site were included."
    generalComment = "The inventory refers to a compost plant over the lifetime of " + \
                     "25 years. The compost plant is onstructed for a treating " + \
                     "capactiy of 10‘000 tons biogenic waste per year. The total " + \
                     "turnover of the plant over the entire lifetime of 25 years " + \
                     "amounts thus 250‘000 tons biogenic waste."
    formula = "0"
    CASNumber = "007439-89-6"
    referenceFunction = parse_file(
        StringIO(
            f"""
            <referenceFunction name="{name}" localName="{localName}"
                infrastructureProcess="true" unit="{unit}" category="{category}"
                subCategory="{subCategory}" localCategory="{localCategory}"
                localSubCategory="{localSubCategory}" amount="1"
                includedProcesses="{includedProcesses}"
                generalComment="{generalComment}" formula="{formula}"
                infrastructureIncluded="true" datasetRelatesToProduct="true"
                CASNumber="{CASNumber}" statisticalClassification="100">
                <synonym>0</synonym>
            </referenceFunction>
            """
        )
    )

    assert referenceFunction.name == name
    assert referenceFunction.localName == localName
    assert referenceFunction.infrastructureProcess
    assert referenceFunction.unit == unit
    assert referenceFunction.category == category
    assert referenceFunction.subCategory == subCategory
    assert referenceFunction.localCategory == localCategory
    assert referenceFunction.localSubCategory == localSubCategory
    assert referenceFunction.amount == 1
    assert referenceFunction.includedProcesses == includedProcesses
    assert referenceFunction.generalComment == generalComment
    assert referenceFunction.formula == formula
    assert referenceFunction.infrastructureIncluded
    assert referenceFunction.datasetRelatesToProduct
    assert referenceFunction.CASNumber == CASNumber
    assert referenceFunction.statisticalClassification == 100
    assert referenceFunction.synonym == ["0"]


def test_parse_file_geography() -> None:
    location = "CH"
    text = "Values refer to the situtation in Switzerland."
    geography = parse_file(
        StringIO(f"<geography location='{location}' text='{text}' />")
    )

    assert geography.location == location
    assert geography.text == text


def test_parse_file_technology() -> None:
    text = "Refer to open plant composting."
    technology = parse_file(StringIO(f"<technology text='{text}' />"))

    assert technology.text == text


def test_parse_file_dataSetInformation() -> None:
    languageCode = "en"
    localLanguageCode = "de"
    dataSetInformation = parse_file(
        StringIO(
            f"""
            <dataSetInformation type="1" impactAssessmentResult="false"
            timestamp="2003-09-12T10:14:36" version="1.3" internalVersion="53.03"
            energyValues="0" languageCode="{languageCode}"
            localLanguageCode="{localLanguageCode}"/>
            """
        )
    )

    assert dataSetInformation.type == 1
    assert dataSetInformation.typeStr == "Unit process"
    assert not dataSetInformation.impactAssessmentResult
    assert dataSetInformation.timestamp == datetime(2003, 9, 12, 10, 14, 36)
    assert dataSetInformation.version == 1.3
    assert dataSetInformation.internalVersion == 53.03
    assert dataSetInformation.energyValues == 0
    assert dataSetInformation.energyValuesStr == "Undefined"
    assert dataSetInformation.languageCode == languageCode
    assert dataSetInformation.localLanguageCode == localLanguageCode


def test_parse_file_validation() -> None:
    proofReadingDetails = "passed"
    otherDetails = "otherDetails"
    validation = parse_file(
        StringIO(
            f"""
            <validation proofReadingDetails="{proofReadingDetails}"
            proofReadingValidator="322" otherDetails="{otherDetails}"/>
            """
        )
    )

    assert validation.proofReadingDetails == proofReadingDetails
    assert validation.proofReadingValidator == 322
    assert validation.otherDetails == otherDetails


def test_parse_file_source() -> None:
    firstAuthor = "Nemecek, T."
    additionalAuthors = \
        "Heil A., Huguenin, O., Meier, S., Erzinger S., " + \
        "Blaser S., Dux. D., Zimmermann A.,"
    title = "Life Cycle Inventories of Agricultural Production Systems"
    titleOfAnthology = "Final report ecoinvent 2000"
    placeOfPublications = "Dübendorf, CH"
    publisher = "Swiss Centre for LCI, FAL &amp; FAT"
    text = "CD-ROM"
    pageNumbers = "pageNumbers"
    nameOfEditors = "Dones R."
    journal = "journal"
    issueNo = "issueNo"
    source = parse_file(
        StringIO(
            f"""
            <source number="146" sourceType="4" firstAuthor="{firstAuthor}"
            additionalAuthors="{additionalAuthors}" year="2003" title="{title}"
            titleOfAnthology="{titleOfAnthology}"
            placeOfPublications="{placeOfPublications}" publisher="{publisher}"
            volumeNo="15" text="{text}" pageNumbers="{pageNumbers}"
            nameOfEditors="{nameOfEditors}" journal="{journal}" issueNo="{issueNo}"/>
            """
        )
    )

    assert source.number == 146
    assert source.sourceType == 4
    assert source.sourceTypeStr == "Measurement on site"
    assert source.firstAuthor == firstAuthor
    assert source.additionalAuthors == additionalAuthors
    assert source.year == 2003
    assert source.title == title
    assert source.titleOfAnthology == titleOfAnthology
    assert source.placeOfPublications == placeOfPublications
    # assert source.publisher == publisher  FIXME: parsing &amp
    assert source.volumeNo == 15
    assert source.text == text
    assert source.pageNumbers == pageNumbers
    assert source.nameOfEditors == nameOfEditors
    assert source.journal == journal
    assert source.issueNo == issueNo


def test_parse_file_dataGeneratorAndPublication() -> None:
    companyCode = "EMPA-SG"
    countryCode = "CH"
    pageNumbers = "pageNumbers"
    dataGeneratorAndPublication = parse_file(
        StringIO(
            f"""
            <dataGeneratorAndPublication person="309" dataPublishedIn="2"
            referenceToPublishedSource="146" copyright="true"
            accessRestrictedTo="0" companyCode="{companyCode}"
            countryCode="{countryCode}" pageNumbers="{pageNumbers}"/>
            """
        )
    )

    assert dataGeneratorAndPublication.person == 309
    assert dataGeneratorAndPublication.dataPublishedIn == 2
    assert dataGeneratorAndPublication.dataPublishedInStr == \
        "Data has been published entirely in 'referenceToPublishedSource'"
    assert dataGeneratorAndPublication.referenceToPublishedSource == 146
    assert dataGeneratorAndPublication.copyright
    assert dataGeneratorAndPublication.accessRestrictedTo == 0
    assert dataGeneratorAndPublication.accessRestrictedToStr == "Public"
    assert dataGeneratorAndPublication.companyCode == companyCode
    assert dataGeneratorAndPublication.countryCode == countryCode
    assert dataGeneratorAndPublication.pageNumbers == pageNumbers


def test_parse_file_representativeness() -> None:
    productionVolume = "9.5 million tonnes in Cu in 1994"
    samplingProcedure = "literature"
    extrapolations = "see Geography and Technology"
    uncertaintyAdjustments = "none"
    representativeness = parse_file(
        StringIO(
            f"""
            <representativeness percent="84.0" productionVolume="{productionVolume}"
            samplingProcedure="{samplingProcedure}" extrapolations="{extrapolations}"
            uncertaintyAdjustments="{uncertaintyAdjustments}"/>
            """
        )
    )

    assert representativeness.percent == 84.0
    assert representativeness.productionVolume == productionVolume
    assert representativeness.samplingProcedure == samplingProcedure
    assert representativeness.extrapolations == extrapolations
    assert representativeness.uncertaintyAdjustments == uncertaintyAdjustments


def test_parse_file_timePeriod() -> None:
    text = "Year when reference used for this inventory was published."
    startYear = "1999"
    endYear = "1999"
    timePeriod = parse_file(
        StringIO(
            f"""
            <timePeriod dataValidForEntirePeriod="true"
                text="{text}">
                <startYear>{startYear}</startYear>
                <endYear>{endYear}</endYear>
            </timePeriod>
            """
        )
    )

    assert timePeriod.dataValidForEntirePeriod
    assert timePeriod.text == text
    assert timePeriod.startYear == startYear
    assert timePeriod.endYear == endYear


def test_parse_file_dataEntryBy() -> None:
    dataEntryBy = parse_file(
        StringIO("""<dataEntryBy person="309" qualityNetwork="1" />""")
    )

    assert dataEntryBy.person == 309
    assert dataEntryBy.qualityNetwork == 1
