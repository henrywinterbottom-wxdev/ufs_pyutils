# =========================================================================

# Module: utils/schema_interface.py

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

    schema_interface.py

Description
-----------

    This module contains functions to validate calling class and/or
    function attributes.

Functions
---------

    __andopts__(key, valid_opts)

        This function builds a Python schema dictionary using the And
        attribute.

    __buildtbl__(cls_schema, cls_opts, logger_method)

        This function compiles and writes a table using the defined
        logger method for the respective schema attributes and the
        values corresponding to the respective application.

    __def_schema__(schema_dict, ignore_extra_keys=True)

        This function defines the schema object in accordance with the
        specified parameters.

    build_schema(schema_def_dict)

        This function builds a schema provided a YAML-formatted file
        containing the variable types and attributes (if necessary);
        supported schema types are mandatory (e.g., `required = True`)
        and optional (e.g., `required = False` or is not defined
        within the schema definitions (`schema_def_dict` key and value
        pairs.

        The YAML-formatted file containing the schema attributes
        should be formatted similar to the example below.

        variable1:
            required: False
            type: bool
            default: True

        variable2:
            required: True
            type: float

        variable3:
            type: int
            default: 1

    check_opts(key, valid_opts, data, check_and=False)

        This function checks that key and value pair is valid relative
        to the list of accepted values.

    validate_opts(cls_schema, cls_opts)

        This function validates the calling class schema; if the
        respective schema is not validated an exception will be
        raised; otherwise this function is passive.

    validate_schema(cls_schema, cls_opts, ignore_extra_keys=True,
                    write_table=True, logger_method="info")

        This method validates the specified caller method options
        against the specified schema; schema optional values (denoted
        as `Optional` instances) are assigned default values during
        instances when the caller method options (`cls_opts`) as not
        defined a corresponding value.

Requirements
------------

- schema; https://github.com/keleshev/schema

- tabulate; https://github.com/gregbanks/python-tabulate

Author(s)
---------

    Henry R. Winterbottom; 27 December 2022

History
-------

    2022-12-27: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=broad-except

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

from collections import OrderedDict
from pydoc import locate
from typing import Dict, List

from schema import And, Optional, Schema
from tabulate import tabulate
from tools import parser_interface

from utils.exceptions_interface import SchemaInterfaceError
from utils.logger_interface import Logger

# ----

# Define all available attributes.
__all__ = ["build_schema", "check_opts", "validate_opts", "validate_schema"]

# ----

logger = Logger(caller_name=__name__)

# ----


def __andopts__(key: str, valid_opts: List) -> Dict:
    """
    Description
    -----------

    This function builds a Python schema dictionary using the And
    attribute.

    Parameters
    ----------

    key: str

        A Python string specifying the key for which to valid the
        respective value against list of accepted values.

    valid_opts: List

        A Python list containing the accepted values.

    Returns
    -------

    schema_dict: Dict

        A Python dictionary containing the schema to be validated.

    """

    schema_dict = {f"{key}": And(str, lambda opt: opt in valid_opts)}

    return schema_dict


# ----


def __buildtbl__(cls_schema: Dict, cls_opts: Dict, logger_method: str) -> None:
    """
    Description
    -----------

    This function compiles and writes a table using the defined logger
    method for the respective schema attributes and the values
    corresponding to the respective application.

    Parameters
    ----------

    cls_schema: Dict

        A Python dictionary containing the calling class schema.

    cls_opts: Dict

        A Python dictionary containing the options (i.e., parameter
        arguments, keyword arguments, etc.,) passed to the respective
        calling class.

    logger_method: str

        A Python string specifying the logger method to be usedf to
        write the schema attributes table.

    Raises
    ------

    SchemaInterfaceError:

        - raised if the logger method defined by `logger_method` upon
          entry is not supported.

    """

    # Build the table attributes.
    header = ["Variable", "Type", "Optional", "Value"]
    table = []
    for (cls_key, _) in OrderedDict(cls_schema).items():
        if "bool" in cls_schema[cls_key].__name__:
            value = str(bool(cls_opts[cls_key]))
        else:
            value = cls_opts[cls_key.key]

        if isinstance(cls_key, Optional):
            msg = [cls_key.key, cls_schema[cls_key].__name__, "True", value]

        if not isinstance(cls_key, Optional):
            msg = [cls_key, cls_schema[cls_key].__name__, "False", value]
        table.append(msg)

    # Write the table using the logger method.
    msg = (
        "\n\n"
        + tabulate(
            table,
            header,
            tablefmt="outline",
            numalign=("center", "center", "center", "center"),
            colalign=("center", "center", "center", "center"),
            disable_numparse=True,
        )
        + "\n\n"
    )

    logmethod = parser_interface.object_getattr(
        object_in=logger, key=logger_method.lower(), force=True
    )
    if logmethod is None:
        msg = f"Logger method {logger_method} is not supported. Aborting!!!"
        raise SchemaInterfaceError(msg=msg)
    logmethod(msg=msg)


# ----


def __def_schema__(schema_dict: Dict, ignore_extra_keys: bool = True) -> Schema:
    """
    Description
    -----------

    This function defines the schema object in accordance with the
    specified parameters.

    Parameters
    ----------

    schema_dict: Dict

        A Python dictionary containing the defined schema.

    Keywords
    --------

    ignore_extra_keys: bool, optional

        A Python boolean valued variable specifying whether to ignore
        extra keys that are contained with the Python dictionary
        containing the schema to be validated.

    Returns
    -------

    schema: Schema

        A Python object containing the defined schema object.

    """

    # Define the schema object.
    schema = Schema([schema_dict], ignore_extra_keys=ignore_extra_keys)

    return schema


# ----


def build_schema(schema_def_dict: Dict) -> Dict:
    """
    Description
    -----------

    This function builds a schema provided a YAML-formatted file
    containing the variable types and attributes (if necessary);
    supported schema types are mandatory (e.g., `required = True`) and
    optional (e.g., `required = False` or is not defined within the
    schema definitions (`schema_def_dict` key and value pairs.

    The YAML-formatted file containing the schema attributes should be
    formatted similar to the example below.

    variable1:
        required: False
        type: bool
        default: True

    variable2:
        required: True
        type: float

    variable3:
        type: int
        default: 1

    Parameters
    ----------

    schema_def_dict: Dict

        A Python dictionary containing the schema definition
        attributes; these contents are collect from a YAML-formatted
        file containing the respective variables and corresponding
        attributes and defined above.

    Returns
    -------

    schema_dict: Dict

        A Python dictionary containing the defined schema.

    Raises
    ------

    SchemaInterfaceError:

        - raised if an exception is encountered while defining the
          default value for optional schema attributes; this is most
          often encountered when a key and value pair corresponding to
          the attribute `default` for an optional variable is not
          defined for the respective schema variable.

    """

    # Build the schema for the respective application.
    schema_dict = {}
    for schema_def in schema_def_dict:
        schema_attr_dict = parser_interface.dict_key_value(
            dict_in=schema_def_dict, key=schema_def, no_split=True
        )

        # Check whether the schema attribute is optional (e.g.,
        # required); proceed accordingly.
        if "required" in schema_attr_dict:
            schema_attr_dict["required"] = schema_def_dict[schema_def]["required"]
            if schema_attr_dict["required"]:
                schema_dict[schema_def] = locate(schema_attr_dict["type"])

        else:
            schema_attr_dict["required"] = False

        if not schema_attr_dict["required"]:
            try:
                msg = (
                    f"Found optional variable {schema_def}; setting to type "
                    f"{schema_attr_dict['type']}; default value is "
                    f"{schema_attr_dict['default']}."
                )
                logger.warn(msg=msg)
                schema_dict[
                    Optional(schema_def, default=schema_attr_dict["default"])
                ] = locate(schema_attr_dict["type"])
            except Exception as errmsg:
                msg = (
                    f"Defining schema for variable {schema_def} failed with "
                    f"error {errmsg}. Aborting!!!"
                )
                raise SchemaInterfaceError(msg=msg) from errmsg

        if schema_attr_dict["required"]:
            msg = (
                f"Found required variable {schema_def}; setting to type "
                f"{schema_attr_dict['type']}."
            )
            logger.info(msg=msg)
            schema_dict[schema_def] = locate(schema_attr_dict["type"])

    return schema_dict


# ----


def check_opts(key: str, valid_opts: List, data: Dict, check_and: bool = False) -> None:
    """
    Description
    -----------

    This function checks that key and value pair is valid relative to
    the list of accepted values.

    Parameters
    ----------

    key: str

        A Python string specifying the key for which to validate the
        respective value against list of accepted values.

    valid_opts: List

        A Python list containing the accepted values.

    data: Dict

        A Python dictionary containing the key and value pair which to
        validate.

    Keywords
    --------

    check_and: bool, optional

        A Python boolean valued variable specifying whether to
        construct the Python schema dictionary using the And
        attribute; see __andopts__.

    Raises
    ------

    SchemaInterfaceError:

        - raised if an exception is encountered while validating the
          schema.

    """

    if check_and:
        schema_dict = __andopts__(key=key, valid_opts=valid_opts)

    # Build the schema.
    schema = Schema([schema_dict])

    # Check that the respective key and value pair is valid; proceed
    # accordingly.
    try:

        # Validate the schema.
        schema.validate([data])

    except Exception as errmsg:

        msg = f"Schema validation failed with error {errmsg}. Aborting!!!"
        raise SchemaInterfaceError(msg=msg) from errmsg


# ----


def validate_opts(
    cls_schema: Dict, cls_opts: Dict, ignore_extra_keys: bool = True
) -> None:
    """
    Description
    -----------

    This function validates the calling class schema; if the
    respective schema is not validated an exception will be raised;
    otherwise this function is passive.

    Parameters
    ----------

    cls_schema: Dict

        A Python dictionary containing the calling class schema.

    cls_opts: Dict

        A Python dictionary containing the options (i.e., parameter
        arguments, keyword arguments, etc.,) passed to the respective
        calling class.

    Keywords
    --------

    ignore_extra_keys: bool, optional

        A Python boolean valued variable specifying whether to ignore
        extra keys that are contained with the Python dictionary
        containing the schema to be validated (`cls_opts`).

    Raises
    ------

    SchemaInterfaceError:

        - raised if an exception is encountered while validating the
          schema.

    """

    # Define the schema.
    schema = __def_schema__(schema_dict=cls_schema,
                            ignore_extra_keys=ignore_extra_keys)

    # Check that the class attributes are valid; proceed accordingly.
    try:

        # Validate the schema.
        schema.validate([cls_opts])

    except Exception as errmsg:

        msg = f"Schema validation failed with error {errmsg}. Aborting!!!"
        raise SchemaInterfaceError(msg=msg) from errmsg


# ----


def validate_schema(
    cls_schema: Dict,
    cls_opts: Dict,
    ignore_extra_keys: bool = True,
    write_table: bool = True,
    logger_method: str = "info",
) -> Dict:
    """
    Description
    -----------

    This method validates the specified caller method options against
    the specified schema; schema optional values (denoted as
    `Optional` instances) are assigned default values during instances
    when the caller method options (`cls_opts`) as not defined a
    corresponding value.

    Parameters
    ----------

    cls_schema: Dict

        A Python dictionary containing the calling class schema.

    cls_opts: Dict

        A Python dictionary containing the options (i.e., parameter
        arguments, keyword arguments, etc.,) passed to the respective
        calling class.

    Keywords
    --------

    ignore_extra_keys: bool, optional

        A Python boolean valued variable specifying whether to ignore
        extra keys that are contained with the Python dictionary
        containing the schema to be validated (`cls_opts`).

    write_table: bool, optional

        A Python boolean valued variable specifying whether to write
        the schema attributes table using the specified logger method.

    logger_method: str, optional

        A Python string specifying the logger method to be usedf to
        write the schema attributes table.

    Returns
    -------

    cls_opts: Dict

        A Python dictionary containing the options defined upon entry
        and updated to contain any optional schema default key and
        value pairs if not specified within the Python dictionary upon
        entry.

    """

    # Define the schema.
    schema = __def_schema__(schema_dict=cls_schema,
                            ignore_extra_keys=ignore_extra_keys)

    # Check that any optional schema attributes have been specified by
    # the calling class attributes (`cls_opts`); if not, assign the
    # schema default key and value pairs; proceed accordingly.
    for (cls_key, _) in cls_schema.items():
        if isinstance(cls_key, Optional):
            if cls_key.key not in cls_opts:
                msg = (
                    f"Schema optional value {cls_key.key} has not be defined; setting to "
                    f"default value {cls_key.default}."
                )
                logger.warn(msg=msg)

                cls_opts[cls_key.key] = cls_key.default

    # Validate the schema and build and write a table containing the
    # calling class attributes; proceed accordingly.
    schema.validate([cls_opts])
    if write_table:
        __buildtbl__(
            cls_schema=cls_schema, cls_opts=cls_opts, logger_method=logger_method
        )

    return cls_opts
