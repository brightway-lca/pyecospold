"""Custom EcoSpold Python classes for v1 of EcoSpold schema."""
from typing import Dict, List

from lxml import etree

from .helpers import DataHelper


class EcoSpold(etree.ElementBase):
    """The data (exchange) format of the ecoinvent context."""

    @property
    def activityDataset(self) -> "ActivityDataset":
        """Contains information about one individual activity. Information is divided
        into metaInformation and flowData."""
        return DataHelper.get_element(self, "activityDataset")

    @property
    def childActivityDataset(self) -> "ActivityDataset":
        """Contains information about one individual activity. Information is divided
        into metaInformation and flowData."""
        return DataHelper.get_element(self, "childActivityDataset")


class ActivityDataset(etree.ElementBase):
    """Contains information about one individual activity. Information is divided into
    metaInformation and flowData."""

    @property
    def activityDescription(self) -> "ActivityDescription":
        """Contains content-related metainformation for the activity."""
        return DataHelper.get_element(self, "activityDescription")

    @property
    def flowData(self) -> "FlowData":
        """Contains information about inputs and outputs of the given activity
        (exchanges with environment as well as intermediate exchanges) as well
        as their properties, allocations, transfer coefficients, uncertainties
        and parameters for the use in mathematical formulas."""
        return DataHelper.get_element(self, "flowData")

    @property
    def modellingAndValidation(self) -> "ModellingAndValidation":
        """Contains metainformation about how unit processes are modelled and about the
        review/validation of the dataset."""
        return DataHelper.get_element(self, "modellingAndValidation")

    @property
    def administrativeInformation(self) -> "AdministrativeInformation":
        """Contains the administrative information about the dataset at issue: The
        persons that compiled and entered the dataset in the database and about kind
        of publication and the accessibility of the dataset, timestamp, version and
        internalVersion number as well as language and localLanguage code."""
        return DataHelper.get_element(self, "administrativeInformation")


class ActivityDescription(etree.ElementBase):
    """Contains content-related metainformation for the activity."""

    @property
    def activity(self) -> List["Activity"]:
        """Contains the identifying information of an activity dataset including name
        and classification."""
        return DataHelper.get_element_list(self, "activity")

    @property
    def classification(self) -> List["Classification"]:
        """Contains classification pairs to specify the activity.)"""
        return DataHelper.get_element_list(self, "classification")

    @property
    def geography(self) -> List["Geography"]:
        """Describes the geographic location for which the dataset is supposed to be
        valid."""
        return DataHelper.get_element_list(self, "geography")

    @property
    def technology(self) -> List["Technology"]:
        """Describes the technological properties of the unit process."""
        return DataHelper.get_element_list(self, "technology")

    @property
    def timePeriod(self) -> List["TimePeriod"]:
        """Characterises the temporal properties of the unit activity
        (or system terminated) at issue."""
        return DataHelper.get_element_list(self, "timePeriod")

    @property
    def macroEconomicScenario(self) -> List["MacroEconomicScenario"]:
        """References the macro-economic scenario used in this dataset."""
        return DataHelper.get_element_list(self, "macroEconomicScenario")


class FlowData(etree.ElementBase):
    """Contains information about inputs and outputs of the given activity (exchanges
    with environment as well as intermediate exchanges) as well as their properties,
    allocations, transfer coefficients, uncertainties and parameters for the use in
    mathematical formulas."""

    @property
    def intermediateExchanges(self) -> List["IntermediateExchange"]:
        """Comprises intermediate product and waste inputs and outputs for the
        activity."""
        return DataHelper.get_element_list(self, "intermediateExchange")

    @property
    def elementaryExchanges(self) -> List["ElementaryExchange"]:
        """Comprises elementary inputs and outputs (exchanges with the environment)
        for the activity."""
        return DataHelper.get_element_list(self, "elementaryExchange")

    @property
    def parameters(self) -> List["Parameter"]:
        """Comprises all parameters of the activity."""
        return DataHelper.get_element_list(self, "parameter")

    @property
    def impactIndicators(self) -> List["ImpactIndicator"]:
        """Calculated impact indicators"""
        return DataHelper.get_element_list(self, "impactIndicator")


class ModellingAndValidation(etree.ElementBase):
    """Contains metainformation about how unit processes are modelled and about the
    review/validation of the dataset."""

    @property
    def representativeness(self) -> "Representativeness":
        """Contains information about the representativeness of the unit process data
        (meta information and flow data)."""
        return DataHelper.get_element(self, "representativeness")

    @property
    def review(self) -> "Review":
        """Contains information about the reviewers' comments on the dataset content."""
        return DataHelper.get_element(self, "review")


class AdministrativeInformation(etree.ElementBase):
    """Contains the administrative information about the dataset at issue: The
    persons that compiled and entered the dataset in the database and about kind
    of publication and the accessibility of the dataset, timestamp, version and
    internalVersion number as well as language and localLanguage code."""

    @property
    def dataEntryBy(self) -> "DataEntryBy":
        """Contains information about the author of the dataset, i.e. the person
        that entered the dataset into the database format and thereby is the
        person responsible for the data."""
        return DataHelper.get_element(self, "dataEntryBy")

    @property
    def dataGeneratorAndPublication(self) -> "DataGeneratorAndPublication":
        """Contains information about who collected, compiled or published
        the original data. This may or may not be the same person as under
        'DataEntryBy'. Furthermore contains information about kind of
        publication underlying the dataset and the accessibility of the dataset."""
        return DataHelper.get_element(self, "dataGeneratorAndPublication")

    @property
    def fileAttributes(self) -> "FileAttributes":
        """This constraint ensures that each xml:lang attribute is only used once
        in this context. I.e. there must be only one translation of the element."""
        return DataHelper.get_element(self, "fileAttributes")


class Activity(etree.ElementBase):
    """Contains the identifying information of an activity dataset including name and
    classification."""

    INHERITANCE_DEPTH_MAP: Dict[int, str] = {
        0: "not a child",
        1: "a geography child",
        2: "a temporal child",
        3: "a macro-economic scenario child",
    }

    TYPE_MAP: Dict[int, str] = {
        1: "Unit process",
        2: "System terminated",
    }

    SPECIAL_ACTIVITY_TYPE_MAP: Dict[int, str] = {
        0: "ordinary transforming activity (default)",
        1: "market activity",
        2: "IO activity",
        3: "Residual activity",
        4: "production mix",
        5: "import activity",
        6: "supply mix",
        7: "export activity",
        8: "re-export activity",
        9: "correction activity",
        10: "market group",
    }

    ENERGY_VALUES_MAP: Dict[int, str] = {
        0: "Undefined (default)",
        1: "Net values",
        2: "Gross values",
    }

    activityNames = DataHelper.create_attribute_list_v2("activityName", str)
    """List[str]: A name for the activity that is represented by this dataset."""

    synonyms = DataHelper.create_attribute_list_v2("synonym", str)
    """List[str]: List of synonyms for the name. Contrary to normal multi language
    strings, synonyms may contain more than one element with the same xml:lang
    attribute value. 0..n entries are allowed with a max. length of 80 each."""

    includedActivitiesStarts = DataHelper.create_attribute_list_v2(
        "includedActivitiesStart", str
    )
    """List[str]: Describes the starting point of the activity. For "system
    terminated" the starting point is always "From cradle, i.e. including all
    upstream activities". For unit processes, the starting point may be described
    in terms of the nature of the inputs, e.g. "From reception of
    [e.g. raw material X]..." or "Service starting with the input of
    [e.g. labour and energy]."""

    includedActivitiesEnds = DataHelper.create_attribute_list_v2(
        "includedActivitiesEnd", str
    )
    """List[str]: Describes the included activities to the extent that this is not
    self-explanatory from the activity name, as well as activities or inputs that are
    intentionally excluded, e.g. if the activity “application of pesticides” as a
    service excludes the pesticide, in order to be applicable for many different
    active ingredients. The description ends by mentioning the last activity and/or
    point of delivery, e.g. “until and including loading of the product on lorries”."""

    tags = DataHelper.create_attribute_list_v2("tag", str)
    """List[str]: The tag field allows an open list of keywords which describes the
    activity and can be used for filtering, grouping and searching. The validTags file
    reference provides a list of predefined tags, but the semantic validation procedure
    should only display an information (not an error) if a tag entry cannot be found in
    the validTags master file."""

    id = DataHelper.create_attribute_v2("id", str)
    """str: Unique identifier for this activity. The datat type UUID is a 36 characters
    string with hexadecimal characters and ensures a world-wide unique identifier.
    A UUID for a new item must be supplied by external software. There are several UUID
    generators on the web and implementations in most programming languages."""

    activityNameId = DataHelper.create_attribute_v2("activityNameId", str)
    """str: Reference to the activity name master data entry for this activity."""

    activityNameContextId = DataHelper.create_attribute_v2("activityNameContextId", str)
    """str: Reference to the context of the activity name. If this attribute is omitted
    the context of the dataset itself will be used instead."""

    parentActivityId = DataHelper.create_attribute_v2("parentActivityId", str)
    """str: he parentActivityId is a UUID to the parent activity dataset. When this
    field is filled with a UUID, all the field content from the parent activity
    dataset is taken over by the child activity dataset (the activity that calls
    the parent via the UUID). Child activity is derived (inherited) from its parent
    activity and only the content changes in comparison to its parent are stored in
    the child process. Child activity datasets cannot be validated using the EcoSpold02
    schema, since most of the required fields will not be filled. Please refer to the
    additional documentation regarding inheritance of datasets in the ecoinvent database
    for further details. There are 5 ways to fill a field in a child activity dataset
    ("http://www.EcoInvent.org/EcoSpold02Child"): Leave a field blank: In this case,
    the value from the parent activity dataset applies. 2) Fill in content: In this
    case, the filled in value applies, and the value from the parent activity dataset is
    ignored. 3) In a string field, fill in content including the text {{PARENTTEXT}} in
    which case the field content from the parent activity dataset is included at this
    place in the filled in text in the child dataset. 4) In a field with type
    TTextAndImage, both {{PARENTTEXT}} and {{text_variables}} are supported; the latter
    allows to define text variables in the parent dataset and use them in the text as
    {{variablename}}. If a parent textfield includes a variable, this variable may be
    redefined by the child activity dataset while keeping the rest of the parent text
    intact. This allows easy changes of text parts in child processes. 5) In an amount
    field with corresponding mathematical relation fields, fill in content in the
    mathematicalRelation field including the reserved variable PARENTVALUE, e.g. the
    formula PARENTVALUE*0.5 results in halfing the value of the original amount field.
    """

    parentActivityContextId = DataHelper.create_attribute_v2(
        "parentActivityContextId", str
    )
    """str: Reference to the context of the parent activity. If this attribute is
    omitted the context of the dataset itself will be used instead."""

    inheritanceDepth = DataHelper.create_attribute_v2("inheritanceDepth", int)
    """int: The inheritance depth expresses the maximum number of parent datasets for
    the current dataset. The following values are used in the ecoinvent context:
    0 = not a child, 1 = a geography child, 2 = a temporal child, 3 = a macro-economic
    scenario child."""

    type = DataHelper.create_attribute_v2("type", int)
    """int: Indicates the kind of data (1 = Unit process; 2 = System terminated) that
    is represented by this dataset. Data are always entered by the data providers as
    Unit process. The database-generated, attributional and consequential datasets are
    available both at the unit process level and as aggregated (terminated) system
    dataset (i.e. the life cycle inventory results) containing the aggregated elementary
    exchanges and impacts of the product system related to one specific product from the
    unit process. The terminated product systems include all upstream activity datasets,
    as linked by the intermediate exchanges, and therefore do not themselves have any
    intermediate exchanges, only environmental exchanges and accumulated impact
    assessment results."""

    specialActivityType = DataHelper.create_attribute_v2("specialActivityType", int)
    """int: The special activity types are: 0 = “ordinary” transforming activities.
    Transforming activities are human activities that transform inputs, so that the
    output of the activity is different from the inputs, e.g. a hard coal mine that
    transforms hard coal in ground to the marketable product hard coal. Transforming
    activities are here understood in the widest possible sense, including extraction,
    production, transport, consumption and waste treatment activities, i.e. any human
    activity where the intermediate output is different from the intermediate input.
    The concept “transforming activities” is introduced here simply to distinguish –
    in the further modelling and linking of activities – these “ordinary” activities
    from the market activities, production and supply mixes, import and export
    activities, and correction datasets. 1 = market activity. Market activities do not
    transform their inputs, but simply transfer the intermediate output from a
    transforming activity to the transforming activities that consume this intermediate
    output as an input, e.g. from hard coal at the supplier to hard coal at the
    consumer. Market activities typically mix similar intermediate outputs from
    different transforming activities. Market activities therefore supply consumption
    mixes of the intermediate outputs. 10 = market group. Market groups are to markets
    what markets are to transforming activities. In the undefined system model a market
    group only contains a reference product. The linking algorithm will add supplying
    markets as inputs which are contained in the location of the market group and have
    the same reference product. 2 = IO activity. An IO activity represents an activity
    dataset from a national supply-use table, i.e. typically the supply and use of one
    specific industry. 3 = Residual activity. A residual activity is the resulting
    activity when subtracting all available unit processes within an activity class from
    the supply-use data (IO activity) of the same activity class, for the same year and
    geo-graphical area. 4 = production mix. A production mix represents the
    production-volume-weighted average of the suppliers of a specific product within a
    geographical area.5 = import activity. An import activity represents the import of a
    specified product to a specified geographical area, solely for use in national
    balancing (not contributing to any auto-generated consumption mixes). Imports to
    administratively constrained markets and from partly isolated markets are modelled
    as ordinary transforming activities in order to be included in the relevant market
    activities (consumption mixes).6 = supply mix. A supply mix is a production mix with
    the addition of the import of a specified product to a specified geographical area.
    7 = export activity. An export activity represents the export volume of a national
    production mix that has the national area as its geographical location and does not
    contribute to any auto-generated consumption mixes. To give the correct value of the
    export, the same activities and data that are included with the market activities
    are added directly to the export activity. This includes transport activities,
    production losses, wholesaler and retailer activities, and product taxes and
    subsidies. 8 = re-export activity. A re-export activity represents the re-export
    volume of a geographical area and does not contribute to any auto-generated
    consumption mixes. 9 = correction activity. A correction activity is an activity
    that is added twice to a product system, one with a positive and once with a
    negative flow, in order to move one or more exchanges from one part of the system
    to another, e.g. to correct for downstream effects of an upstream activity, or to
    correct a bias in the mass-balance introduced by an allocation. More details on
    this is provided in the Chapters on "Downstream changes caused by differences in
    product quality" and "Allocation corrections" in the ecoinvent Data Quality
    Guidelines."""

    energyValues = DataHelper.create_attribute_v2("energyValues", int)
    """int: Indicates the way energy values are applied in the dataset. The codes
    are: 0=Undefined (default). 1=Net (lower) heating value. 2=Gross (higher)
    heating value. This data field is by default set to 0."""

    masterAllocationPropertyId = DataHelper.create_attribute_v2(
        "masterAllocationPropertyId", str
    )
    """str: References the default Allocation Property (via UUID) for all exchanges
    of this dataset. The Allocation Property can be overwritten for each exchange
    (see field 1150 specificAllocationPropertyId). The allocation factor for a
    specific output is then the declared TProperty value for this output multiplied
    by the amount of the output divided by the sum of the all such multiplied
    TProperty values for all outputs."""

    masterAllocationPropertyIdOverwrittenByChild = DataHelper.create_attribute_v2(
        "masterAllocationPropertyIdOverwrittenByChild", bool
    )
    """bool: If a reference to a master data entity must be removed in a child
    dataset it is required to set the corresponding xxxOverwrittenByChild attribute
    to true. Otherwise the removed referenced will be interpreted as "Keep the
    Parent Value"."""

    masterAllocationPropertyContextId = DataHelper.create_attribute_v2(
        "masterAllocationPropertyContextId", str
    )
    """str: Reference to the context of the master allocation property. If this
    attribute is omitted the context of the dataset itself will be used instead.
    """

    datasetIcon = DataHelper.create_attribute_v2("datasetIcon", str)
    """str: The URL of the dataset icon. A dataset icon serves a quick
    identification of the specific dataset, and may also be used for product
    brands and company logos. The icon is not directly part of the dataset, but
    is stored locally or on the ecoinvent web-server, from where it is
    retrievable via the Http protocol."""

    @property
    def allocationComment(self) -> "Comment":
        """Text and image field for further information about the allocation
        procedure and the allocation properties chosen. An eventual coincidence in
        allocation factors when comparing different allocation parameters (like physical
        and economic ones) may be reported here as well.Text and image fields are list
        of text, imageUri and variable elements. The text and imageUri elements can used
        to describe the current section and they can be combined in any order given by
        their index attribute. Text variables are defined by the variable elements,
        which may be used in the text as {{variablename}}. If a parent text field
        includes a variable, this variable may be redefined by the child activity
        dataset while keeping the rest of the parent text intact. This allows easy
        changes of text parts in child processes."""
        return DataHelper.get_element(self, "allocationComment")

    @property
    def generalComment(self) -> "Comment":
        """Text and image field for general information about the dataset. Only comments
        and references of more general nature that cannot be placed in any of the more
        specific comment fields, should be placed here. In general, the information in
        the dataset should be sufficient to judge the appropriateness of a dataset for a
        specific application.Text and image fields are list of text, imageUri and
        variable elements. The text and imageUri elements can used to describe the
        current section and they can be combined in any order given by their index
        attribute. Text variables are defined by the variable elements, which may be
        used in the text as {{variablename}}. If a parent text field includes a
        variable, this variable may be redefined by the child activity dataset while
        keeping the rest of the parent text intact. This allows easy changes of text
        parts in child processes."""
        return DataHelper.get_element(self, "generalComment")

    @property
    def inheritanceDepthStr(self) -> str:
        """String representation for inheritanceDepth. See inheritanceDepth for
        explanations. 0 = not a child, 1 = a geography child, 2 = a temporal child,
        3 = a macro-economic scenario child."""
        return Activity.INHERITANCE_DEPTH_MAP[self.inheritanceDepth]

    @property
    def typeStr(self) -> str:
        """String representation for type. See type for explanations.
        1 = Unit process; 2 = System terminated"""
        return Activity.TYPE_MAP[self.type]

    @property
    def specialActivityTypeStr(self) -> str:
        """String representation for specialActivityType. See specialActivityType
        for explanations. 0 = ordinary transforming activity (default),
        1 = market activity, 2 = IO activity, 3 = Residual activity,
        4 = production mix, 5 = import activity, 6 = supply mix, 7 = export activity,
        8 = re-export activity, 9 = correction activity, 10 = market group"""
        return Activity.SPECIAL_ACTIVITY_TYPE_MAP[self.specialActivityType]

    @property
    def energyValuesStr(self) -> str:
        """String representation for energyValues. See energyValues for explanations.
        0=Undefined (default). 1=Net (lower) heating value. 2=Gross (higher) heating
        value. This data field is by default set to 0."""
        return Activity.ENERGY_VALUES_MAP[self.energyValues]


class Classification(etree.ElementBase):
    """Contains classification pairs to specify the activity.)"""

    classificationId = DataHelper.create_attribute_v2("classificationId", str)
    """str: Reference to the value of a classification system. Must be defined
    in list of valid classifications (see field 5160)."""

    classificationContextId = DataHelper.create_attribute_v2(
        "classificationContextId", str
    )
    """str: Reference to the context of the classification. If this attribute
    is omitted the context of the dataset itself will be used instead."""

    @property
    def classificationSystem(self) -> str:
        """The name of the classification system used, e.g. ISIC Rev. 4.
                This is an optional plaintext value of the referenced classification
        system (field 320)."""
        return DataHelper.get_element_text(self, "classificationSystem")

    @property
    def classificationValue(self) -> str:
        """The class that the activity belongs to within the specified
                classification system. This is an optional plaintext value of
        the referenced classification value (field 320)."""
        return DataHelper.get_element_text(self, "classificationValue")


class Geography(etree.ElementBase):
    """Describes the geographic location for which the dataset is supposed
    to be valid."""

    geographyId = DataHelper.create_attribute_v2("geographyId", str)
    """str: Reference to valid locations file with detailed geography information."""

    geographyContextId = DataHelper.create_attribute_v2("geographyContextId", str)
    """str: Reference to the context of the geography. If this attribute is
    omitted the context of the dataset itself will be used instead."""

    shortNames = DataHelper.create_attribute_list_v2("shortname", str)
    """List[str]: Descriptive shortname of the location referenced by geographyId,
    e.g. the regional codes of EcoSpold version 1."""

    @property
    def comments(self) -> List["Comment"]:
        """Text and image field for further explanations of the geography.
        Especially for area descriptions, the nature of the geographical
        delimitation may be given, especially when this is not an administrative
        area. Justifications for market boundaries may also be provided here.Text
        and image fields are list of text, imageUri and variable elements. The text
        and imageUri elements can used to describe the current section and they can
        be combined in any order given by their index attribute. Text variables are
        defined by the variable elements, which may be used in the text as
        {{variablename}}. If a parent text field includes a variable, this variable
        may be redefined by the child activity dataset while keeping the rest of the
        parent text intact. This allows easy changes of text parts in child
        processes."""
        return DataHelper.get_element_list(self, "comment")


class Technology(etree.ElementBase):
    """Describes the technological properties of the unit process."""

    TECHNOLOGY_LEVEL_MAP: Dict[int, str] = {
        0: "undefined",
        1: "New",
        2: "Modern",
        3: "Current (default)",
        4: "Old",
        5: "Outdated",
    }

    technologyLevel = DataHelper.create_attribute_v2("technologyLevel", int)
    """int: Label that grossly classifies the technology of the described
    activity and can be used in modelling to select processes with a specific
    technological level. The codes used are:0=Undefined. For market activities
    that do not have a technology level.1=New. For a technology assumed to be
    on some aspects technically superior to modern technology, but not yet the
    most commonly installed when investment is based on purely economic
    considerations.2=Modern. For a technology currently used when installing
    new capacity, when investment is based on purely economic considerations
    (most competitive technology). 3=Current (default). For a technology in
    between modern and old.4=Old. For a technology that is currently taken
    out of use, when decommissioning is based on purely economic
    considerations (least competitive technology).5=Outdated. For a technology
    no longer in use.The terms used does not necessarily reflect the age of
    the technologies. A modern technology can be a century old, if it is still
    the most competitive technology, and an old technology can be relatively young,
    if it is one that has quickly become superseded by other more competitive ones.
    The technology level is relative to the year for which the data are valid, as
    given under Time Period. In a time series, the same technology can move between
    different technology levels over time. The same technology can also be given
    different technology levels in different geographical locations, even in the
    same year."""

    @property
    def comments(self) -> List["Comment"]:
        """Text and image field to describe the technology of the activity. The
        text should cover information necessary to identify the properties and
        particularities of the technology(ies) underlying the activity data.
        Describes the technological properties of the unit process. If the activity
        comprises several subactivities, the corresponding technologies should be
        reported as well. Professional nomenclature should be used for the
        description.Text and image fields are list of text, imageUri and variable
        elements. The text and imageUri elements can used to describe the current
        section and they can be combined in any order given by their index
        attribute. Text variables are defined by the variable elements, which may
        be used in the text as {{variablename}}. If a parent text field includes
        a variable, this variable may be redefined by the child activity dataset
        while keeping the rest of the parent text intact. This allows easy changes
        of text parts in child processes."""
        return DataHelper.get_element_list(self, "comment")

    @property
    def technologyLevelStr(self) -> str:
        """String representation for technologyLevel. See technologyLevel for
        explanations. 0 = undefined, 1 = New, 2 = Modern, 3 = Current (default),
        4 = Old, 5 = Outdated"""
        return self.TECHNOLOGY_LEVEL_MAP[self.technologyLevel]


class TimePeriod(etree.ElementBase):
    """Characterises the temporal properties of the unit activity
    (or system terminated) at issue."""


class MacroEconomicScenario(etree.ElementBase):
    """References the macro-economic scenario used in this dataset."""


class IntermediateExchange(etree.ElementBase):
    """Comprises intermediate product and waste inputs and outputs for the activity."""


class ElementaryExchange(etree.ElementBase):
    """Comprises elementary inputs and outputs (exchanges with the environment)
    for the activity."""


class Parameter(etree.ElementBase):
    """Comprises all parameters of the activity."""


class ImpactIndicator(etree.ElementBase):
    """Calculated impact indicators"""


class Representativeness(etree.ElementBase):
    """Contains information about the representativeness of the unit process data
    (meta information and flow data)."""


class Review(etree.ElementBase):
    """Contains information about the reviewers' comments on the dataset content."""


class DataEntryBy(etree.ElementBase):
    """Contains information about the author of the dataset, i.e. the person that
    entered the dataset into the database format and thereby is the person
    responsible for the data."""


class DataGeneratorAndPublication(etree.ElementBase):
    """Contains information about who collected, compiled or published the original
    data. This may or may not be the same person as under 'DataEntryBy'. Furthermore
    contains information about kind of publication underlying the dataset and the
    accessibility of the dataset."""


class FileAttributes(etree.ElementBase):
    """This constraint ensures that each xml:lang attribute is only used once in this
    context. I.e. there must be only one translation of the element."""


class Comment(etree.ElementBase):
    """Text and image field for information."""

    @property
    def texts(self) -> List[str]:
        """Texts."""
        return DataHelper.get_inner_text_list(self, "text")

    @property
    def imageUrls(self) -> List[str]:
        """Image URLs."""
        return DataHelper.get_inner_text_list(self, "imageUrl")
