from datetime import datetime
from typing import Dict, List

from lxml import etree

from .config import Defaults
from .helpers import DataTypesConverter, DataValidator


class EcoSpold(etree.ElementBase):
    """"The data (exchange) format of the ECOINVENT quality network. A dataset
    describes LCI related information of a unit process or a terminated system
    comprising metaInformation (description of the process) and flowData
    (quantified inputs and outputs and allocation factors, if any)."""

    @property
    def dataset(self) -> "Dataset":
        """Contains information about one individual unit process (or terminated
        system). Information is divided into metaInformation and flowData."""
        return self.find("dataset", namespaces=self.nsmap)


class Dataset(etree.ElementBase):
    """Contains information about one individual unit process (or terminated
    system). Information is divided into metaInformation and flowData."""

    @property
    def metaInformation(self) -> "MetaInformation":
        """Contains information about the process (its name, (functional) unit,
        classification, technology, geography, time, etc.), about modelling
        assumptions and validation details and about dataset administration
        (version number, kind of dataset, language)."""
        return self.find("metaInformation", namespaces=self.nsmap)

    @property
    def flowData(self) -> "FlowData":
        """Contains information about inputs and outputs (to and from nature
        as well as to and from technosphere) and information about allocation
        (flows to be allocated, co-products to be allocated to, allocation
        factors)."""
        return self.find("flowData", namespaces=self.nsmap)


class MetaInformation(etree.ElementBase):
    """Contains information about the process (its name, (functional) unit,
    classification, technology, geography, time, etc.), about modelling
    assumptions and validation details and about dataset administration
    (version number, kind of dataset, language)."""

    @property
    def processInformation(self) -> "ProcessInformation":
        return self.find("processInformation", namespaces=self.nsmap)

    @property
    def modellingAndValidation(self) -> "ModellingAndValidation":
        return self.find("modellingAndValidation", namespaces=self.nsmap)

    @property
    def administrativeInformation(self) -> "AdministrativeInformation":
        return self.find("administrativeInformation", namespaces=self.nsmap)


class FlowData(etree.ElementBase):
    """Contains information about inputs and outputs (to and from nature
    as well as to and from technosphere) and information about allocation
    (flows to be allocated, co-products to be allocated to, allocation
    factors)."""

    pass


class ProcessInformation(etree.ElementBase):
    """Contains content-related metainformation for the unit process."""

    @property
    def referenceFunction(self) -> "ReferenceFunction":
        """Comprises information which identifies and characterises one particular
        dataset (=unit process or system terminated)."""
        return self.find("referenceFunction", namespaces=self.nsmap)

    @property
    def geography(self) -> "Geography":
        """Contains information about the geographic validity of the process. The region
        described with regional code and free text is the market area of the
        product / service at issue and not necessarily the place of production."""
        return self.find("geography", namespaces=self.nsmap)

    @property
    def technology(self) -> "Technology":
        """Contains a description of the technology for which flow data have been
        collected. Free text can be used. Pictures, graphs and tables are not allowed.
        The text should cover information necessary to identify the properties and
        particularities of the technology(ies) underlying the process data."""
        return self.find("technology", namespaces=self.nsmap)

    @property
    def dataSetInformation(self) -> "DataSetInformation":
        """Contains the administrative information about the dataset at issue: type of
        dataset (unit process, elementary flow, impact category, multi-output process)
        timestamp, version and internalVersion number as well as language and
        localLanguage code."""
        return self.find("dataSetInformation", namespaces=self.nsmap)

    @property
    def timePeriod(self) -> "TimePeriod":
        """Contains all possible date-formats applicable to describe start and end date
        of the time period for which the dataset is valid."""
        return self.find("timePeriod", namespaces=self.nsmap)


class ModellingAndValidation(etree.ElementBase):
    """Contains metaInformation about how unit processes are modelled
    and about the review/validation of the dataset."""

    @property
    def representativeness(self) -> "Representativeness":
        """Contains information about the fraction of the relevant market supplied by
        the product/service described in the dataset. Information about market share,
        production volume (in the ecoinvent quality network: also consumption volume in
        the market area) and information about how data have been sampled."""
        return self.find("representativeness", namespaces=self.nsmap)

    @property
    def source(self) -> "Source":
        """Contains information about author(s), title, kind of publication,
        place of publication, name of editors (if any), etc.."""
        return self.find("source", namespaces=self.nsmap)

    @property
    def validation(self) -> "Validation":
        """Contains information about who carried out the critical review
        and about the main results and conclusions of the revie and the
        recommendations made."""
        return self.find("validation", namespaces=self.nsmap)


class AdministrativeInformation(etree.ElementBase):
    """Contains information about the person that compiled and entered
    the dataset in the database and about kind of publication and the
    accessibility of the dataset."""

    @property
    def dataEntryBy(self) -> "DataEntryBy":
        """Contains information about the person that entered data in the
        database or transformed data into the format of the ecoinvent
        (or any other) quality network."""
        return self.find("dataEntryBy", namespaces=self.nsmap)

    @property
    def dataGeneratorAndPublication(self) -> "DataGeneratorAndPublication":
        """Contains information about who compiled for and entered data into
        the database. Furthermore contains information about kind of publication
        underlying the dataset and the accessibility of the dataset."""
        return self.find("dataGeneratorAndPublication", namespaces=self.nsmap)

    @property
    def person(self) -> List["Person"]:
        """Used for the identification of members of the organisation institute
        co-operating within a quality network (e.g., ecoinvent) referred to in
        the areas Validation, dataEntryBy and dataGeneratorAndPublication."""
        return self.findall("person", namespaces=self.nsmap)


class Exchange(etree.ElementBase):
    """Comprises all inputs and outputs (both elementary flows and
    intermediate product flows) recorded in a unit process and its
    related information."""

    pass


class ReferenceFunction(etree.ElementBase):
    """
    Comprises information which identifies and characterises one particular dataset
    (=unit process or system terminated).
    """

    @property
    def synonyms(self) -> List[str]:
        """Synonyms for the name, localName. In the Excel editor they are separated
        by two slashes ('//'). Synonyms are a subset of referenceFunction. 0..n
        entries are allowed with a max. length of 80 each."""
        return [
            synonym.text for synonym in self.findall("synonym", namespaces=self.nsmap)
        ]

    @property
    def datasetRelatesToProduct(self) -> bool:
        """Indicates whether the dataset relates to a process/service or not. In
        the ecoinvent quality network the value required is 'yes' for unit
        processes and multioutput processes and 'no' for elementary flows and
        impact categories."""
        return DataTypesConverter.str_to_bool(self.get("datasetRelatesToProduct"))

    @property
    def name(self) -> str:
        """Name of the unit process, elementary flow or impact category. For unit
        processes and system terminated name is used as the identifying entry
        together with unit, location and infrastructureProcess (yes/no). The process
        name is structured as follows (quality guidelines of ecoinvent 2000):
        1. Name of product/service, production process or worked product, level of
        processing; 2. additional descriptions, separated by comma: sum formula,
        site of production or provenience, company, imports included or not;
        3. Location in the value added chain (at plant, at regional storehouse),
        or destination (for wastes: to sanitary landfill, to municipal incineration)
        always using "at" and "to", respectively. For elementary flows name, unit,
        category and subCategory are used as the discriminating elements. The
        nomenclature of the SETAC WG 'Data quality and data availability' is used
        for elementary flows as far as possible. For impact categories, name,
        location, unit, category and subCategory are used as discriminating elements.
        The naming of impact categories takes pattern from the corresponding original
        publication. English is the default language in the ecoinvent quality network.
        """
        return self.get("name")

    @property
    def localName(self) -> str:
        """see 'name' for explanations. German is the default local language in the
        ecoinvent quality network."""
        return self.get("localName")

    @property
    def infrastructureProcess(self) -> bool:
        """Indicates whether the process is an investment or an operation process.
        Investment processes are for instance building of a nuclear power plant,
        a road, docks, construction of production machinery which deliver as the output
        a nuclear power plant, a km road, one seaport, and production machinery
        respectively. It is used as a discriminating element for the identification of
        processes. Not applicable for elementary flows and impact categories."""
        return DataTypesConverter.str_to_bool(self.get("infrastructureProcess"))

    @property
    def amount(self) -> float:
        """Indicates the amount of reference flow (product/service, elementary flow,
        impact category).  Within the ecoinvent quality network the amount of the
        reference flow always equals 1."""
        return float(self.get("amount"))

    @amount.setter
    def amount(self, value: str) -> bool:
        return DataValidator.try_set(self, "amount", value)

    @property
    def unit(self) -> str:
        """For unit processes (and systems terminated) it is the unit to which all
        inputs and outputs of the unit process are related to (functional unit).
        For elementary flows it is the unit in which exhanges are reported. For impact
        categories, it is the unit in which characterisation, damage or weighting
        factors are expressed. SI-units are preferred. The units are always expressed
        in English language."""
        return self.get("unit")

    @property
    def category(self) -> str:
        """Category is used to structure the content of the database (together with
        SubCategory). It is not required for the identification of a process (processes
        in different categories/subCategories may therefore not be named identically).
        But it is required for the identification of elementary flows and impact
        categories. Categories are administrated centrally. English is the default
        language in the ecoinvent quality network."""
        return self.get("category")

    @property
    def subCategory(self) -> str:
        """SubCategory is used to further structure the content of the database
        (together with category). It is not required for the identification of a
        process (processes in different categories/subCategories may therefore not be
        named identically). But it is required for the identification of elementary
        flows and impact categories. SubCategories are administrated centrally. English
        is the default language in the ecoinvent quality network."""
        return self.get("subCategory")

    @property
    def localCategory(self) -> str:
        """See category for explanations. German is the default local language in the
        ecoinvent quality network."""
        return self.get("localCategory")

    @property
    def localSubCategory(self) -> str:
        """"See subCategory for explanations. German is the default local language in
        the ecoinvent quality network."""
        return self.get("localSubCategory")

    @property
    def includedProcesses(self) -> str:
        """"Contains a description of the (sub-)processes which are combined to form
        one unit process (e.g., 'operation of heating system' including operation of
        boiler unit, regulation unit and circulation pumps). Such combination may be
        necessary because of lack of detailedness in available data or because of data
        confidentiality. As far as possible and feasible, data should however be
        reported on the level of detail it has been received. Not applicable for
        elementary flows and impact categories."""
        return self.get("includedProcesses")

    @property
    def generalComment(self) -> str:
        """Free text for general information about the dataset.
        It may contain information about:
            - the intended application of the dataset
            - information sources used
            - data selection principles
            -  modelling choices (exclusion of intermediate product flows, processes,
            allocation if done before entering into database).
        """
        return self.get("generalComment")

    @property
    def infrastructureIncluded(self) -> bool:
        """Indicates whether the unit process imported into the database on the basis
        of an LCI result (received as cumulative mass- and energy-flows, hence, no LCI
        results will be calculated for such processes) has included infrastructure
        processes or not. For all other unit process raw data data sets this data field
        is empty. After calculation of LCI results in ecoinvent, the data field is
        filled in according to the fact, whether or not infrastructure has been
        including during the calculation. Not applicable for elementary flows and impact
        categories."""
        return DataTypesConverter.str_to_bool(self.get("infrastructureIncluded"))

    @property
    def CASNumber(self) -> str:
        """Indicates the number according to the Chemical Abstract Service (CAS).
        The Format of the CAS-number: 000000-00-0, where the first string of digits
        needs not to be complete (i.e. less than six digits are admitted).
        Not applicable for impact categories."""
        return self.get("CASNumber")

    @property
    def statisticalClassification(self) -> int:
        """Contains the EU-classification system (NACE code). For the first edition
        of the ecoinvent database this data field will not be used. Not applicable
        for elementary flows and impact categories."""
        return int(self.get("statisticalClassification"))

    @property
    def formula(self) -> str:
        """Chemical formula (e.g. sum formula) may be entered. No graphs are allowed
        to represent chemical formulas. Not applicable for impact categories."""
        return self.get("formula")


class Geography(etree.ElementBase):
    """Contains information about the geographic validity of the process. The region
    described with regional code and free text is the market area of the
    product / service at issue and not necessarily the place of production."""

    @property
    def location(self) -> str:
        """7 letter regional code (capital letters). List of 2 letter ISO country
        codes extended by codes for regions, continents, market areas, and
        organisations and companies. The location code indicates the supply area
        of a product/service and the area of validity of impact assessment methods
        and impact categories, respectively. It does NOT necessarily coincide with
        the area/site of production or provenience. If supply and production area
        differ, production area is indicated in the name of the unit process."""
        return self.get("location")

    @property
    def text(self) -> str:
        """Free text for further explanation. Text comprises additional aspects of
        the location, namely whether:
        - certain areas are exempted from the location indicated,
        - data are only valid for certain regions within the location indicated.
        - certain elementary flows or intermediate product flows are extrapolated
        from another geographical area than indicated.
        Extrapolations should be reported under 'representativeness'.
        """
        return self.get("text")


class Technology(etree.ElementBase):
    """Contains a description of the technology for which flow data have been
    collected. Free text can be used. Pictures, graphs and tables are not allowed.
    The text should cover information necessary to identify the properties and
    particularities of the technology(ies) underlying the process data."""

    @property
    def text(self) -> str:
        """Describes the technological properties of the unit process. If the
        process comprises several subprocesses, the corresponding technologies
        should be reported as well. Professional nomenclature should be used for
        the description. The description helps the user to judge the technical
        suitability of the process dataset for his or her application (purpose).
        No graphs, figures or tables are allowed in this text field. It should be
        stated if data for certain elementary flows or intermediate product flows
        are derived from different technology."""
        return self.get("text")


class DataSetInformation(etree.ElementBase):
    """Contains the administrative information about the dataset at issue: type of
    dataset (unit process, elementary flow, impact category, multi-output process)
    timestamp, version and internalVersion number as well as language and localLanguage
    code."""

    timestampFormat = "%Y-%m-%dT%H:%M:%S"

    typeMap: Dict[int, str] = {
        0: "System non-terminated",
        1: "Unit process",
        2: "System terminated",
        3: "Elementary Flow",
        4: "Impact Category",
        5: "Multioutput process"
    }

    energyValuesMap: Dict[int, str] = {
        0: "Undefined",
        1: "Net values",
        2: "Gross values"
    }

    @property
    def type(self) -> int:
        """Indicates the kind of data that is represented by this dataset. The code is:
        0=System non-terminated. 1=Unit process. 2=System terminated. 3=Elementary flow.
        4=Impact category.5=Multioutput process. 'Unit process' contains the description
        of processes and their direct (in situ) elementary flows (emissions and resource
        consumption) and intermediate product flows (demand for energy carriers, waste
        treatment and transport services, working materials, etc.), so-called unit
        process raw data. Data that arrives at the ecoinvent database in the form of
        life cycle inventory results are nevertheless classified as unit process.
        'System non-terminated' is not used in the ecoinvent quality network.
        'System terminated' contains the cumulative elementary flows (i.e. the life
        cycle inventory result) of a unit process. This code is only used for
        datasets calculated within the ecoinvent database (LCI results).
        'Elementary flow' contains the definition of pollutants and of resources.
        'Impact category' contains the definition of the characterisation, damage or
        weighting factors of life cycle impact assessment methods. 'Multioutput process'
        is a special kind of unit process, which delivers more than one product/service
        output.
        """
        return int(self.get("type"))

    @property
    def typeStr(self) -> str:
        """String representation for type. See type for explanations.
        0=System non-terminated. 1=Unit process. 2=System terminated. 3=Elementary flow.
        4=Impact category.5=Multioutput process."""
        return self.typeMap[self.type]

    @property
    def impactAssessmentResult(self) -> bool:
        """Indicates whether or not (yes/no) the dataset contains the results of an
        impact assessment applied on unit processes (unit process raw data) or
        terminated systems (LCI results)."""
        return DataTypesConverter.str_to_bool(self.get("impactAssessmentResult"))

    @property
    def timestamp(self) -> datetime:
        """Automatically generated date when dataset is created"""
        return datetime.strptime(self.get("timestamp"), self.timestampFormat)

    @property
    def version(self) -> float:
        """The ecoinvent version number is used as follows: with a major update
        (e.g. every second year) the version number is increased by
        one (1.00, 2.00, etc.). The digits after the decimal point
        (e.g., 1.01, 1.02, etc.) are used for minor updates (corrected errors)
        within the period of two major updates. The version number is placed manually.
        """
        return float(self.get("version"))

    @property
    def internalVersion(self) -> float:
        """The internalVersion number is used to discern different versions during
        the working period until the dataset is entered into the database). The
        internalVersion is generated automatically with each change made in the
        dataset or related file."""
        return float(self.get("internalVersion"))

    @property
    def energyValues(self) -> int:
        """Indicates the way energy values are used and applied in the dataset. The
        codes are: 0=Undefined. 1=Net values. 2=Gross values. This data field is by
        default set to 0 and not actively used in ecoinvent quality network."""
        return int(self.get("energyValues"))

    @property
    def energyValuesStr(self) -> str:
        """String representation for energyValues. See energyValues for explanations.
        0=Undefined. 1=Net values. 2=Gross values."""
        return self.energyValuesMap[self.energyValues]

    @property
    def languageCode(self) -> str:
        """2 letter ISO language codes are used. Default language is English.
        Lower case letters are used."""
        return self.get("languageCode")

    @property
    def localLanguageCode(self) -> str:
        """2 letter ISO language codes are used. Default localLanguage is German.
        Lower case letters are used."""
        return self.get("localLanguageCode")


class TimePeriod(etree.ElementBase):
    """Contains all possible date-formats applicable to describe start and end date of
    the time period for which the dataset is valid."""

    @property
    def startYear(self) -> str:
        """Start date of the time period for which the dataset is valid, entered
        as year only."""
        return self.find("startYear", namespaces=self.nsmap).text

    @property
    def startYearMonth(self) -> str:
        """Start date of the time period for which the dataset is valid, entered
        as year and month."""
        return self.find("startYearMonth", namespaces=self.nsmap).text

    @property
    def startDate(self) -> str:
        """Start date of the time period for which the dataset is valid, presented
        as a complete date (year-month-day). StartDate may as well be entered as year
        (0000) or year-month (0000-00) only. 2000 and 2000-01 means: from 01.01.2000.
        If it is only known that data is older than a certain data, 'startDate' is left
        blank."""
        return self.find("startDate", namespaces=self.nsmap).text

    @property
    def endYear(self) -> str:
        """End date of the time period for which the dataset is valid, entered as year
        only."""
        return self.find("endYear", namespaces=self.nsmap).text

    @property
    def endYearMonth(self) -> str:
        """End date of the time period for which the dataset is valid, entered as year
        and month."""
        return self.find("endYearMonth", namespaces=self.nsmap).text

    @property
    def endDate(self) -> str:
        """End date of the time period for which the dataset is valid, presented as a
        complete date (year-month-day). EndDate may as well be entered as year (0000)
        or year-month (0000-00) only. 2000 and 2000-12 means: until 31.12.2000."""
        return self.find("endDate", namespaces=self.nsmap).text

    @property
    def dataValidForEntirePeriod(self) -> bool:
        """Indicates whether or not the process data (elementary and intermediate
        product flows reported under flow data) are valid for the entire time period
        stated. If not, explanations may be given under 'text'."""
        return DataTypesConverter.str_to_bool(self.get("dataValidForEntirePeriod"))

    @property
    def text(self) -> str:
        """Additional explanations concerning the temporal validity of the flow data
        reported. It may comprise information about:
            - how strong the temporal correlation is for the unit process at issue
            (e.g., are four year old data still adequate for the process operated
            today?),
            - why data is not valid for the entire period,
            - for which smaller periods data are valid,
            - whether for certain elementary and intermediate product flows a different
            time period is valid.
        The fact that data are based on forecasts should be reported under
        'representativeness'."""
        return self.get("text")


class Representativeness(etree.ElementBase):
    """Contains information about the fraction of the relevant market supplied by the
    product/service described in the dataset. Information about market share,
    production volume (in the ecoinvent quality network: also consumption volume in
    the market area) and information about how data have been sampled."""

    @property
    def percent(self) -> float:
        """Indicates the share in market supply in the geographical area indicated
        of the product/service at issue. If data representative for a process operated
        in one country is used for another country's process, the entry should be '0'.
        The representativity for the original country is reported under
        'extrapolations'."""
        return float(self.get("percent"))

    @property
    def productionVolume(self) -> str:
        """Indicates the market area consumption volume (NOT necessarily identical with
        the production volume) in the geographical area indicated of the product/service
        at issue. The market volume should be given in absolute terms per year and in
        common units. It is related to the time period specified elsewhere.
        """
        return self.get("productionVolume")

    @property
    def samplingProcedure(self) -> str:
        """Indicates the sampling procedure applied for quantifying the exchanges. It
        should be reported whether the sampling procedure for particular elementary
        and intermediate product flows differ from the general procedure. Possible
        problems in combining different sampling procedures should be mentioned."""
        return self.get("samplingProcedure")

    @property
    def extrapolations(self) -> str:
        """Describes extrapolations of data from another time period, another
        geographical area or another technology and the way these extrapolations
        have been carried out. It should be reported whether different extrapolations
        have been done on the level of individual exchanges. If data representative for
        a process operated in one country is used for another country's process, its
        original representativity can be indicated here. Changes in mean values
        due to extrapolations may also be reported here."""
        return self.get("extrapolations")

    @property
    def uncertaintyAdjustments(self) -> str:
        """For datasets where the additional uncertainty from lacking representativeness
        has been included in the quantified uncertainty values ('minValue' and
        'maxValue'), thus raising the value in 'percent' of the dataset to 100%, this
        field also reports the original representativeness, the additional uncertainty
        and the procedure by which it was assessed or calculated."""
        return self.get("uncertaintyAdjustments")


class Source(etree.ElementBase):
    """Contains information about author(s), title, kind of publication, place of
    publication, name of editors (if any), etc.."""

    sourceTypeMap: Dict[int, str] = {
        0: "Undefined (default)",
        1: "Article",
        2: "Chapters in anthology",
        3: "Seperate publication",
        4: "Measurement on site",
        5: "Oral communication",
        6: "Personal written communication",
        7: "Questionnaries"
    }

    @property
    def number(self) -> int:
        """ID number to identify the source within one dataset."""
        return int(self.get("number"))

    @property
    def sourceType(self) -> int:
        """Indicates the kind of source. The codes are: 0=Undefined (default).
        1=Article. 2=Chapters in anthology. 3=Seperate publication.
        4=Measurement on site. 5=Oral communication. 6=Personal written communication.
        7=Questionnaries."""
        return int(self.get("sourceType"))

    @property
    def sourceTypeStr(self) -> str:
        """String representation for sourceType. See sourceType for explanations.
        0=Undefined (default). 1=Article. 2=Chapters in anthology.
        3=Seperate publication. 4=Measurement on site. 5=Oral communication.
        6=Personal written communication. 7=Questionnaries."""
        return self.sourceTypeMap[self.sourceType]

    @property
    def firstAuthor(self) -> str:
        """Indicates the first author by surname and abbreviated name
        (e.g., Einstein A.). In case of measurement on site, oral communication,
        personal written communication and questionnaries ('sourceType'=4, 5, 6, 7)
        the name of the communicating person is mentioned here. Identifies the
        source together with 'title' and 'year'."""
        return self.get("firstAuthor")

    @property
    def additionalAuthors(self) -> str:
        """List of additional authors (surname and abbreviated name, e.g. Newton I.),
        separated by commas. 'Et al.' may be used, if more than five additonal authors
        contributed to the cited publication."""
        return self.get("additionalAuthors")

    @property
    def year(self) -> int:
        """Indicates the year of publication and communication, respectively. Identifies
        the source together with 'firstAuthor' and 'title'."""
        return int(self.get("year"))

    @property
    def title(self) -> str:
        """Measurement on site: write "Measurement documentation of company XY".
        Oral communication: write "Oral communication, company XY". Personal written
        communication: write: "personal written communication, Mr./Mrs. XY, company Z".
        Questionnaires: write "Questionnaire, filled in by Mr./Mrs. XY, company Z".
        Identifies the source together with 'firstAuthor' and 'year'."""
        return self.get("title")

    @property
    def pageNumbers(self) -> str:
        """If an article or a chapter in an anthology, list the relevant page numbers.
        In case of separate publications the total number of pages may be entered."""
        return self.get("pageNumbers")

    @property
    def nameOfEditors(self) -> str:
        """Contains the names of the editors (if any)."""
        return self.get("nameOfEditors")

    @property
    def titleOfAnthology(self) -> str:
        """If the publication is a chapter in an anthology, the title of the anthology
        is reported here. For the reports of the ecoinvent quality network 'Final report
        ecoinvent 2000' is written here."""
        return self.get("titleOfAnthology")

    @property
    def placeOfPublications(self) -> str:
        """Indicates the place(s) of publication. In case of measurements on site, oral
        communication, personal written communication or questionnaires, it is the
        location of the company which provided the information. If available via the
        web add the web-address. For the ECOINVENT final reports 'EMPA Dübendorf' is
        written."""
        return self.get("placeOfPublications")

    @property
    def publisher(self) -> str:
        """Lists the name of the publisher (if any). In case of the ecoinvent quality
        network it is the 'Swiss Centre for Life Cycle Inventories'."""
        return self.get("publisher")

    @property
    def journal(self) -> str:
        """Indicates the name of the journal an article is published in."""
        return self.get("journal")

    @property
    def volumeNo(self) -> int:
        """Indicates the volume of the journal an article is published in."""
        return int(self.get("volumeNo"))

    @property
    def issueNo(self) -> str:
        """Indicates the issue number of the journal an article is published in."""
        return self.get("issueNo")

    @property
    def text(self) -> str:
        """Free text for additional description of the source. It may contain a
        brief summary of the publication and the kind of medium used (e.g. CD-ROM,
        hard copy)"""
        return self.get("text")


class Validation(etree.ElementBase):
    """Contains information about who carried out the critical review and about
    the main results and conclusions of the revie and the recommendations made."""

    @property
    def proofReadingDetails(self) -> str:
        """Contains the comment of the reviewer of the dataset. For the ecoinvent
        quality network the review text should cover the following items:
        1. completeness and transparency of the documentation, 2. conformity with
        the ecoinvent quality guidelines, 3. plausibility of the data (unit process
        elementary and intermediate product flows), 4. completeness regarding
        elementary and intermediate product flows, 5. mathematical correctness.
        The review is limited to sample audits (not covering each and every figure).
        """
        return self.get("proofReadingDetails")

    @property
    def proofReadingValidator(self) -> int:
        """Indicates the person who carried out the review. ID number must correspond
        to an ID number of a person listed in the respective dataset."""
        return int(self.get("proofReadingValidator"))

    @property
    def otherDetails(self) -> str:
        """Contains further information from the review process, especially comments
        received from third parties once the dataset has been published."""
        return self.get("otherDetails")


class DataEntryBy(etree.ElementBase):
    """Contains information about the person that entered data in the database or
    transformed data into the format of the ecoinvent (or any other) quality network.
    """

    @property
    def person(self) -> int:
        """ID number for the person that prepared the dataset and enters the dataset
        into the database. It must correspond to an ID number of a person listed in
        the respective dataset."""
        return int(self.get("person"))

    @property
    def qualityNetwork(self) -> int:
        """Indicates a project team that works on the database. The information is
        used, e.g., for restricting the accessibility of dataset information to one
        particular quality network. The code used is: 1=ecoinvent"""
        return int(self.get("qualityNetwork", Defaults.qualityNetwork))


class DataGeneratorAndPublication(etree.ElementBase):
    """Contains information about who compiled for and entered data into the
    database. Furthermore contains information about kind of publication underlying
    the dataset and the accessibility of the dataset."""

    dataPublishedInMap: Dict[int, str] = {
        0: "Data as such notpublished (default)",
        1: "The data of some unit processes or subsystems are published",
        2: "Data has been published entirely in 'referenceToPublishedSource'"
    }

    accessRestrictedToMap: Dict[int, str] = {
        0: "Public",
        1: "ETH Domain",
        2: "ecoinvent 2000",
        3: "Institute"
    }

    @property
    def person(self) -> int:
        """ID number for the person that generated the dataset. It must correspond to
        an ID number of a person listed in the respective dataset."""
        return int(self.get("person"))

    @property
    def dataPublishedIn(self) -> int:
        """Indicates whether the dataset has been published (not, partly, entirely).
        The codes are: 0=Data as such not published (default). 1=The data of some unit
        processes or subsystems are published. 2=Data has been published entirely in
        'referenceToPublishedSource'. Within the ecoinvent quality network all datasets
        are published in the series of ecoinvent reports."""
        return int(self.get("dataPublishedIn"))

    @property
    def dataPublishedInStr(self) -> str:
        """String representation for dataPublishedIn. See dataPublishedIn for
        explanations. 0=Data as such not published (default). 1=The data of some unit
        processes or subsystems are published. 2=Data has been published entirely in
        'referenceToPublishedSource'"""
        return self.dataPublishedInMap[self.dataPublishedIn]

    @property
    def referenceToPublishedSource(self) -> int:
        """ID number for the report in which the dataset is documented. It must
        correspond to an ID number of a source listed in the respective dataset."""
        return int(self.get("referenceToPublishedSource"))

    @property
    def copyright(self) -> bool:
        """Indicates whether or not a copyright exists. '1' (Yes) or '0' (No)
        should be entered correspondingly."""
        return DataTypesConverter.str_to_bool(self.get("copyright"))

    @property
    def accessRestrictedTo(self) -> int:
        """Indicates possible access restrictions for the dataset. The codes
        used are: 0=Public. 1=ETH Domain. 2=ecoinvent 2000. 3=Institute. If access
        is restricted to a particular institute, 'companyCode' and 'countryCode'
        indicates the institute that has access to the data. accessRestrictedTo=0:
        all information can be accessed by everybody accessRestrictedTo=1,
        2: ecoinvent clients have access to LCI results but not to unit process
        raw data. Members of the ecoinvent quality network (ecoinvent centre)
        have access to all information.  accessRestrictedTo=3: The ecoinvent
        administrator has full access to information. Via the web only LCI result
        are accessible (for ecoinvent clients and for members of the ecoinvent centre.
        """
        return int(self.get("accessRestrictedTo"))

    @property
    def accessRestrictedToStr(self) -> str:
        """String representation for accessRestrictedTo. See accessRestrictedTo for
        explanations. The codes used are: 0=Public. 1=ETH Domain. 2=ecoinvent 2000.
        3=Institute. If access is restricted to a particular institute, 'companyCode'
        and 'countryCode' indicates the institute that has access to the data.
        accessRestrictedTo=0: all information can be accessed by everybody
        accessRestrictedTo=1, 2: ecoinvent clients have access to LCI results but not
        to unit process raw data. Members of the ecoinvent quality network (ecoinvent
        centre) have access to all information. accessRestrictedTo=3: The ecoinvent
        administrator has full access to information. Via the web only LCI results are
        accessible (for ecoinvent clients and for members of the ecoinvent centre."""
        return self.accessRestrictedToMap[self.accessRestrictedTo]

    @property
    def companyCode(self) -> str:
        """7 letter code with which organisations/institutes that co-operate within one
        of the database quality networks (see also 'qualityNetwork') are characterised
        and identified. 'countryCode' is required additionally. Only required and
        allowed if access to the dataset is restricted to a particular institute within
        the ecoinvent quality network."""
        return self.get("companyCode")

    @property
    def countryCode(self) -> str:
        """2 letter ISO-country codes are used to indicate the country where
        organisations/institutes are located which co-operate within one of the database
        quality networks (see also 'qualityNetwork'). Only required and allowed if
        access to the dataset is restricted to a particular institute within the
        ecoinvent quality network."""
        return self.get("countryCode")

    @property
    def pageNumbers(self) -> str:
        """Indicates the page numbers in the publication where the table with the unit
        process raw data, and the characterisation, damage or weighting factors of the
        impact category, respectively are documented."""
        return self.get("pageNumbers")


class Person(etree.ElementBase):
    """Used for the identification of members of the organisation institute co-operating
    within a quality network (e.g., ecoinvent) referred to in the areas Validation,
    dataEntryBy and dataGeneratorAndPublication."""

    @property
    def number(self) -> int:
        """ID number is attributed to each person of an organisation/institute
        co-operating in a quality network such as ecoinvent. It is used to identify
        persons cited within one dataset."""
        return int(self.get("number"))

    @property
    def name(self) -> str:
        """Name and surname of the person working in an organisation/institute which is
        a member of the quality network. Identifies the person together with
        'address' (#5803)."""
        return self.get("name")

    @property
    def address(self) -> str:
        """Complete address, including street, po-box (if applicable), zip-code,
        city, state (if applicable), country. Identifies the person together with
        'name' (#5802)."""
        return self.get("address")

    @property
    def telephone(self) -> str:
        """Phone number including country and regional codes."""
        return self.get("telephone")

    @property
    def telefax(self) -> str:
        """Fax number including country and regional codes."""
        return self.get("telefax")

    @property
    def email(self) -> str:
        """Complete email address."""
        return self.get("email")

    @property
    def companyCode(self) -> str:
        """7 letter company code of the organisation/institute co-operating in a
        quality network. Identifies the co-operation partner together with the
        countryCode (#5808)."""
        return self.get("companyCode")

    @property
    def countryCode(self) -> str:
        """2 letter ISO-country code of the organisation/institute co-operating
        in a quality network. Identifying the co-operation partner together with
        the companyCode (#5807)."""
        return self.get("countryCode")
