"""Custom EcoSpold Python classes for v1 of EcoSpold schema."""
from typing import List

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
    def activity(self) -> "Activity":
        """Contains the identifying information of an activity dataset including name
        and classification."""
        return DataHelper.get_element(self, "activity")

    @property
    def classification(self) -> "Classification":
        """Contains classification pairs to specify the activity.)"""
        return DataHelper.get_element(self, "classification")

    @property
    def geography(self) -> "Geography":
        """Describes the geographic location for which the dataset is supposed to be
        valid."""
        return DataHelper.get_element(self, "geography")

    @property
    def technology(self) -> "Technology":
        """Describes the technological properties of the unit process."""
        return DataHelper.get_element(self, "technology")

    @property
    def timePeriod(self) -> "TimePeriod":
        """Characterises the temporal properties of the unit activity
        (or system terminated) at issue."""
        return DataHelper.get_element(self, "timePeriod")

    @property
    def macroEconomicScenario(self) -> "MacroEconomicScenario":
        """References the macro-economic scenario used in this dataset."""
        return DataHelper.get_element(self, "macroEconomicScenario")


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

    allocationComments = DataHelper.create_attribute_list_v2("allocationComment", str)
    """List[str]: Text and image field for further information about the allocation
    procedure and the allocation properties chosen. An eventual coincidence in
    allocation factors when comparing different allocation parameters (like physical
    and economic ones) may be reported here as well.Text and image fields are list of
    text, imageUri and variable elements. The text and imageUri elements can used to
    describe the current section and they can be combined in any order given by their
    index attribute. Text variables are defined by the variable elements, which may be
    used in the text as {{variablename}}. If a parent text field includes a variable,
    this variable may be redefined by the child activity dataset while keeping the rest
    of the parent text intact. This allows easy changes of text parts in child processes
    """

    generalComments = DataHelper.create_attribute_list_v2("generalComment", str)
    """List[str]: Text and image field for general information about the dataset.
    Only comments and references of more general nature that cannot be placed in any of
    the more specific comment fields, should be placed here. In general, the information
    in the dataset should be sufficient to judge the appropriateness of a dataset for a
    specific application.Text and image fields are list of text, imageUri and variable
    elements. The text and imageUri elements can used to describe the current section
    and they can be combined in any order given by their index attribute. Text variables
    are defined by the variable elements, which may be used in the text as
    {{variablename}}. If a parent text field includes a variable, this variable may be
    redefined by the child activity dataset while keeping the rest of the parent text
    intact. This allows easy changes of text parts in child processes."""

    tags = DataHelper.create_attribute_list_v2("tag", str)
    """List[str]: The tag field allows an open list of keywords which describes the
    activity and can be used for filtering, grouping and searching. The validTags file
    reference provides a list of predefined tags, but the semantic validation procedure
    should only display an information (not an error) if a tag entry cannot be found in
    the validTags master file."""


class Classification(etree.ElementBase):
    """Contains classification pairs to specify the activity.)"""


class Geography(etree.ElementBase):
    """Describes the geographic location for which the dataset is supposed
    to be valid."""


class Technology(etree.ElementBase):
    """Describes the technological properties of the unit process."""


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
