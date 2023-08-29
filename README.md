[![License](https://img.shields.io/badge/License-LGPL_v2.1-black)](https://github.com/HenryWinterbottom-NOAA/ufs_pyutils/blob/develop/LICENSE)
![Linux](https://img.shields.io/badge/Linux-ubuntu%7Ccentos-lightgrey)
![Python Version](https://img.shields.io/badge/Python-3.5|3.6|3.7-blue)
[![Code style: black](https://img.shields.io/badge/Code%20Style-black-purple.svg)](https://github.com/psf/black)
[![Documentation Status](https://readthedocs.org/projects/ufs-pyutils/badge/?version=latest)](https://ufs-pyutils.readthedocs.io/en/latest/?badge=latest)

[![Build Tests](https://github.com/HenryWinterbottom-NOAA/ufs_pyutils/actions/workflows/buildtest.yaml/badge.svg)](https://github.com/HenryWinterbottom-NOAA/ufs_pyutils/actions/workflows/buildtest.yaml)
[![Unit Tests](https://github.com/HenryWinterbottom-NOAA/ufs_pyutils/actions/workflows/unittests.yaml/badge.svg)](https://github.com/HenryWinterbottom-NOAA/ufs_pyutils/actions/workflows/unittests.yaml)
[![Python Coding Standards](https://github.com/HenryWinterbottom-NOAA/ufs_pyutils/actions/workflows/pycodestyle.yaml/badge.svg)](https://github.com/HenryWinterbottom-NOAA/ufs_pyutils/actions/workflows/pycodestyle.yaml)

# Cloning

This repository utilizes several sub-modules from various sources. To
obtain the entire system, do as follows.

~~~shell
user@host:$ git clone --recursive https://github.com/HenryWinterbottom-NOAA/ufs_pyutils
~~~

# Dependencies

The package dependencies and the respective repository and manual
installation attributes are provided in the table below.

<div align="left">

| Package | <div align="left">Installation Instructions</div> |
| :-------------: | :-------------: | 
| <div align="left">[`astropy`](https://github.com/astropy/astropy)</div> | <div align="left">`pip install astropy==5.2`</div> |
| <div align="left">[`boto3`](https://github.com/boto/boto3)</div> | <div align="left">`pip boto3==1.24.28`</div> | 
| <div align="left">[`bs4`](https://github.com/waylan/beautifulsoup)</div> | <div align="left">`pip install bs4==0.0.1`</div> | 
| <div align="left">[`croniter`](https://github.com/kiorky/croniter)</div> | <div align="left">`pip install croniter==1.3.8`</div> | 
| <div align="left">[`lxml`](https://github.com/lxml/lxml)</div> | <div align="left">`pip install lxml==4.9.2`</div> | 
| <div align="left">[`netcdf4`](https://github.com/Unidata/netcdf4-python)</div> | <div align="left">`pip install netcdf4==1.6.2`</div> |
| <div align="left">[`numpy`](https://github.com/numpy/numpy)</div> | <div align="left">`pip install numpy==1.22.4`</div> |
| <div align="left">[`pyyaml`](https://github.com/yaml/pyyaml)</div> | <div align="left">`conda install -c anaconda pyyaml==6.0`</div> |
| <div align="left">[`rich_argparse`](https://github.com/hamdanal/rich-argparse)</div> | <div align="left">`pip install rich_argparse==1.1.1`</div> |
| <div align="left">[`schema`](https://github.com/keleshev/schema)</div> | <div align="left">`pip install schema==0.7.5`</div> | 
| <div align="left">[`tabulate`](https://github.com/gregbanks/python-tabulate)</div> | <div align="left">`pip install tabulate==0.9.0`</div> |
| <div align="left">[`xarray`](https://github.com/pydata/xarray)</div> | <div align="left">`pip install xarray==0.16.2`</div> |
| <div align="left">[`xmltodict`](https://github.com/martinblech/xmltodict)</div> | <div align="left">`pip install xmltodict==0.13.0`</div> |

</div>

# Installing Package Dependencies

In order to install the respective Python packages upon which
`ufs_pyutils` is dependent, do as follow.

~~~shell
user@host:$ cd /path/to/ufs_pyutils
user@host:$ /path/to/pip install update
user@host:$ /path/to/pip install -r /path/to/ufs_pyutils/requirements.txt
user@host:$ /path/to/conda install -y -c conda-forge --file /path/to/ufs_pyutils/requirements.conda
~~~

For additional information using `pip` and `requirements.txt` type files, see [here](https://pip.pypa.io/en/stable/reference/requirements-file-format/).

# Building and Installing

In order to install via the Python setup applications, do as follows.

~~~shell
user@host:$ cd /path/to/ufs_pyutils
user@host:$ /path/to/python setup.py build --user
user@host:$ /path/to/python setup.py install --user
~~~

For additional information and options for building Python packages, see [here](https://docs.python.org/3.5/distutils/setupscript.html).

# Docker Containers

Docker containers containing the `ufs_pyutils` dependencies can be
collected as follows.

~~~shell
user@host:$ /path/to/docker pull ghcr.io/henrywinterbottom-noaa/ubuntu20.04.ufs_pyutils:latest
~~~

To execute within the Docker container, do as follows.

~~~shell
user@host:$ /path/to/docker run -it ghcr.io/henrywinterbottom-noaa/ubuntu20.04.ufs_pyutils:latest
~~~

# Forking

If a user wishes to contribute modifications done within their
respective fork(s) to the authoritative repository, we request that
the user first submit an issue and that the fork naming conventions
follow those listed below.

- `docs/user_fork_name`: Documentation additions and/or corrections for the application(s).

- `feature/user_fork_name`: Additions, enhancements, and/or upgrades for the application(s).

- `fix/user_fork_name`: Bug-type fixes for the application(s) that do not require immediate attention.

- `hotfix/user_fork_name`: Bug-type fixes which require immediate attention to fix issues that compromise the integrity of the respective application(s).  
