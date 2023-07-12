![Linux](https://img.shields.io/badge/Linux-ubuntu%7Ccentos-lightgrey)
![Python Version](https://img.shields.io/badge/Python-3.5|3.6|3.7|3.8|3.9-blue)
[![Code style: black](https://img.shields.io/badge/Code%20Style-black-purple.svg)](https://github.com/psf/black)
[![Documentation Status](https://img.shields.io/badge/Documentation-latest-gree)](https://ufs-pyutils.readthedocs.io/en/latest/?badge=latest)

[![Build Tests](https://github.com/HenryWinterbottom-NOAA/ufs_pyutils/actions/workflows/buildtest.yaml/badge.svg)](https://github.com/HenryWinterbottom-NOAA/ufs_pyutils/actions/workflows/buildtest.yaml)
[![Unit Tests](https://github.com/HenryWinterbottom-NOAA/ufs_pyutils/actions/workflows/unittests.yaml/badge.svg)](https://github.com/HenryWinterbottom-NOAA/ufs_pyutils/actions/workflows/unittests.yaml)
[![Python Coding Standards](https://github.com/HenryWinterbottom-NOAA/ufs_pyutils/actions/workflows/pycodestyle.yaml/badge.svg)](https://github.com/HenryWinterbottom-NOAA/ufs_pyutils/actions/workflows/pycodestyle.yaml)
[![Container Builds](https://github.com/HenryWinterbottom-NOAA/ufs_pyutils/actions/workflows/containers.yaml/badge.svg)](https://github.com/HenryWinterbottom-NOAA/ufs_pyutils/actions/workflows/containers.yaml)
[![PyPI](https://github.com/HenryWinterbottom-NOAA/ufs_pyutils/actions/workflows/pypi.yaml/badge.svg)](https://github.com/HenryWinterbottom-NOAA/ufs_pyutils/actions/workflows/pypi.yaml)

# Purpose

This the `ufs_pyutils` package contains an API utilized by multiple
[Unified Forecast System](https://ufscommunity.org/) (UFS)
applications. However, it is not limited only to such applications and
may be where the provided application interfaces are valid and/or
useful.

# Installation

The `ufs_pyutils` package may be installed as follows.

~~~
user@host:$ /path/to/pip install ufs_pyutils
~~~

The available unit-tests for the available APIs may be executed as
follows.

~~~
user@host:$ cd /path/to/ufs_pyutils
user@host:$ /path/to/pytest confs
user@host:$ /path/to/pytest ioapps
user@host:$ /path/to/pytest tools
user@host:$ /path/to/pytest utils
~~~

Note that the respective unit-tests require
[pytest](https://github.com/pytest-dev/pytest) and
[pytest-order](https://github.com/pytest-dev/pytest-order).

# Documentation

The API documentation can be found [here](https://ufs-pyutils.readthedocs.io/en/latest/).