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

    build_schema(yaml_path)

        This function builds a schema provided a YAML-formatted file
        containing the variable types and attributes (if necessary);
        supported schema types are mandatory, optional (Optional), and
        multi-type (Or) variables.

        The YAML-formatted file containing the schema attributes
        should be formatted similar to the example below.

        required:
            variable1: bool
            variable2: float
            variable3: int

        optional:
            variable4:
                type: bool
                default: False
            variable5:
                type: bool
                default: True
            variable6:
                type: float
                default: 1.0

        multitype:
            variable7: str, int
            variable8: float, bool, str

    check_opts(key, valid_opts, data, check_and=False)

        This function checks that key and value pair is valid relative
        to the list of accepted values.

    validate_opts(cls_schema, cls_opts)

        This function validates the calling class schema; if the
        respective schema is not validated an exception will be
        raised; otherwise this function is passive.

Requirements
------------

- schema; https://github.com/keleshev/schema

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

from pydoc import locate
from typing import Dict, List

from confs.yaml_interface import YAML
from schema import And, Optional, Or, Schema
from tools import parser_interface

from utils.exceptions_interface import SchemaInterfaceError

# ----

# Define all available attributes.
__all__ = ["build_schema", "check_opts", "validate_opts"]

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


def build_schema(yaml_path: str) -> Dict:
    """
    Description
    -----------

    This function builds a schema provided a YAML-formatted file
    containing the variable types and attributes (if necessary);
    supported schema types are mandatory, optional (Optional), and
    multi-type (Or) variables.

    The YAML-formatted file containing the schema attributes should be
    formatted similar to the example below.

    required:
        variable1: bool
        variable2: float
        variable3: int

    optional:
        variable4:
            type: bool
            default: False
        variable5:
            type: bool
            default: True
        variable6:
            type: float
            default: 1.0

    multitype:
        variable7: str, int
        variable8: float, bool, str

    Parameters
    ----------

    yaml_path: str

        A Python string specifying the YAML-formatted file containing
        the schema attributes.

    Returns
    -------

    schema_dict: Dict

        A Python dictionary containing the define schema.

    Raises
    ------

    SchemaInterfaceError:

        - raised if the a optional variable value is not defined
          properly within YAML-formatted file path.

        - raised if the type-class for the multitype schema variable
          instances is not formatted correctly (i.e., is not a
          string).

        - raised if a multitype schema variable instance does not
          contain two or more attributes within the YAML-formatted
          file.

    """

    # Read the YAML-formatted file containing the schema.
    yaml_dict = YAML().read_yaml(yaml_file=yaml_path)

    # Define any mandatory (e.g., required) schema attributes; proceed
    # accordingly.
    schema_dict = {}

    required_dict = parser_interface.dict_key_value(
        dict_in=yaml_dict, key="required", force=True
    )
    if required_dict is not None:
        for (required_key, required_value) in required_dict.items():
            schema_dict[required_key] = locate(required_value)

    # Define any optional schema attributes; proceed accordingly.
    optional_dict = parser_interface.dict_key_value(
        dict_in=yaml_dict, key="optional", force=True
    )
    if optional_dict is not None:
        for varname in optional_dict:

            varname_dict = parser_interface.dict_key_value(
                dict_in=optional_dict, key=varname, force=True
            )
            if varname_dict is None:
                msg = (
                    f"The schema entry for optional variable {varname} in "
                    f"YAML-formatted file path {yaml_path} is not defined "
                    f"correctly; expected Dict but received NoneType. "
                    "Aborting!!!"
                )
                raise SchemaInterfaceError(msg=msg)

            varname_obj = parser_interface.dict_toobject(in_dict=varname_dict)
            schema_dict[Optional(varname, default=varname_obj.default)] = locate(
                varname_obj.type
            )

    # Define any schema attributes permitted to have multiple
    # supported Python data types; proceed accordingly.
    multitype_dict = parser_interface.dict_key_value(
        dict_in=yaml_dict, key="multitype", force=True
    )
    if multitype_dict is not None:
        for varname in multitype_dict:

            if not isinstance(multitype_dict[varname], str):
                msg = (
                    f"Multiple type variable {varname} in YAML-formatted file path "
                    f"{yaml_path} is not valid; expected str but received "
                    f"{type(multitype_dict[varname])}. Aborting!!!"
                )
                raise SchemaInterfaceError(msg=msg)

            if len(multitype_dict[varname]) <= 1:
                msg = (
                    "Multi-type variables must contain 2 or more supported Python types; "
                    f"for variable {varname} in YAML-formatted file path {yaml_path} "
                    f"received {multitype_dict[varname]}. Aborting!!!"
                )
                raise SchemaInterfaceError(msg=msg)

            type_gen = (
                locate(vartype.strip())
                for vartype in multitype_dict[varname].split(",")
            )

            schema_dict[varname] = Or(
                *(next(type_gen) for vartype in multitype_dict[varname].split(","))
            )

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


def validate_opts(cls_schema: Dict, cls_opts: Dict) -> None:
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

    Raises
    ------

    SchemaInterfaceError:

        - raised if an exception is encountered while validating the
          schema.

    """

    # Define the schema.
    schema = Schema([cls_schema])

    # Check that the class attributes are valid; proceed accordingly.
    try:

        # Validate the schema.
        schema.validate([cls_opts])

    except Exception as errmsg:

        msg = f"Schema validation failed with error {errmsg}. Aborting!!!"
        raise SchemaInterfaceError(msg=msg) from errmsg
