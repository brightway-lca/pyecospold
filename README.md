# pyecospold

[![PyPI](https://img.shields.io/pypi/v/pyecospold.svg)][pypi status]
[![Status](https://img.shields.io/pypi/status/pyecospold.svg)][pypi status]
[![Python Version](https://img.shields.io/pypi/pyversions/pyecospold)][pypi status]
[![License](https://img.shields.io/pypi/l/pyecospold)][license]

[![Read the documentation at https://pyecospold.readthedocs.io/](https://img.shields.io/readthedocs/pyecospold/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Tests](https://github.com/sami-m-g/pyecospold/actions/workflows/python-test.yml/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/sami-m-g/pyecospold/branch/main/graph/badge.svg?token=ZVWBCITI4A)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi status]: https://pypi.org/project/pyecospold/
[read the docs]: https://pyecospold.readthedocs.io/
[tests]: https://github.com/sami-m-g/pyecospold/actions?workflow=Tests
[codecov]: https://codecov.io/gh/sami-m-g/pyecospold
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

## Installation

You can install _pyecospold_ via [pip] from [PyPI]:

```console
$ pip install pyecospold
```

## ecospold1 Schema Updates

### 1.1

This library includes a new version of the schema definitions for ecospold1. Version 1.1 includes the following changes:

* Changed the length restriction on `referenceFunction.name` to 255
* Changed the length restriction on `referenceFunction.synonym` to 255
* Changed the length restriction on `category` and `subCategory` to 255
* Changed the length restriction on `representativeness.productionVolume` to 32.000
* Made `telephone` optional

These changes were based on how this schema was being used by LCA software.

### 1.2

Corrected the handling of CAS numbers based on [the official documentation](https://www.cas.org/support/documentation/chemical-substances/checkdig):

* A fixed size isn't required, zero-padding is optional and in any case is not used consistently by LCA software
* Maximum length is 12, not 11
* The first element has a minimum size of 2 digits, not 1

## Usage

```python
from pyecospold import parse_file, save_file, Defaults

# Override defaults if needed, else skip. Defaults are already set.
Defaults.config("config.ini")  # Replace with your own config file

# Parse the required XML file to EcoSpold class.
ecoSpold = parse_file("data/v1/v1_1.xml")  # Replace with your own XML file
ecoSpold
>> <Element {http://www.EcoInvent.org/EcoSpold01}ecoSpold at 0x24a558b6020>

# Change whatever attributes you need changing.
referenceFunction = ecoSpold.dataset.metaInformation.processInformation.referenceFunction
referenceFunction.amount = 2.0
referenceFunction.amount
>> 2.0

# Save final EcoSpold class as an XML file, make sure root directory exists.
save_file(ecoSpold, "out/00001_new.xml")  # Replace with your own path
```

# Config file

```ini
[parameters]
SCHEMA_V1_FILE=path/to/schemas/v1/EcoSpold01Dataset.xsd
SCHEMA_V2_FILE=path/to/schemas/v2/EcoSpold02.xsd

[Allocation]
allocationMethod=-1

[DataEntryBy]
qualityNetwork=1

[Dataset]
validCompanyCodes=CompanyCodes.xml
validRegionalCodes=RegionalCodes.xml
validCategories=Categories.xml
validUnits=Units.xml

[DataSetInformation]
impactAssessmentResult=false
internalVersion=1.0
version=1.0

[Exchange]
uncertaintyType=1

[ReferenceFunction]
infrastructureProcess=true
```

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide][Contributor Guide].

## License

Distributed under the terms of the [BSD license][License],
_pyecospold_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue][Issue Tracker] along with a detailed description.


## Credits


[License]: https://github.com/sami-m-g/pyecospold/blob/main/LICENSE
[Contributor Guide]: https://github.com/sami-m-g/pyecospold/blob/main/CONTRIBUTING.md
[Issue Tracker]: https://github.com/sami-m-g/pyecospold/issues
