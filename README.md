[![License](https://img.shields.io/badge/license-LGPL_v2.1-black)](https://github.com/HenryWinterbottom-NOAA/ufs_pyutils/blob/develop/LICENSE)
![Linux](https://img.shields.io/badge/linux-ubuntu%7Ccentos-lightgrey)
![Python Version](https://img.shields.io/badge/python-3.5|3.6|3.7-blue)

[![](https://img.shields.io/badge/dependencies-astropy-orange)](https://github.com/astropy/astropy)
[![Dependencies](https://img.shields.io/badge/dependencies-boto3-orange)](https://github.com/boto/boto3)
[![Dependencies](https://img.shields.io/badge/dependencies-bs4-orange)](https://github.com/waylan/beautifulsoup)
[![Dependencies](https://img.shields.io/badge/dependencies-croniter-orange)](https://github.com/kiorky/croniter)
[![Dependencies](https://img.shields.io/badge/dependencies-lxml-orange)](https://github.com/lxml/lxml)
[![Dependencies](https://img.shields.io/badge/dependencies-netcdf4-orange)](https://github.com/Unidata/netcdf4-python)
[![Dependencies](https://img.shields.io/badge/dependencies-numpy-orange)](https://github.com/numpy/numpy)
[![Dependencies](https://img.shields.io/badge/dependencies-pyyaml-orange)](https://github.com/yaml/pyyaml)
[![Dependencies](https://img.shields.io/badge/dependencies-rich__argparse-orange)](https://github.com/hamdanal/rich-argparse)
[![Dependencies](https://img.shields.io/badge/dependencies-schema-orange)](https://github.com/keleshev/schema)
[![Dependencies](https://img.shields.io/badge/dependencies-tabulate-orange)](https://github.com/gregbanks/python-tabulate)
[![Dependencies](https://img.shields.io/badge/dependencies-xmltodict-orange)](https://github.com/martinblech/xmltodict)

[![Build Tests](https://github.com/HenryWinterbottom-NOAA/ufs_pyutils/actions/workflows/buildtest.yaml/badge.svg)](https://github.com/HenryWinterbottom-NOAA/ufs_pyutils/actions/workflows/buildtest.yaml)
[![Unit Tests](https://github.com/HenryWinterbottom-NOAA/ufs_pyutils/actions/workflows/unittests.yaml/badge.svg)](https://github.com/HenryWinterbottom-NOAA/ufs_pyutils/actions/workflows/unittests.yaml)
[![Python Coding Standards](https://github.com/HenryWinterbottom-NOAA/ufs_pyutils/actions/workflows/pycodestyle.yaml/badge.svg)](https://github.com/HenryWinterbottom-NOAA/ufs_pyutils/actions/workflows/pycodestyle.yaml)
[![Container Builds](https://github.com/HenryWinterbottom-NOAA/ufs_pyutils/actions/workflows/containers.yaml/badge.svg)](https://github.com/HenryWinterbottom-NOAA/ufs_pyutils/actions/workflows/containers.yaml)

# Cloning

This repository utilizes several sub-modules from various sources. To
obtain the entire system, do as follows.

~~~
user@host:$ git clone https://github.com/HenryWinterbottom-NOAA/ufs_pyutils
~~~

# Dependencies

The package dependencies and the respective repository and manual
installation attributes are provided in the table below.

<div align="center">

| Dependency Package | Installation Instructions |
| :-------------: | :-------------: | 
| [`astropy`](https://github.com/astropy/astropy) | <div align="left">`pip install astropy==5.2`</div> | 
| [`boto3`](https://github.com/boto/boto3) | <div align="left">`pip boto3==1.24.28`</div> | 
| [`bs4`](https://github.com/waylan/beautifulsoup) | <div align="left">`pip install bs4==0.0.1`</div> | 
| [`croniter`](https://github.com/kiorky/croniter) | <div align="left">`pip install croniter==1.3.8`</div> |
| [`lxml`](https://github.com/lxml/lxml) | <div align="left">`pip install lxml==4.9.2`</div> |
| [`netcdf4`](https://github.com/Unidata/netcdf4-python) | <div align="left">`pip install netcdf4==1.6.2`</div> |
| [`numpy`](https://github.com/numpy/numpy) | <div align="left">`pip install numpy==1.22.4`</div> |
| [`pyyaml`](https://github.com/yaml/pyyaml) | <div align="left">`conda install -c anaconda pyyaml==6.0`</div> |
| [`rich_argparse`](https://github.com/hamdanal/rich-argparse) | <div align="left">`pip install rich_argparse==1.1.1`</div> |
| [`schema`](https://github.com/keleshev/schema) | <div align="left">`pip install schema==0.7.5`</div> |
| [`tabulate`](https://github.com/gregbanks/python-tabulate) | <div align="left">`pip install tabulate==0.9.0`</div> | 
| [`xmltodict`](https://github.com/martinblech/xmltodict) | <div align="left">`pip install xmltodict==0.13.0`</div> |

</div>

# Installing Package Dependencies

In order to install the respective Python packages upon which
`ufs_pyutils` is dependent, do as follow.

~~~
user@host:$ cd ufs_pyutils
user@host:$ /path/to/pip install update
user@host:$ /path/to/pip install -r /path/to/ufs_pyutils/requirements.txt
~~~

For additional information using `pip` and `requirements.txt` type files, see [here](https://pip.pypa.io/en/stable/reference/requirements-file-format/).

# Building and Installing

In order to install via the Python setup applications, do as follows.

~~~
user@host:$ cd ufs_pyutils
user@host:$ python setup.py build
user@host:$ python setup.py install
~~~

For additional information and options for building Python packages, see [here](https://docs.python.org/3.5/distutils/setupscript.html).

A Docker image exist containing the applications in this repository and can be collected as follows.

~~~
user@host:$ docker pull noaaufsrnr/ubuntu20.04-miniconda-ufs_pyutils:latest
~~~

A corresponding Singularity image may be built as follows.

~~~
user@host:$ singularity build ufs_pyutils_latest.sif docker://noaaufsrnr/noaaufsrnr/ufs_pyutils:latest
~~~

The attribute `latest` refers to the respective tag. For a specific tag, replace `latest` with the desired tag.

# Forking

If a user wishes to contribute modifications done within their
respective fork(s) to the authoritative repository, we request that
the user first submit an issue and that the fork naming conventions
follow those listed below.

- `docs/user_fork_name`: Documentation additions and/or corrections for the application(s).

- `feature/user_fork_name`: Additions, enhancements, and/or upgrades for the application(s).

- `fix/user_fork_name`: Bug-type fixes for the application(s) that do not require immediate attention.

- `hotfix/user_fork_name`: Bug-type fixes which require immediate attention to fix issues that compromise the integrity of the respective application(s).  
