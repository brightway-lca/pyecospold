"""Custom EcoSpold Python classes for v1 of EcoSpold schema."""
from datetime import datetime
from typing import ClassVar, Dict, List

from lxml import etree
from lxmlh import get_element, get_element_list
from pycasreg.validation import validate_cas

from .helpers import (
    create_attribute_list_v1,
    create_attribute_v1,
    create_element_text_v1,
)


class EcoSpold(etree.ElementBase):
    """The data (exchange) format of the ECOINVENT quality network. A dataset
    describes LCI related information of a unit process or a terminated system
    comprising metaInformation (description of the process) and flowData
    (quantified inputs and outputs and allocation factors, if any)."""

    validationId = create_attribute_v1("validationId", int)
    """int:"""

    validationStatus = create_attribute_v1("validationStatus", str)
    """str:"""

    @property
    def datasets(self) -> List["Dataset"]:
        """Contains information about one individual unit process (or terminated
        system). Information is divided into metaInformation and flowData."""
        return get_element_list(self, "dataset")


class Dataset(etree.ElementBase):
    """Contains information about one individual unit process (or terminated
    system). Information is divided into metaInformation and flowData."""

    number = create_attribute_v1("number", int)
    """int: ID number used as an identifier of the dataset."""

    internalSchemaVersion = create_attribute_v1("internalSchemaVersion", str)

    generator = create_attribute_v1("generator", str)
    """str: The person or organisation that collected, compiled or published the
    original data."""

    timestamp = create_attribute_v1("timestamp", datetime)
    """datetime: Automatically generated date when dataset is created"""

    validCompanyCodes = create_attribute_v1("validCompanyCodes", str)
    """str: XML file for valid company codes."""

    validRegionalCodes = create_attribute_v1("validRegionalCodes", str)
    """str: XML file for valid regional codes."""

    validCategories = create_attribute_v1("validCategories", str)
    """str: XML file for valid categories."""

    validUnits = create_attribute_v1("validUnits", str)
    """str: XML file for valid units."""

    @property
    def metaInformation(self) -> "MetaInformation":
        """Contains information about the process (its name, (functional) unit,
        classification, technology, geography, time, etc.), about modelling
        assumptions and validation details and about dataset administration
        (version number, kind of dataset, language)."""
        return get_element(self, "metaInformation")

    @property
    def flowData(self) -> "FlowData":
        """Contains information about inputs and outputs (to and from nature
        as well as to and from technosphere) and information about allocation
        (flows to be allocated, co-products to be allocated to, allocation
        factors)."""
        return get_element(self, "flowData")


class MetaInformation(etree.ElementBase):
    """Contains information about the process (its name, (functional) unit,
    classification, technology, geography, time, etc.), about modelling
    assumptions and validation details and about dataset administration
    (version number, kind of dataset, language)."""

    @property
    def processInformation(self) -> "ProcessInformation":
        """Contains content-related metainformation for the unit process."""
        return get_element(self, "processInformation")

    @property
    def modellingAndValidation(self) -> "ModellingAndValidation":
        """Contains metaInformation about how unit processes are modelled
        and about the review/validation of the dataset."""
        return get_element(self, "modellingAndValidation")

    @property
    def administrativeInformation(self) -> "AdministrativeInformation":
        """Contains information about the person that compiled and entered
        the dataset in the database and about kind of publication and the
        accessibility of the dataset."""
        return get_element(self, "administrativeInformation")


class FlowData(etree.ElementBase):
    """Contains information about inputs and outputs (to and from nature
    as well as to and from technosphere) and information about allocation
    (flows to be allocated, co-products to be allocated to, allocation
    factors)."""

    @property
    def exchanges(self) -> List["Exchange"]:
        """Comprises all inputs and outputs (both elementary flows and
        intermediate product flows) registered in a unit process."""
        return get_element_list(self, "exchange")

    @property
    def allocations(self) -> List["Allocation"]:
        """Comprises all referenceToInputOutput."""
        return get_element_list(self, "allocation")


class ProcessInformation(etree.ElementBase):
    """Contains content-related metainformation for the unit process."""

    @property
    def referenceFunction(self) -> "ReferenceFunction":
        """Comprises information which identifies and characterises one particular
        dataset (=unit process or system terminated)."""
        return get_element(self, "referenceFunction")

    @property
    def geography(self) -> "Geography":
        """Contains information about the geographic validity of the process. The region
        described with regional code and free text is the market area of the
        product / service at issue and not necessarily the place of production."""
        return get_element(self, "geography")

    @property
    def technology(self) -> "Technology":
        """Contains a description of the technology for which flow data have been
        collected. Free text can be used. Pictures, graphs and tables are not allowed.
        The text should cover information necessary to identify the properties and
        particularities of the technology(ies) underlying the process data."""
        return get_element(self, "technology")

    @property
    def dataSetInformation(self) -> "DataSetInformation":
        """Contains the administrative information about the dataset at issue: type of
        dataset (unit process, elementary flow, impact category, multi-output process)
        timestamp, version and internalVersion number as well as language and
        localLanguage code."""
        return get_element(self, "dataSetInformation")

    @property
    def timePeriod(self) -> "TimePeriod":
        """Contains all possible date-formats applicable to describe start and end date
        of the time period for which the dataset is valid."""
        return get_element(self, "timePeriod")


class ModellingAndValidation(etree.ElementBase):
    """Contains metaInformation about how unit processes are modelled
    and about the review/validation of the dataset."""

    @property
    def representativeness(self) -> "Representativeness":
        """Contains information about the fraction of the relevant market supplied by
        the product/service described in the dataset. Information about market share,
        production volume (in the ecoinvent quality network: also consumption volume in
        the market area) and information about how data have been sampled."""
        return get_element(self, "representativeness")

    @property
    def source(self) -> "Source":
        """Contains information about author(s), title, kind of publication,
        place of publication, name of editors (if any), etc.."""
        return get_element(self, "source")

    @property
    def validation(self) -> "Validation":
        """Contains information about who carried out the critical review
        and about the main results and conclusions of the revie and the
        recommendations made."""
        return get_element(self, "validation")


class AdministrativeInformation(etree.ElementBase):
    """Contains information about the person that compiled and entered
    the dataset in the database and about kind of publication and the
    accessibility of the dataset."""

    @property
    def dataEntryBy(self) -> "DataEntryBy":
        """Contains information about the person that entered data in the
        database or transformed data into the format of the ecoinvent
        (or any other) quality network."""
        return get_element(self, "dataEntryBy")

    @property
    def dataGeneratorAndPublication(self) -> "DataGeneratorAndPublication":
        """Contains information about who compiled for and entered data into
        the database. Furthermore contains information about kind of publication
        underlying the dataset and the accessibility of the dataset."""
        return get_element(self, "dataGeneratorAndPublication")

    @property
    def persons(self) -> List["Person"]:
        """Used for the identification of members of the organisation institute
        co-operating within a quality network (e.g., ecoinvent) referred to in
        the areas Validation, dataEntryBy and dataGeneratorAndPublication."""
        return get_element_list(self, "person")


class Exchange(etree.ElementBase):
    """Comprises all inputs and outputs (both elementary flows and
    intermediate product flows) recorded in a unit process and its
    related information."""

    INPUT_GROUPS_MAP: ClassVar[Dict[int, str]] = {
        1: "Materials/Fuels",
        2: "Electricity/Heat",
        3: "Services",
        4: "FromNature",
        5: "FromTechnosphere",
    }

    OUTPUT_GROUPS_MAP: ClassVar[Dict[int, str]] = {
        0: "ReferenceProduct",
        1: "Include avoided product system",
        2: "Allocated by product",
        3: "WasteToTreatment",
        4: "ToNature",
    }

    UNCERTAINTY_TYPE_MAP: ClassVar[Dict[int, str]] = {
        0: "undefined",
        1: "lognormal",
        2: "normal",
        3: "triang",
        4: "uniform",
    }

    _inputGroups = create_attribute_list_v1("inputGroup", int)
    """List[int]: Indicates the kind of input flow. The codes are:
    1=Materials/Fuels, 2=Electricity/Heat, 3=Services, 4=FromNature,
    5=FromTechnosphere. Within the ecoinvent quality network,
    only 4 and 5 are actively used (any material, fuel, electricity,
    heat or service is classified as an input from technosphere)."""

    _outputGroups = create_attribute_list_v1("outputGroup", int)
    """List[int]: Indicates the kind of output flow. The codes are: 0=ReferenceProduct,
    1=Include avoided product system, 2=Allocated by product,
    3=WasteToTreatment, 4=ToNature. The options 0, 2, and 4 are actively used
    in the ecoinvent quality network. Products of multioutput processes are
    classified as allocated by-products (2). Avoided product systems are modelled
    with a negative input from technosphere. WasteToTreatment are modelled like
    services (hence inputFromTechnosphere). Therefore codes '1' and '3' are not
    required."""

    number = create_attribute_v1("number", int)
    """int: ID number used as an identifier of a particular exchange
    in a dataset."""

    category = create_attribute_v1("category", str)
    """str: Describes the category one particular exchange belongs to
    (in English language). Category and subCategory are required for
    elementary flows because they have a discriminative function."""

    subCategory = create_attribute_v1("subCategory", str)
    """str: Describes the subCategory one particular exchange belongs to
    (in English language). Category and subCategory are required for
    elementary flows because they have a discriminative function."""

    localCategory = create_attribute_v1("localCategory", str)
    """str: Describes the category one particular exchange belongs to
    (in German local language).See further explanations in 'category'.
    """

    localSubCategory = create_attribute_v1("localSubCategory", str)
    """str: Describes the subCategory one particular exchange belongs to
    (in German local language).See further explanations in
    'subCategory'."""

    CASNumber = create_attribute_v1("CASNumber", str, validate_cas)
    """str: Indicates the number according to the Chemical Abstract
    Service (CAS). The Format of the CAS-number: 000000-00-0,
    where the first string of digits needs not to be complete
    (i.e. less than six digits are admitted)."""

    name = create_attribute_v1("name", str)
    """str: Name of the exchange (elementary flow or intermediate
    product flow) in English language. See 'name' in
    'metaInformation/referenceFunction' for more explanations."""

    location = create_attribute_v1("location", str)
    """str: Area information for the intermediate product/service flow.
    Location is defined by a 7 letter code written with capital
    letters. See 'metaInformation/referenceFunction' for more
    explanations. Information about the geographic area for which
    an impact assessment method is valid. Not applicable for
    elementary flows."""

    unit = create_attribute_v1("unit", str)
    """str: Unit of the exchange (elementary flow or intermediate product
    flow). See 'metaInformation/referenceFunction' for more
    explanations. Unit of the elementary flow for which a
    characterisation, damage or weighting factor is determined."""

    meanValue = create_attribute_v1("meanValue", float)
    """float: Mean amount of elementary flow or intermediate product flow.
    In case of triangular uncertainty distribution, the meanValue shall
    be calculated from the mostLikelyValue. The field mostLikelyValue (#3797)
    shall not be used in the ecoinvent quality network."""

    uncertaintyType = create_attribute_v1("uncertaintyType", int)
    """int: Defines the kind of uncertainty distribution applied on one particular
    exchange. Lognormal distribution is default, normal, triangular or
    uniform distribution may be chosen if appropriate. 0=undefined,
    1=lognormal (default), 2=normal, 3=triang, 4=uniform"""

    standardDeviation95 = create_attribute_v1("standardDeviation95", float)
    """float: Defines the 2.5% and the 97.5% value for the uncertainty range
    with normal and lognormal distribution. For lognormal distribution
    the square of the geometric standard deviation (SDg^2) is entered.
    SDg^2 is dimensionless. MeanValue times SDg^2 equals the 97.5% value
    (=maxValue), meanvalue divided by SDg^2 equals the 2.5% value
    (=minValue). For normal distribution the double standard deviation
    (2*SD) is entered. 2*SD is given in the same unit like the meanValue.
    MeanValue plus 2*SD equals 97.5% value (=maxValue), meanValue minus
    2*SD equals 2.5% value (=minValue). This data field remains empty when
    uniform or triangular uncertainty distribution is applied
    (uncertaintyType = 3 and 4, respectively)."""

    formula = create_attribute_v1("formula", str)
    """str: Chemical formula (e.g. sum formula) may be entered. No graphs are
    allowed to represent chemical formulas."""

    referenceToSource = create_attribute_v1("referenceToSource", int)
    """int: An ID used in the area 'sources' of the respective dataset is
    required. It indicates the publication (of the ecoinvent quality
    network) where the unit process raw data at issue and the
    characterisation, damage or weighting factors of an impact category,
    respectively, are documented."""

    pageNumbers = create_attribute_v1("pageNumbers", str)
    """str: The page numbers of the publication (of the ecoinvent quality
    network) where the exchanges of the unit process at issue are
    documented."""

    generalComment = create_attribute_v1("generalComment", str)
    """str: A general comment can be made about each individual exchange
    (or characterisation, damage or weighting factor) of a particular
    unit process and impact category, respectively. It contains the
    string of code numbers of the ecoinvent uncertainty assessment
    (if pedigree matrix is applied) as well as further comments
    about the uncertainty assessment. The string of numbers of the
    uncertainty assessment describes (reliability, completeness,
    temporal correlation, geographical correlation, further technical
    correlation, sample size) and uses a score from 1 to 5. See
    methodology report for further information."""

    localName = create_attribute_v1("localName", str)
    """str: Name of the exchange (or characterisation, damage or weighting
    factor) of a particular unit process and impact category,
    respectively (in German local language)."""

    infrastructureProcess = create_attribute_v1("infrastructureProcess", bool)
    """bool: Describes whether the intermediate product flow from or to the
    unit process is an infrastructure process or not. Not applicable
    to elementary flows."""

    minValue = create_attribute_v1("minValue", float)
    """float: Contains the minimum value for exchange data with a uniform or
    triangular distribution. In case of LCI results imported into the
    ecoinvent database, the 2.5% value is reported in this field."""

    maxValue = create_attribute_v1("maxValue", float)
    """float: Contains the maximum value for exchange data with a uniform or
    triangular distribution. In case of LCI results imported into the
    ecoinvent database, the 97.5% value is reported in this field."""

    mostLikelyValue = create_attribute_v1("mostLikelyValue", float)
    """float: In some cases the MostLikelyValue is available for exhange data
    with triangular distribution. However, do not use this field, but
    calculate the mean value, (minValue + mostLikelyValue +maxValue)/3,
    and enter it into the field "meanValue")."""

    @property
    def groups(self) -> List[int]:
        """Choice between _inputGroups and _outputGroups. Check their documentation
        for more information."""
        return self._inputGroups if self._inputGroups != [] else self._outputGroups

    @property
    def groupsStr(self) -> List[str]:
        """Choice between _inputGroupsStr and _outputGroupsStr. Check their
        documentation for more information."""
        return (
            self._inputGroupsStr if self._inputGroups != [] else self._outputGroupsStr
        )

    @property
    def _inputGroupsStr(self) -> List[str]:
        """String representation for inputGroups. See inputGroups for
        explanations. 1=Materials/Fuels, 2=Electricity/Heat, 3=Services,
        4=FromNature, 5=FromTechnosphere."""
        return [
            Exchange.INPUT_GROUPS_MAP[inputGroup] for inputGroup in self._inputGroups
        ]

    @property
    def _outputGroupsStr(self) -> List[str]:
        """String representation for outputGroups. See outputGroups for
        explanations. 0=ReferenceProduct, 1=Include avoided product system,
        2=Allocated by product, 3=WasteToTreatment, 4=ToNature"""
        return [
            Exchange.OUTPUT_GROUPS_MAP[outputGroup]
            for outputGroup in self._outputGroups
        ]

    @property
    def uncertaintyTypeStr(self) -> str:
        """String representation for uncertaintyType. See uncertaintyType for
        explanations. 0=undefined, 1=lognormal (default), 2=normal, 3=triang,
        4=uniform"""
        return Exchange.UNCERTAINTY_TYPE_MAP[self.uncertaintyType]


class Allocation(etree.ElementBase):
    """Contains all information about allocation procedure, allocation
    parameters and allocation factors applied on a multi-output process."""

    ALLOCATION_METHOD_MAP: ClassVar[Dict[int, str]] = {
        -1: "Undefined",
        0: "Physical causality",
        1: "Economic causality",
        2: "Othermethod",
    }

    referenceToInputOutputs = create_attribute_list_v1("referenceToInputOutput", int)
    """List[int]: The data field is only required, if the reference function describes
    a multioutput process. Lists the relation(s) to which a certain allocation
    factor is applied. MultipleOccurrence=Yes on two levels: Firstly, the
    reference occurs per co-product and secondly, the reference occurs per
    input and output flows which are allocated to the co-products."""

    referenceToCoProduct = create_attribute_v1("referenceToCoProduct", int)
    """int: Indicates the co-product output for which a particular allocation
    factor is valid. Additional information is required about the exchange
    on which the allocation factor is applied (see 'referenceToInputOutput').
    MultipleOccurences=Yes is only valid, if referenceFunction
    describes a multioutput process."""

    allocationMethod = create_attribute_v1("allocationMethod", int)
    """int: Indicates the kind of allocation parameter chosen. The codes are:
    -1=Undefined (default). 0=Physical causality. 1=Economic causality. 2=Other
    method. 'Other method' comprises in particular physical parameters (like mass,
    energy, exergy, etc.) and parameters other than economic. MultipleOccurences=Yes
    only valid, if referenceFunction describes a multioutput process."""

    fraction = create_attribute_v1("fraction", float)
    """float: Allocation factor, expressed as a fraction (in %), applied on one
    particular exchange for one particular co-product. The sum of the allocation
    factors applied on one particular exchange must add up to 100%.
    MultipleOccurences=Yes only valid, if referenceFunction describes
    a multioutput process."""

    explanations = create_attribute_v1("explanations", str)
    """str: Contains further information about the allocation procedure and
    the allocation parameter chosen. An eventual coincidence in allocation factors
    when comparing different allocation parameters (like physical and economic ones)
    may be reported here as well."""

    @property
    def allocationMethodStr(self) -> str:
        """String representation for allocationMethod. See allocationMethod for
        explanations. -1=Undefined (default). 0=Physical causality. 1=Economic
        causality. 2=Other method."""
        return Allocation.ALLOCATION_METHOD_MAP[self.allocationMethod]


class ReferenceFunction(etree.ElementBase):
    """
    Comprises information which identifies and characterises one particular dataset
    (=unit process or system terminated).
    """

    synonyms = create_attribute_list_v1("synonym", str)
    """List[str]: Synonyms for the name, localName. In the Excel editor they are
    separated by two slashes ('//'). Synonyms are a subset of referenceFunction.
    0..n entries are allowed with a max. length of 80 each."""

    datasetRelatesToProduct = create_attribute_v1("datasetRelatesToProduct", bool)
    """bool: Indicates whether the dataset relates to a process/service or not. In
    the ecoinvent quality network the value required is 'yes' for unit
    processes and multioutput processes and 'no' for elementary flows and
    impact categories."""

    name = create_attribute_v1("name", str)
    """str: Name of the unit process, elementary flow or impact category. For unit
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

    localName = create_attribute_v1("localName", str)
    """str: see 'name' for explanations. German is the default local language in the
    ecoinvent quality network."""

    infrastructureProcess = create_attribute_v1("infrastructureProcess", bool)
    """bool: Indicates whether the process is an investment or an operation process.
    Investment processes are for instance building of a nuclear power plant,
    a road, docks, construction of production machinery which deliver as the output
    a nuclear power plant, a km road, one seaport, and production machinery
    respectively. It is used as a discriminating element for the identification of
    processes. Not applicable for elementary flows and impact categories."""

    amount = create_attribute_v1("amount", float)
    """float: Indicates the amount of reference flow (product/service, elementary flow,
    impact category).  Within the ecoinvent quality network the amount of the
    reference flow always equals 1."""

    unit = create_attribute_v1("unit", str)
    """str: For unit processes (and systems terminated) it is the unit to which all
    inputs and outputs of the unit process are related to (functional unit).
    For elementary flows it is the unit in which exhanges are reported. For impact
    categories, it is the unit in which characterisation, damage or weighting
    factors are expressed. SI-units are preferred. The units are always expressed
    in English language."""

    category = create_attribute_v1("category", str)
    """str: Category is used to structure the content of the database (together with
    SubCategory). It is not required for the identification of a process (processes
    in different categories/subCategories may therefore not be named identically).
    But it is required for the identification of elementary flows and impact
    categories. Categories are administrated centrally. English is the default
    language in the ecoinvent quality network."""

    subCategory = create_attribute_v1("subCategory", str)
    """str: SubCategory is used to further structure the content of the database
    (together with category). It is not required for the identification of a
    process (processes in different categories/subCategories may therefore not be
    named identically). But it is required for the identification of elementary
    flows and impact categories. SubCategories are administrated centrally. English
    is the default language in the ecoinvent quality network."""

    localCategory = create_attribute_v1("localCategory", str)
    """str: See category for explanations. German is the default local language in the
    ecoinvent quality network."""

    localSubCategory = create_attribute_v1("localSubCategory", str)
    """"str: See subCategory for explanations. German is the default local language in
    the ecoinvent quality network."""

    includedProcesses = create_attribute_v1("includedProcesses", str)
    """"str: Contains a description of the (sub-)processes which are combined to form
    one unit process (e.g., 'operation of heating system' including operation of
    boiler unit, regulation unit and circulation pumps). Such combination may be
    necessary because of lack of detailedness in available data or because of data
    confidentiality. As far as possible and feasible, data should however be
    reported on the level of detail it has been received. Not applicable for
    elementary flows and impact categories."""

    generalComment = create_attribute_v1("generalComment", str)
    """str: Free text for general information about the dataset.
    It may contain information about:
        - the intended application of the dataset
        - information sources used
        - data selection principles
        -  modelling choices (exclusion of intermediate product flows, processes,
        allocation if done before entering into database).
    """

    infrastructureIncluded = create_attribute_v1("infrastructureIncluded", bool)
    """bool: Indicates whether the unit process imported into the database on the basis
    of an LCI result (received as cumulative mass- and energy-flows, hence, no LCI
    results will be calculated for such processes) has included infrastructure
    processes or not. For all other unit process raw data data sets this data field
    is empty. After calculation of LCI results in ecoinvent, the data field is
    filled in according to the fact, whether or not infrastructure has been
    including during the calculation. Not applicable for elementary flows and impact
    categories."""

    CASNumber = create_attribute_v1("CASNumber", str, validate_cas)
    """str: Indicates the number according to the Chemical Abstract Service (CAS).
    The Format of the CAS-number: 000000-00-0, where the first string of digits
    needs not to be complete (i.e. less than six digits are admitted).
    Not applicable for impact categories."""

    statisticalClassification = create_attribute_v1("statisticalClassification", int)
    """int: Contains the EU-classification system (NACE code). For the first edition
    of the ecoinvent database this data field will not be used. Not applicable
    for elementary flows and impact categories."""

    formula = create_attribute_v1("formula", str)
    """str: Chemical formula (e.g. sum formula) may be entered. No graphs are allowed
    to represent chemical formulas. Not applicable for impact categories."""


class Geography(etree.ElementBase):
    """Contains information about the geographic validity of the process. The region
    described with regional code and free text is the market area of the
    product / service at issue and not necessarily the place of production."""

    location = create_attribute_v1("location", str)
    """str: 7 letter regional code (capital letters). List of 2 letter ISO country
    codes extended by codes for regions, continents, market areas, and
    organisations and companies. The location code indicates the supply area
    of a product/service and the area of validity of impact assessment methods
    and impact categories, respectively. It does NOT necessarily coincide with
    the area/site of production or provenience. If supply and production area
    differ, production area is indicated in the name of the unit process."""

    text = create_attribute_v1("text", str)
    """str: Free text for further explanation. Text comprises additional aspects of
    the location, namely whether:
    - certain areas are exempted from the location indicated,
    - data are only valid for certain regions within the location indicated.
    - certain elementary flows or intermediate product flows are extrapolated
    from another geographical area than indicated.
    Extrapolations should be reported under 'representativeness'.
    """


class Technology(etree.ElementBase):
    """Contains a description of the technology for which flow data have been
    collected. Free text can be used. Pictures, graphs and tables are not allowed.
    The text should cover information necessary to identify the properties and
    particularities of the technology(ies) underlying the process data."""

    text = create_attribute_v1("text", str)
    """str: Describes the technological properties of the unit process. If the
    process comprises several subprocesses, the corresponding technologies
    should be reported as well. Professional nomenclature should be used for
    the description. The description helps the user to judge the technical
    suitability of the process dataset for his or her application (purpose).
    No graphs, figures or tables are allowed in this text field. It should be
    stated if data for certain elementary flows or intermediate product flows
    are derived from different technology."""


class DataSetInformation(etree.ElementBase):
    """Contains the administrative information about the dataset at issue: type of
    dataset (unit process, elementary flow, impact category, multi-output process)
    timestamp, version and internalVersion number as well as language and localLanguage
    code."""

    TYPE_MAP: Dict[int, str] = {
        0: "System non-terminated",
        1: "Unit process",
        2: "System terminated",
        3: "Elementary Flow",
        4: "Impact Category",
        5: "Multioutput process",
    }

    ENERGY_VALUES_MAP: Dict[int, str] = {
        0: "Undefined",
        1: "Net values",
        2: "Gross values",
    }

    type = create_attribute_v1("type", int)
    """int: Indicates the kind of data that is represented by this dataset. The code is:
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

    impactAssessmentResult = create_attribute_v1("impactAssessmentResult", bool)
    """bool: Indicates whether or not (yes/no) the dataset contains the results of an
    impact assessment applied on unit processes (unit process raw data) or
    terminated systems (LCI results)."""

    timestamp = create_attribute_v1("timestamp", datetime)
    """datetime: Automatically generated date when dataset is created"""

    version = create_attribute_v1("version", float)
    """float: The ecoinvent version number is used as follows: with a major update
    (e.g. every second year) the version number is increased by
    one (1.00, 2.00, etc.). The digits after the decimal point
    (e.g., 1.01, 1.02, etc.) are used for minor updates (corrected errors)
    within the period of two major updates. The version number is placed manually.
    """

    internalVersion = create_attribute_v1("internalVersion", float)
    """float: The internalVersion number is used to discern different versions during
    the working period until the dataset is entered into the database). The
    internalVersion is generated automatically with each change made in the
    dataset or related file."""

    energyValues = create_attribute_v1("energyValues", int)
    """int: Indicates the way energy values are used and applied in the dataset. The
    codes are: 0=Undefined. 1=Net values. 2=Gross values. This data field is by
    default set to 0 and not actively used in ecoinvent quality network."""

    languageCode = create_attribute_v1("languageCode", str)
    """str: 2 letter ISO language codes are used. Default language is English.
    Lower case letters are used."""

    localLanguageCode = create_attribute_v1("localLanguageCode", str)
    """str: 2 letter ISO language codes are used. Default localLanguage is German.
    Lower case letters are used."""

    @property
    def typeStr(self) -> str:
        """String representation for type. See type for explanations.
        0=System non-terminated. 1=Unit process. 2=System terminated. 3=Elementary flow.
        4=Impact category.5=Multioutput process."""
        return DataSetInformation.TYPE_MAP[self.type]

    @property
    def energyValuesStr(self) -> str:
        """String representation for energyValues. See energyValues for explanations.
        0=Undefined. 1=Net values. 2=Gross values."""
        return DataSetInformation.ENERGY_VALUES_MAP[self.energyValues]


class TimePeriod(etree.ElementBase):
    """Contains all possible date-formats applicable to describe start and end date of
    the time period for which the dataset is valid."""

    dataValidForEntirePeriod = create_attribute_v1("dataValidForEntirePeriod", bool)
    """bool: Indicates whether or not the process data (elementary and intermediate
    product flows reported under flow data) are valid for the entire time period
    stated. If not, explanations may be given under 'text'."""

    text = create_attribute_v1("text", str)
    """str: Additional explanations concerning the temporal validity of the flow data
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

    _startYear = create_element_text_v1("startYear", str)
    """str: Start date of the time period for which the dataset is valid, entered
    as year only."""

    _startYearMonth = create_element_text_v1("startYearMonth", str)
    """str: Start date of the time period for which the dataset is valid, entered
    as year and month."""

    _startDate = create_element_text_v1("startDate", str)
    """str: Start date of the time period for which the dataset is valid, presented
    as a complete date (year-month-day). StartDate may as well be entered as year
    (0000) or year-month (0000-00) only. 2000 and 2000-01 means: from 01.01.2000.
    If it is only known that data is older than a certain data, 'startDate' is left
    blank."""

    _endYear = create_element_text_v1("endYear", str)
    """str: End date of the time period for which the dataset is valid, entered as year
    only."""

    _endYearMonth = create_element_text_v1("endYearMonth", str)
    """str: End date of the time period for which the dataset is valid, entered as year
    and month."""

    _endDate = create_element_text_v1("endDate", str)
    """str: End date of the time period for which the dataset is valid, presented as a
    complete date (year-month-day). EndDate may as well be entered as year (0000)
    or year-month (0000-00) only. 2000 and 2000-12 means: until 31.12.2000."""

    @property
    def startDate(self) -> datetime:
        """Start date of the time period for which the dataset is valid. If it is only
        known that data is older than a certain data, 'startDate' is left blank."""
        return self._parse_date(self._startDate)

    @startDate.setter
    def startDate(self, date: datetime) -> None:
        self._write_date(date, "start")

    @property
    def endDate(self) -> datetime:
        """End date of the time period for which the dataset is valid."""
        return self._parse_date(self._endDate)

    @endDate.setter
    def endDate(self, date: datetime) -> None:
        self._write_date(date, "end")

    def _parse_date(
        self,
        date: str,
        default_month: int = 1,
        default_day: int = 1,
    ) -> datetime:
        if len(date) == 10:
            return datetime(
                int(date[:4]),
                int(date[5:7]),
                int(date[8:]),
            )
        if len(date) == 7:
            return datetime(int(date[:4]), int(date[5:]), default_day)
        return datetime(int(date), default_month, default_day)

    def _write_date(self, date: datetime, prefix: str) -> None:
        month = "0" * (date.month < 10) + str(date.month)
        day = "0" * (date.day < 10) + str(date.day)
        setattr(self, f"_{prefix}Date", f"{date.year}-{month}-{day}")

    def _init(self):
        # 1. Check for fooDate is present, because _init is called multiple times
        # 2. Get Value from either fooYearMonth or fooYear
        # 3. Write the value to fooDate and delete the other 2
        if len(self._startDate) > 0:
            return

        defaultMonth = 1
        defaultDay = 1
        dateElements = []
        for prefix in ["start", "end"]:  # Must be in this order
            yearMonth = getattr(self, f"_{prefix}YearMonth")
            year = getattr(self, f"_{prefix}Year")

            month = defaultMonth
            day = defaultDay
            # fooYearMonth is present
            if len(yearMonth) != 0:
                yearInt = int(yearMonth[:4])
                month = int(yearMonth[5:])
            # fooYear is present
            elif len(year) != 0:
                yearInt = int(year)

            dateElements.append(
                etree.SubElement(self, f"{{{dict(self.nsmap)[None]}}}{prefix}Date")
            )
            dateElements[-1].text = f"{yearInt}-0{month}-0{day}"
            for elementName in [f"{prefix}YearMonth", f"{prefix}Year"]:
                element = get_element(self, elementName)
                if element is not None:
                    self.remove(element)


class Representativeness(etree.ElementBase):
    """Contains information about the fraction of the relevant market supplied by the
    product/service described in the dataset. Information about market share,
    production volume (in the ecoinvent quality network: also consumption volume in
    the market area) and information about how data have been sampled."""

    percent = create_attribute_v1("percent", float)
    """float: Indicates the share in market supply in the geographical area indicated
    of the product/service at issue. If data representative for a process operated
    in one country is used for another country's process, the entry should be '0'.
    The representativity for the original country is reported under
    'extrapolations'."""

    productionVolume = create_attribute_v1("productionVolume", str)
    """str: Indicates the market area consumption volume (NOT necessarily identical with
    the production volume) in the geographical area indicated of the product/service
    at issue. The market volume should be given in absolute terms per year and in
    common units. It is related to the time period specified elsewhere.
    """

    samplingProcedure = create_attribute_v1("samplingProcedure", str)
    """str: Indicates the sampling procedure applied for quantifying the exchanges. It
    should be reported whether the sampling procedure for particular elementary
    and intermediate product flows differ from the general procedure. Possible
    problems in combining different sampling procedures should be mentioned."""

    extrapolations = create_attribute_v1("extrapolations", str)
    """str: Describes extrapolations of data from another time period, another
    geographical area or another technology and the way these extrapolations
    have been carried out. It should be reported whether different extrapolations
    have been done on the level of individual exchanges. If data representative for
    a process operated in one country is used for another country's process, its
    original representativity can be indicated here. Changes in mean values
    due to extrapolations may also be reported here."""

    uncertaintyAdjustments = create_attribute_v1("uncertaintyAdjustments", str)
    """str: For datasets where the additional uncertainty from lacking
    representativeness has been included in the quantified uncertainty values
    ('minValue' and 'maxValue'), thus raising the value in 'percent' of the dataset to
    100%, this field also reports the original representativeness, the additional
    uncertainty and the procedure by which it was assessed or calculated."""


class Source(etree.ElementBase):
    """Contains information about author(s), title, kind of publication, place of
    publication, name of editors (if any), etc.."""

    SOURCE_TYPE_MAP: Dict[int, str] = {
        0: "Undefined (default)",
        1: "Article",
        2: "Chapters in anthology",
        3: "Seperate publication",
        4: "Measurement on site",
        5: "Oral communication",
        6: "Personal written communication",
        7: "Questionnaries",
    }

    number = create_attribute_v1("number", int)
    """int: ID number to identify the source within one dataset."""

    sourceType = create_attribute_v1("sourceType", int)
    """int: Indicates the kind of source. The codes are: 0=Undefined (default).
    1=Article. 2=Chapters in anthology. 3=Seperate publication.
    4=Measurement on site. 5=Oral communication. 6=Personal written communication.
    7=Questionnaries."""

    firstAuthor = create_attribute_v1("firstAuthor", str)
    """str: Indicates the first author by surname and abbreviated name
    (e.g., Einstein A.). In case of measurement on site, oral communication,
    personal written communication and questionnaries ('sourceType'=4, 5, 6, 7)
    the name of the communicating person is mentioned here. Identifies the
    source together with 'title' and 'year'."""

    additionalAuthors = create_attribute_v1("additionalAuthors", str)
    """str: List of additional authors (surname and abbreviated name, e.g. Newton I.),
    separated by commas. 'Et al.' may be used, if more than five additonal authors
    contributed to the cited publication."""

    year = create_attribute_v1("year", int)
    """int: Indicates the year of publication and communication, respectively.
    Identifies the source together with 'firstAuthor' and 'title'."""

    title = create_attribute_v1("title", str)
    """str: Measurement on site: write "Measurement documentation of company XY".
    Oral communication: write "Oral communication, company XY". Personal written
    communication: write: "personal written communication, Mr./Mrs. XY, company Z".
    Questionnaires: write "Questionnaire, filled in by Mr./Mrs. XY, company Z".
    Identifies the source together with 'firstAuthor' and 'year'."""

    pageNumbers = create_attribute_v1("pageNumbers", str)
    """str: If an article or a chapter in an anthology, list the relevant page numbers.
    In case of separate publications the total number of pages may be entered."""

    nameOfEditors = create_attribute_v1("nameOfEditors", str)
    """str: Contains the names of the editors (if any)."""

    titleOfAnthology = create_attribute_v1("titleOfAnthology", str)
    """str: If the publication is a chapter in an anthology, the title of the anthology
    is reported here. For the reports of the ecoinvent quality network 'Final report
    ecoinvent 2000' is written here."""

    placeOfPublications = create_attribute_v1("placeOfPublications", str)
    """str: Indicates the place(s) of publication. In case of measurements on site, oral
    communication, personal written communication or questionnaires, it is the
    location of the company which provided the information. If available via the
    web add the web-address. For the ECOINVENT final reports 'EMPA Dübendorf' is
    written."""

    publisher = create_attribute_v1("publisher", str)
    """str: Lists the name of the publisher (if any). In case of the ecoinvent quality
    network it is the 'Swiss Centre for Life Cycle Inventories'."""

    journal = create_attribute_v1("journal", str)
    """str: Indicates the name of the journal an article is published in."""

    volumeNo = create_attribute_v1("volumeNo", int)
    """int: Indicates the volume of the journal an article is published in."""

    issueNo = create_attribute_v1("issueNo", str)
    """str: Indicates the issue number of the journal an article is published in."""

    text = create_attribute_v1("text", str)
    """str: Free text for additional description of the source. It may contain a
    brief summary of the publication and the kind of medium used (e.g. CD-ROM,
    hard copy)"""

    @property
    def sourceTypeStr(self) -> str:
        """String representation for sourceType. See sourceType for explanations.
        0=Undefined (default). 1=Article. 2=Chapters in anthology.
        3=Seperate publication. 4=Measurement on site. 5=Oral communication.
        6=Personal written communication. 7=Questionnaries."""
        return Source.SOURCE_TYPE_MAP[self.sourceType]


class Validation(etree.ElementBase):
    """Contains information about who carried out the critical review and about
    the main results and conclusions of the revie and the recommendations made."""

    proofReadingDetails = create_attribute_v1("proofReadingDetails", str)
    """str: Contains the comment of the reviewer of the dataset. For the ecoinvent
    quality network the review text should cover the following items:
    1. completeness and transparency of the documentation, 2. conformity with
    the ecoinvent quality guidelines, 3. plausibility of the data (unit process
    elementary and intermediate product flows), 4. completeness regarding
    elementary and intermediate product flows, 5. mathematical correctness.
    The review is limited to sample audits (not covering each and every figure).
    """

    proofReadingValidator = create_attribute_v1("proofReadingValidator", int)
    """int: Indicates the person who carried out the review. ID number must correspond
    to an ID number of a person listed in the respective dataset."""

    otherDetails = create_attribute_v1("otherDetails", str)
    """str: Contains further information from the review process, especially comments
    received from third parties once the dataset has been published."""


class DataEntryBy(etree.ElementBase):
    """Contains information about the person that entered data in the database or
    transformed data into the format of the ecoinvent (or any other) quality network.
    """

    person = create_attribute_v1("person", int)
    """int: ID number for the person that prepared the dataset and enters the dataset
    into the database. It must correspond to an ID number of a person listed in
    the respective dataset."""

    qualityNetwork = create_attribute_v1("qualityNetwork", int)
    """int: Indicates a project team that works on the database. The information is
    used, e.g., for restricting the accessibility of dataset information to one
    particular quality network. The code used is: 1=ecoinvent"""


class DataGeneratorAndPublication(etree.ElementBase):
    """Contains information about who compiled for and entered data into the
    database. Furthermore contains information about kind of publication underlying
    the dataset and the accessibility of the dataset."""

    DATA_PUBLISHED_IN_MAP: Dict[int, str] = {
        0: "Data as such notpublished (default)",
        1: "The data of some unit processes or subsystems are published",
        2: "Data has been published entirely in 'referenceToPublishedSource'",
    }

    ACCESS_RESTRICTED_TO_MAP: Dict[int, str] = {
        0: "Public",
        1: "ETH Domain",
        2: "ecoinvent 2000",
        3: "Institute",
    }

    person = create_attribute_v1("person", int)
    """int: ID number for the person that generated the dataset. It must correspond to
    an ID number of a person listed in the respective dataset."""

    dataPublishedIn = create_attribute_v1("dataPublishedIn", int)
    """int: Indicates whether the dataset has been published (not, partly, entirely).
    The codes are: 0=Data as such not published (default). 1=The data of some unit
    processes or subsystems are published. 2=Data has been published entirely in
    'referenceToPublishedSource'. Within the ecoinvent quality network all datasets
    are published in the series of ecoinvent reports."""

    referenceToPublishedSource = create_attribute_v1("referenceToPublishedSource", int)
    """int: ID number for the report in which the dataset is documented. It must
    correspond to an ID number of a source listed in the respective dataset."""

    copyright = create_attribute_v1("copyright", bool)
    """bool: Indicates whether or not a copyright exists. '1' (Yes) or '0' (No)
    should be entered correspondingly."""

    accessRestrictedTo = create_attribute_v1("accessRestrictedTo", int)
    """int: Indicates possible access restrictions for the dataset. The codes
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

    companyCode = create_attribute_v1("companyCode", str)
    """str: 7 letter code with which organisations/institutes that co-operate within one
    of the database quality networks (see also 'qualityNetwork') are characterised
    and identified. 'countryCode' is required additionally. Only required and
    allowed if access to the dataset is restricted to a particular institute within
    the ecoinvent quality network.

    Here are the codes used in ecoinvent release 2.2:

        {'ART', 'B+H', 'BAUCHEM', 'CARBOTE', 'DOKA', 'ECN', 'EMPA', 'EMPA-SG', 'ENERS',
        'EPFL', 'ESU', 'ETH S+U', 'ETH-UNS', 'HEIG-VD', 'INFRAS', 'LCS', 'OEKOSCI',
        'PRIVAT', 'PSI', 'SBB', 'SCHLEIS', 'U+E', 'UU'}

    The length 7 restriction is bizarre; just truncate and move on with your life.

    """

    countryCode = create_attribute_v1("countryCode", str)
    """str: 2 letter ISO-country codes are used to indicate the country where
    organisations/institutes are located which co-operate within one of the database
    quality networks (see also 'qualityNetwork'). Only required and allowed if
    access to the dataset is restricted to a particular institute within the
    ecoinvent quality network."""

    pageNumbers = create_attribute_v1("pageNumbers", str)
    """str: Indicates the page numbers in the publication where the table with the unit
    process raw data, and the characterisation, damage or weighting factors of the
    impact category, respectively are documented."""

    @property
    def dataPublishedInStr(self) -> str:
        """String representation for dataPublishedIn. See dataPublishedIn for
        explanations. 0=Data as such not published (default). 1=The data of some unit
        processes or subsystems are published. 2=Data has been published entirely in
        'referenceToPublishedSource'"""
        return DataGeneratorAndPublication.DATA_PUBLISHED_IN_MAP[self.dataPublishedIn]

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
        return DataGeneratorAndPublication.ACCESS_RESTRICTED_TO_MAP[
            self.accessRestrictedTo
        ]


class Person(etree.ElementBase):
    """Used for the identification of members of the organisation institute co-operating
    within a quality network (e.g., ecoinvent) referred to in the areas Validation,
    dataEntryBy and dataGeneratorAndPublication."""

    number = create_attribute_v1("number", int)
    """int: ID number is attributed to each person of an organisation/institute
    co-operating in a quality network such as ecoinvent. It is used to identify
    persons cited within one dataset."""

    name = create_attribute_v1("name", str)
    """str: Name and surname of the person working in an organisation/institute which is
    a member of the quality network. Identifies the person together with
    'address' (#5803)."""

    address = create_attribute_v1("address", str)
    """str: Complete address, including street, po-box (if applicable), zip-code,
    city, state (if applicable), country. Identifies the person together with
    'name' (#5802)."""

    telephone = create_attribute_v1("telephone", str)
    """str: Phone number including country and regional codes."""

    telefax = create_attribute_v1("telefax", str)
    """str: Fax number including country and regional codes."""

    email = create_attribute_v1("email", str)
    """str: Complete email address."""

    companyCode = create_attribute_v1("companyCode", str)
    """str: 7 letter company code of the organisation/institute co-operating in a
    quality network. Identifies the co-operation partner together with the
    countryCode (#5808)."""

    countryCode = create_attribute_v1("countryCode", str)
    """str: 2 letter ISO-country code of the organisation/institute co-operating
    in a quality network. Identifying the co-operation partner together with
    the companyCode (#5807)."""
