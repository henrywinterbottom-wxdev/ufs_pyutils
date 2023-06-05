# =========================================================================

# Module: utils/cli_interface.py

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

    cli_interface.py

Description
-----------

    This module contains functions to be used for any command line
    interface (CLI) argument collection(s) and schema validation(s).

Functions
---------

    __checkschema__(parser, options_obj, schema_path, write_table = False,
                    logger_method = "info")

        This function validates the CLI argument schema.

    __get_knownargs__(parser)

        This function collects the known (i.e., mandatory) arguments
        from the CLI.

    __get_otherargs__(parser, options_obj)

        This function collects any ancillary arguments from the CLI
        and updates the `options_obj` SimpleNamespace.

    init(args_objs, description = None, prog = None, epilog = None,
        formatter_class=RichHelpFormatter)

        This function initializes a Python ArgumentParser object in
        accordance with the specified argument SimpleNamespace objects
        and the respective keyword attributes.

    options(options(parser, validate_schema=False, schema_path=None)

        This function defines a Python SimpleNamespace object
        containing both the mandatory and the ancillary CLI arguments.

Requirements
------------

- rich_argparse; https://github.com/hamdanal/rich-argparse

Author(s)
---------

    Henry R. Winterbottom; 04 June 2023

History
-------

    2023-06-04: Henry Winterbottom -- Initial implementation.

"""

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

from argparse import ArgumentParser
from types import SimpleNamespace
from typing import Any, Tuple

from confs.yaml_interface import YAML
from rich_argparse import RichHelpFormatter
from tools import parser_interface

from utils import schema_interface
from utils.exceptions_interface import CLIInterfaceError

# ----

# Define all available attributes.
__all__ = ["init", "options"]

# ----

# Set the default ArgumentParser formatter class attributes.
RichHelpFormatter.styles["argparse.args"] = "green"
RichHelpFormatter.styles["argparse.metavar"] = "cyan"
RichHelpFormatter.styles["argparse.text"] = "default"
RichHelpFormatter.styles["argparse.help"] = "blue_violet"

# ----


def __checkschema__(
    options_obj: SimpleNamespace,
    schema_path: str,
    write_table: bool = False,
    logger_method: str = "info",
) -> SimpleNamespace:
    """
    Description
    -----------

    This function validates the CLI argument schema.

    Parameters
    ----------

    options_obj: SimpleNamespace

        A Python SimpleNamespace containing the specified CLI
        arguments.

    schema_path: str

        A Python string specifying the path to the YAML-formatted file
        containing the CLI argument schema.

    Keywords
    ---------

    write_table: bool, optional

        A Python boolean valued variable specifying whether to write
        the schema attributes table using the specified logger method.

    logger_method: str, optional

        A Python string specifying the logger method to be usedf to
        write the schema attributes table.

    """

    # Validate the CLI argument schema.
    cls_schema = schema_interface.build_schema(
        YAML().read_yaml(yaml_file=schema_path))
    cls_opts = parser_interface.object_todict(object_in=options_obj)
    options_obj = schema_interface.validate_schema(
        cls_schema=cls_schema,
        cls_opts=cls_opts,
        write_table=write_table,
        logger_method=logger_method.lower(),
    )

    return options_obj


# ----


def __get_knownargs__(parser: ArgumentParser) -> SimpleNamespace:
    """
    Description
    -----------

    This function collects the known (i.e., mandatory) arguments from
    the CLI.

    Parameters
    ----------

    parser: ArgumentParser

        A Python ArgumentParser object containing the CLI arguments.

    Returns
    -------

    options_obj: SimpleNamespace

        A Python SimpleNamespace containing the (any) mandatory CLI
        arguments.

    """

    # Collect any mandatory arguments from the CLI.
    options_obj = parser_interface.object_define()
    args_obj = parser.parse_known_args()[0]

    for opt in vars(args_obj):
        options_obj = parser_interface.object_setattr(
            object_in=options_obj,
            key=opt,
            value=parser_interface.object_getattr(
                object_in=args_obj, key=opt, force=True
            ),
        )

    return options_obj


# ----


def __get_otherargs__(
    parser: ArgumentParser, options_obj: SimpleNamespace
) -> SimpleNamespace:
    """
    Description
    -----------

    This function collects any ancillary arguments from the CLI and
    updates the `options_obj` SimpleNamespace.

    Parameters
    ----------

    parser: ArgumentParser

        A Python ArgumentParser object containing the CLI arguments.

    options_obj: SimpleNamespace

        A Python SimpleNamespace containing the (any) mandatory CLI
        arguments.

    Returns
    -------

    options_obj: SimpleNamespace

        A Python SimpleNamespace object specified upon entry and
        updated with any ancillary CLI arguments.

    """

    otherargs_list = parser.parse_known_intermixed_args()[1]

    for idx in range(0, len(otherargs_list), 2):
        options_obj = parser_interface.object_setattr(
            object_in=options_obj,
            key="".join(otherargs_list[idx].split("-")[::-1]),
            value=otherargs_list[idx + 1],
        )

    return options_obj


# ----


def init(
    args_objs: Tuple[SimpleNamespace],
    description: str = None,
    prog: str = None,
    epilog: str = None,
    formatter_class: Any = RichHelpFormatter,
) -> ArgumentParser:
    """
    Description
    -----------

    This function initializes a Python ArgumentParser object in
    accordance with the specified argument SimpleNamespace objects and
    the respective keyword attributes.

    Parameters
    ----------

    args_objs: Tuple[SimpleNamespace]

        A Python tuple of SimpleNamespace objects containing the
        mandatory, optional, and task arguments.

    Keywords
    --------

    description: str, optional

        A Python string defining the purpose of the respective
        application/program.

    prog: str, optional

        A Python string specifying the program name.

    epilog: str, optional

        A Python string specifying text to be provided at the bottom
        of a `help` type message.

    formatter_class: Any

        A Python Argparse customizing class.

    Returns
    -------

    parser: ArgumentParser

        A Python ArgumentParser object.

    Raises
    ------

    CLIInterfaceError:

        - raised if the attribute `longname` has not been specified in
          an `args_obj` SimpleNamespace object.

        - raised if an exception is encountered while initializing the
          CLI.

    """

    # Initialize the CLI.
    parser = ArgumentParser(
        prog=prog,
        description=description,
        epilog=epilog,
        formatter_class=formatter_class,
    )

    # Define the respective mandatory, optional, and task application
    # attributes accordingly.
    for arg_obj in args_objs:
        argdict = dict(
            [key, value]
            for (key, value) in vars(arg_obj).items()
            if key not in ["longname", "shortname"]
        )
        arg_obj.longname = parser_interface.object_getattr(
            object_in=arg_obj, key="longname", force=True
        )
        arg_obj.shortname = parser_interface.object_getattr(
            object_in=arg_obj, key="shortname", force=True
        )
        if arg_obj.longname is None:
            msg = f"The attribute `longname` for {arg_obj} is {arg_obj.longname}. Aborting!!!"
            raise CLIInterfaceError(msg=msg)

        try:
            if (arg_obj.longname is not None) and (arg_obj.shortname is not None):
                parser.add_argument(
                    f"--{arg_obj.longname}", f"-{arg_obj.shortname}", **argdict
                )
            if (arg_obj.longname is not None) and (arg_obj.shortname is None):
                parser.add_argument(f"--{arg_obj.longname}", **argdict)
        except Exception as errmsg:
            msg = f"Initializing the CLI failed with error {errmsg}. Aborting!!!"
            raise CLIInterfaceError(msg=msg) from errmsg

    return parser


# ----


def options(
    parser: ArgumentParser, validate_schema: bool = False, schema_path: str = None
) -> SimpleNamespace:
    """
    Description
    -----------

    This function defines a Python SimpleNamespace object containing
    both the mandatory and the ancillary CLI arguments.

    Parameters
    ----------

    parser: ArgumentParser

        A Python ArgumentParser object containing the CLI arguments.

    Keywords
    --------

    validate_schema: bool, optional

        A Python boolean valued variable specifying whether to
        validate the schema for the respective CLI arguments; if
        `True` upon entry, either the CLI arguments must contain the
        attribute `schema` or the `schema_path` must be specified upon
        entry.

    schema_path: str, optional

        A Python string specifying the path to the YAML-formatted file
        containing the CLI argument schema.

    Raises
    ------

    CLIInterfaceError:

        - raised if the `schema_path` attribute is NoneType when
          attempting to validate the CLI argument schema.

    """

    # Define the CLI arguments.
    options_obj = __get_knownargs__(parser=parser)
    options_obj = __get_otherargs__(parser=parser, options_obj=options_obj)

    # Validate the CLI argument schema; proceed accordingly.
    if validate_schema:
        if options_obj.schema is not None:
            schema_path = options_obj.schema
        if schema_path is None:
            msg = (
                "The CLI arguments cannot be validated without a specified "
                "schema. Aborting!!!"
            )
            raise CLIInterfaceError(msg=msg)

        options_dict = __checkschema__(
            options_obj=options_obj, schema_path=schema_path)
        options_obj = parser_interface.dict_toobject(in_dict=options_dict)

    return options_obj
