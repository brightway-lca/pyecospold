# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [4.0.0] - 2024-08-09

### Changed

- Include `pycasreg` in source repo to avoid bumping version dominoes
- Include `lxmlh` in source repo to avoid bumping version dominoes

## [3.6.2] - 2024-06-21

### Fixed

- Fix packaging dynamic version

## [3.6.1] - 2024-06-08

### Fixed

- incorrect imports in `config.py`

## [3.6.0] - 2024-05-30

### Changed

- [#49 - Refactor date handling](https://github.com/brightway-lca/pyecospold/pull/49)

### Fixed

- pin to old version of `lxmlh`

## [3.5.5] - 2024-04-03

### Fixed

- documentation

## [3.5.4] - 2024-03-28

### Fixed

- packaging

## [3.5.2] - 2024-03-27

### Added

- readthedocs

## [3.5.1] - 2024-03-09

### Fixed

- typo ecopsold to ecospold

### Removed

- 3.1 size constraint on percent

## [3.5.0] - 2024-03-08

### Changed

- EcoSpold1.ModellingAndValidation.Source to Sources
- EcoSpold1.DataSetInformation.version from float to str
- EcoSpold1.DataSetInformation.internalVersion from float to str
- EcoSpold1.TimePeriod.startDate from datetime to date
- EcoSpold1.TimePeriod.endDate from datetime to date


## [3.4.3] - 2024-02-03

### Added

- EcoSpold.geography
- EcoSpold.geographyShortName
- EcoSpold.activity
- EcoSpold.activityName
- EcoSpold.elementary_exchange()
- EcoSpold.elementary_exchange_compartment()
- EcoSpold.elementary_exchange_sub_compartment()
- EcoSpold.elementary_exchange_name()
- EcoSpold.elementary_exchange_unit_name()
- EcoSpold.intermediate_exchange()
- EcoSpold.intermediate_exchange_name()
- EcoSpold.intermediate_exchange_unit_name()

## [3.4.2] - 2024-02-02

### Added

- IntermediateExchange.groupType
- ElementaryExchange.groupType

## [3.4.1] - 2023-11-23

### Changed

- Bump deps to support python 3.12

## [3.3.2] - 2023-09-26

### Fixed
- Version mismatch

## [3.3.0] - 2023-09-26

### Added
- Validating directories
- Validating ZIP files
- Parsing ZIP files

## [3.2.1] - 2023-09-11

### Modified
- README.md: usage

## [3.2.0] - 2023-04-24

### Added
- Generic group and groupStr attributes for ElementaryExchange and IntermediateExchange

## [3.1.0] - 2023-04-24

### Fixed
- Missing inputGroup and outGroup in IntermediateExchange

## [3.0.0] - 2023-03-27

### Modified
- Bumped lxmlh version from 0.1.0 to 1.1.0

## [2.4.0] - 2023-03-26

### Modified
- Switched to using lxmlh.

## [2.3.0] - 2023-03-26

### Modified
- Switched to using pycasreg.

## [2.2.0] - 2023-03-06

## Added
- Generic attribute for some choice attributes.

## [2.1.0] - 2023-03-06

### Fixed
- Missing XSD in packaging.

## [2.0.0] - 2023-03-04

### Added
- Parsing EcoSpold02 XML files.
- Validating files.
- Parsing whole directories.

### Modified
- Filling in static default values provided in config.ini and dynamic ones.

## [1.0.0] - 2023-01-10

### Added
- Setting attributes for custom classes.

## [0.1.0] - 2023-01-05

### Added
- Parsing EcoSpold01Dataset XML files.
- Saving Python objects to XML files.
- Configuring default values for non-existing attributes.
