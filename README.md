# pyecospold

[![PyPI](https://img.shields.io/pypi/v/pyecospold.svg)][pypi status]
[![Status](https://img.shields.io/pypi/status/pyecospold.svg)][pypi status]
[![Python Version](https://img.shields.io/pypi/pyversions/pyecospold)][pypi status]
[![License](https://img.shields.io/pypi/l/pyecospold)][license]

[![Read the documentation at https://pyecospold.readthedocs.io/](https://img.shields.io/readthedocs/pyecospold/latest.svg?label=Read%20the%20Docs)][read the docs]
[![Tests](https://github.com/brightway-lca/pyecospold/workflows/Tests/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/brightway-lca/pyecospold/branch/main/graph/badge.svg)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi status]: https://pypi.org/project/pyecospold/
[read the docs]: https://pyecospold.readthedocs.io/
[tests]: https://github.com/brightway-lca/pyecospold/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/brightway-lca/pyecospold
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

## Installation

You can install _pyecospold_ via [pip] from [PyPI]:

```console
$ pip install pyecospold
```

## Usage

```python
from pyecospold import parse_file, save_file, Defaults

# Override defaults if needed, else skip. Defaults are already set.
Defaults.config("config.ini")  # Replace with your own config file

# Parse the required XML file to EcoSpold class.
ecoSpold = parse_file("data/examples/00001.xml")  # Replace with your own XML file
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
[defaults]
qualityNetwork="1"
qualityNetwork="1"
uncertaintyType="1"
allocationMethod="-1"
SCHEMA_FILE="data/schema/EcoSpold01Dataset.xsd"
```

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [BSD license license][license],
_pyecospold_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.


## Credits


[license]: https://github.com/brightway-lca/pyecospold/blob/main/LICENSE
[contributor guide]: https://github.com/brightway-lca/pyecospold/blob/main/CONTRIBUTING.md
