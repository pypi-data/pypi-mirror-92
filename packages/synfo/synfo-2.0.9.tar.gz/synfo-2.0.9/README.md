# synfo

[![Build Status](https://travis-ci.com/sfneal/synfo.svg?branch=master)](https://travis-ci.com/sfneal/synfo)
[![PyPi version](https://img.shields.io/pypi/v/synfo)](https://pypi.org/project/synfo)
[![PyPi Python support](https://img.shields.io/pypi/pyversions/synfo)](https://pypi.org/project/synfo)
[![PyPi downloads per month](https://img.shields.io/pypi/dm/synfo)](https://pypi.org/project/synfo)
[![PyPi license](https://img.shields.io/pypi/l/synfo)](https://pypi.org/project/synfo)
[![StyleCI](https://github.styleci.io/repos/148647095/shield?branch=master)](https://github.styleci.io/repos/148647095?branch=master)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/sfneal/synfo/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/sfneal/synfo/?branch=master)

A lightweight Python utility for retrieving system information and specifications.

Package features:

* Retrieve System, Python and Hardware related information
* Importable
* Command line callable

## Propose
synfo was developed to provide an easy way retrieve system information for various uses in any Python script.  

## Usage
Retrieve information about the current system, Python interpreter or connected hardware.  synfo can be imported as a library or called from the command line.


### Import examples
```python
# Retrieve information about Python version and compiler
from synfo import Synfo


print(Synfo().python)
# Python
# ------
# version          : 3.7.0
# compiler         : Clang 6.0 (clang-600.0.57)
```

```python
# Retrieve information about Python version and compiler
from synfo import Synfo


print(Synfo().system)
# System
# ------
# os               : Darwin
# release          : 18.2.0
# machine          : x86_64
# architecture     : 64bit
# hostname         : Stephens-TouchBar-MacBook.local
# username         : Stephen

print(Synfo().system.os)
# Darwin

```
### Command line example
```bash
>>> synfo
Python
------
version          : 3.7.0
compiler         : Clang 6.0 (clang-600.0.57)

System
------
os               : Darwin
release          : 18.2.0
machine          : x86_64
architecture     : 64bit
hostname         : Stephens-TouchBar-MacBook.local
username         : Stephen

Hardware
------
memory_installed : N/A
memory_available : N/A
processor_type   : i386
processor_cores  : 8

```

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

In order to utilize this package/repository you will need to have a Python (only tested on 3.6+ as of now) interpreter installed on your machine.

#### PyPi installation
```
pip install synfo
```

#### PyPi update
```
pip install --upgrade --no-cache-dir synfo
```

### Project Structure

```
synfo
├── __init__.py
├── _version.py
├── drives.py
├── format.py
├── package.py
└── system.py

```

### Changelog

Please see [CHANGELOG](CHANGELOG.md) for more information what has changed recently.

## Contributing

Please read [CONTRIBUTING.md](https://github.com/sfneal/synfo/CONTRIBUTING.md) for details on our code of 
conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/sfneal/synfo). 

## Authors

* **Stephen Neal** - *Initial work* - [synfo](https://github.com/sfneal)

## License

This project is licensed under the Apache License - see the [LICENSE.md](LICENSE.md) file for details
