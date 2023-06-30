# =========================================================================

# Module: utils/table_interface.py

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

    table_interface.py

Description
-----------

    This module provides functions to compose tables using the the
    Python `tabulate` library.

Functions
---------

    __buildtbl__(table_obj)

        This function builds composes a table using to be returned by
        the specified logger method.

    __chkschema__(table_obj)

        This method validates the schema for the respective table
        attributes; if Optional-type attributes are not defined, they
        are assigned the respective default values.

    __getncols__(table_obj)

        This method determines and returns the total number of columns
        for the respective table.

    compose(table_obj)

        This method composes and outputs the specified table in
        accordance with the attributes specified within the
        `table_obj` SimpleNamespace object upon entry.

Requirements
------------

- tabulate; https://github.com/gregbanks/python-tabulate

Author(s)
---------

    Henry R. Winterbottom; 18 May 2023

"""

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

from types import SimpleNamespace

from schema import Optional
from tabulate import tabulate
from tools import parser_interface

from utils import schema_interface
from utils.logger_interface import Logger

# ----

# Define all available attributes.
__all__ = ["compose"
           ]

# ----

logger = Logger(caller_name=__name__)

# ----


def __buildtbl__(table_obj: SimpleNamespace) -> str:
    """
    Description
    -----------

    This function builds composes a table using to be returned by the
    specified logger method.

    Parameters
    ----------

    table_obj: SimpleNamespace

        A Python SimpleNamespace object containing the table
        attributes.

    Returns
    -------

    table: str

        A Python string containing the composed table.

    """

    # Build the table accordingly.
    table = tabulate(
        table_obj.table,
        table_obj.header,
        tablefmt=table_obj.tablefmt,
        numalign=table_obj.numalign,
        colalign=table_obj.colalign,
        disable_numparse=table_obj.disable_numparse,
    )

    return table


# ----


def __chkschema__(table_obj: SimpleNamespace) -> SimpleNamespace:
    """
    Description
    -----------

    This method validates the schema for the respective table
    attributes; if Optional-type attributes are not defined, they are
    assigned the respective default values.

    Parameters
    ----------

    table_obj: SimpleNamespace

        A Python SimpleNamespace object containing the table
        attributes.

    Returns
    -------

    table_obj: SimpleNamespace

        A Python SimpleNamespace object containing the table
        attributes; if Optional-type attributes have not been
        specified within the `table_obj` SimpleNamespace upon entry,
        they are updated to use the specified schema default values.

    """

    # Define the total number of table columns.
    ncols = __getncols__(table_obj=table_obj)

    # Define and evaluate the table schema; replace any missing
    # Optional-type attributes with the specified default values.
    cls_schema = {
        "header": list,
        "table": list,
        Optional("tablefmt", default="outline"): str,
        Optional("numalign", default=ncols * ["center"]): list,
        Optional("colalign", default=ncols * ["center"]): list,
        Optional("disable_numparse", default=False): bool,
    }

    # Update the table attributes accordingly.
    cls_opts = {}
    for table_attr in vars(table_obj):
        cls_opts[table_attr] = parser_interface.object_getattr(
            object_in=table_obj, key=table_attr
        )

    schema_dict = schema_interface.validate_schema(
        cls_schema=cls_schema,
        cls_opts=cls_opts,
        ignore_extra_keys=True,
        write_table=False,
    )

    for (schema_key, schema_value) in schema_dict.items():
        table_obj = parser_interface.object_setattr(
            object_in=table_obj, key=schema_key, value=schema_value
        )

    return table_obj


# ----


def __getncols__(table_obj: SimpleNamespace) -> int:
    """
    Description
    -----------

    This method determines and returns the total number of columns for
    the respective table.

    Parameters
    ----------

    table_obj: SimpleNamespace

        A Python SimpleNamespace object containing the table
        attributes.

    Returns
    -------

    ncols: int

        A Python integer defining the total number of columns for the
        respective table.

    """

    ncols = len(table_obj.table[0])

    return ncols


# ----


def compose(table_obj: SimpleNamespace) -> str:
    """
    Description
    -----------

    This method composes and outputs the specified table in accordance
    with the attributes specified within the `table_obj`
    SimpleNamespace object upon entry.

    Parameters
    ----------

    table_obj: SimpleNamespace

        A Python SimpleNamespace object containing the table
        attributes.

    Returns
    -------

    table: str

        A Python object containing the composed table.

    """

    # Evaluate the schema and compose the respective table.
    table_obj = __chkschema__(table_obj=table_obj)
    table = __buildtbl__(table_obj=table_obj)

    return table
