# =========================================================================

# Module: confs/enviro_interface.py

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

    enviro_interface.py

Description
-----------

    This module contains function and objects to parser run-time
    environments.

Functions
---------

    enviro_to_obj()

        This method collects the status of the environment upon entry
        and casts and returns the environment attributes as a Python
        object.

Author(s)
---------

    Henry R. Winterbottom; 21 March 2023

History
-------

    2023-03-21: Henry Winterbottom -- Initial implementation.

"""

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

import os

from tools import parser_interface
from utils.exceptions_interface import EnviroInterfaceError
from utils.logger_interface import Logger

# ----

# Define all available functions.
__all__ = ["enviro_to_obj"]

# ----

logger = Logger(caller_name=__name__)

# ----


def enviro_to_obj() -> object:
    """
    Description
    -----------

    This method collects the status of the environment upon entry and
    casts and returns the environment attributes as a Python object.

    Returns
    -------

    envobj: object

        A Python object containing the environment attributes.

    Raises
    ------

    EnviroInterfaceError:

        - raised if an exception is encountered while parsing the
          environment and/or building the Python object.

    """

    # Collect the run-time argument environment and format
    # accordingly.
    envdict = parser_interface.dict_formatter(in_dict=dict(os.environ))

    # Build the output object; proceed accordingly.
    envobj = parser_interface.object_define()

    for envvar in envdict:

        try:
            value = parser_interface.dict_key_value(
                dict_in=envdict, key=envvar, no_split=True
            )
            envobj = parser_interface.object_setattr(
                object_in=envobj, key=envvar, value=value
            )

        except Exception as errmsg:
            msg = (
                "Casting the runtime environment as a Python dictionary "
                f"failed with error {errmsg}. Aborting!!!"
            )
            raise EnviroInterfaceError(msg=msg) from errmsg

    return envobj
