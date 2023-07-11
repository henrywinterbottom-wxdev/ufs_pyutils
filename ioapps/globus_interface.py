# =========================================================================

# Module: ioapps/globus_interface.py

# Author: Henry R. Winterbottom

# Email: henry.winterbottom@noaa.gov

# This program is free software: you can redistribute it and/or modify
# it under the terms of the respective public license published by the
# Free Software Foundation and included with the repository within
# which this application is contained.

# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

# =========================================================================

"""
Module
------

    globus_interface.py

Description
-----------

   # TODO

Functions
---------

    _check_globuscli_env()

        This function checks whether the Globus CLI environment has
        been loaded; if not, a GlobusCLIInterfaceError will be raised;
        otherwise, the path to the Globus CLI executable will be
        defined and returned.

Requirements
------------

- globus-cli; https://github.com/globus/globus-cli

- globus-sdk-python; https://github.com/globus/globus-sdk-python

Author(s)
---------

    Henry R. Winterbottom; 11 July 2023

History
-------

    2023-07-11: Henry Winterbottom -- Initial implementation.

"""

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

import globus_cli
import globus_sdk

from tools import parser_interface
from utils.exceptions_interface import GlobusInterfaceError
from utils.logger_interface import Logger

# ----

logger = Logger(caller_name=__name__)

# ----


def _check_globuscli_env() -> str:
    """
    Description
    -----------

    This function checks whether the Globus CLI environment has been
    loaded; if not, a GlobusCLIInterfaceError will be raised; otherwise,
    the path to the Globus CLI executable will be defined and returned.

    Returns
    -------

    globuscli: str

        A Python string specifying the path to the Globus CLI
        executable.

    Raises
    ------

    GlobusCLIInterfaceError:

        - raised if the Globus CLI executable path cannot be
          determined.

    """

    # Check the run-time environment in order to determine the Globus
    # CLI executable path.
    globuscli = system_interface.get_app_path(app="globus")
    if globuscli is None:
        msg = (
            "The GLOBUS CLI executable could not be determined for your "
            "system; please check that the appropriate Globus CLI "
            "libaries/modules are loaded prior to calling this script. "
            "Aborting!!!"
        )
        raise GlobusCLIInterfaceError(msg=msg)

    return globuscli
