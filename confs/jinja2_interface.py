# =========================================================================

# Module: confs/jinja2_interface.py

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

    jinja2_interface.py

Description
-----------

    This module contains classes and functions to read and write
    Jinja2-formatted files.

Functions
---------

    _fail_missing_vars(tmpl_path, in_dict)

        This function parses the Jinja2-formatted template file and
        the Python dictionary containing the Jinja2 template key and
        value pairs; if a Jinja2-formatted template file variable has
        not been defined (i.e., is missing) a Jinja2InterfaceError
        exception is raised.

    _get_env(tmpl_path)

        This function defines the Jinja2 environment object.

    _get_template(tmpl_path)

        This function defines the Jinja2 environment template object.

    _get_template_file_attrs(tmpl_path)

        This function returns the template file name attributes.

    _get_template_vars(tmpl_path)

        This function collects the template variable names from a
        Jinja2-formatted template file.

    _replace_tmplmarkser(tmpl_path)

        This function replaces specified non-Jinja2-formatted template
        string-values with the respective Jinja2-formatted template
        indicators; the updated template file is written to a
        temporary (e.g., virtual) file path and returned to the
        calling function; the non-Jinja2-formatted template
        string-values are defined bu the `confs/template_interface.py`
        module attribute `TMPL_ITEM_LIST`.

    write_from_template(tmpl_path, output_file, in_dict,
                        fail_missing=False, rpl_tmpl_mrks=False,
                        f90_bool=False)

        This function writes a Jinja2-formatted file established from
        a templated Jinja2-formatted file.

    write_jinja2(jinja2_file, in_dict)

        This function writes a Jinja2 formatted file using the
        specified Python dictionary.

Author(s)
---------

    Henry R. Winterbottom; 27 December 2022

History
-------

    2022-12-27: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=broad-except
# pylint: disable=consider-using-f-string
# pylint: disable=raise-missing-from
# pylint: disable=too-many-arguments

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

import os
from typing import Dict, List, Tuple

from jinja2 import Environment, FileSystemLoader, meta
from tools import fileio_interface, parser_interface
from utils.exceptions_interface import Jinja2InterfaceError
from utils.logger_interface import Logger

from confs.template_interface import TMPL_ITEM_LIST

# ----

# Define all available functions.
__all__ = ["write_from_template", "write_jinja2"]

# ----

logger = Logger()

# ----


def _fail_missing_vars(tmpl_path: str, in_dict: Dict) -> None:
    """
    Description
    -----------

    This function parses the Jinja2-formatted template file and the
    Python dictionary containing the Jinja2 template key and value
    pairs; if a Jinja2-formatted template file variable has not been
    defined (i.e., is missing) a Jinja2InterfaceError exception is
    raised.

    Parameters
    ----------

    tmpl_path: str

        A Python string defining the path to the Jinja2-formatted
        template file.

    in_dict: Dict

        A Python dictionary containing the Jinja2 template key and
        value pairs.

    Raises
    ------

    Jinja2InterfaceError:

        - raised if variables within the Jinja2-formatted template
          file have not been specified within the Python dictionary
          containing the Jinja2-formatted file template variable key
          and value pairs (in_dict).

    """

    # Check that the Python dictionary is not empty; proceed
    # accordingly.
    if not in_dict:
        msg = "The Python dictionary provided upon entry is empty. Aborting!!!"
        raise Jinja2InterfaceError(msg=msg)

    # Collect the variables within the Jinja2-formatted template file.
    variables = _get_template_vars(tmpl_path=tmpl_path)

    # If variables are collected, check again by search for the
    # Jinja2-formatted template variables; proceed accordingly.
    if len(variables) == 0:

        # Initialize the variables.
        variables = []

        start_str = "{{"
        stop_str = "}}"

        # Collect all data from the Jinja2-formatted file.
        with open(tmpl_path, "r", encoding="utf-8") as file:
            data = file.read().split("\n")

        # Search for Jinja2-formatted template variables; proceed
        # accordingly; ignoring template variable with default values.
        for item in data:
            if (start_str and stop_str in item) and ("or" not in item):

                start = item.index(start_str)
                stop = item.index(stop_str)

                string = (item[start + len(start_str): stop].rstrip()).lstrip()
                variables.append(string)

    # Build the list of attribute variables.
    compare_variables = []
    for item in list(in_dict):
        if isinstance(item, tuple):
            compare_variables.append(item[0])
        else:
            compare_variables.append(item)

    # Compare the respective variable lists and find unique (i.e.,
    # missing variables).
    missing_vars = [
        variable for variable in variables if variable not in compare_variables
    ]

    # If Jinja2-formatted template file variables have not been
    # defined, proceed accordingly.
    if len(missing_vars) != 0:
        msg = (
            "The following variables have not been defined within the "
            f"Jinja2-formatted template file {tmpl_path}:\n"
        )
        for missing_var in missing_vars:
            msg = msg + f"{missing_var}\n"

        msg = msg + "Aborting!!!"
        raise Jinja2InterfaceError(msg=msg)


# ----


def _get_env(tmpl_path: str) -> object:
    """
    Description
    -----------

    This function defines the Jinja2 environment object.

    Parameters
    ----------

    tmpl_path: str

        A Python string defining the path to the Jinja2-formatted
        template file.

    Returns
    -------

    env: object

        A Python object containing the Jinja2 environment.

    """

    # Collect the Jinja2-formatted template file attributes.
    (dirname, _) = _get_template_file_attrs(tmpl_path=tmpl_path)

    # Establish the Jinja2 environment.
    env = Environment(loader=FileSystemLoader(searchpath=dirname))

    return env


# ----


def _get_template(tmpl_path: str) -> object:
    """
    Description
    -----------

    This function defines the Jinja2 environment template object.

    Parameters
    ----------

    tmpl_path: str

        A Python string defining the path to the Jinja2-formatted
        template file.

    Returns
    -------

    tmpl: object

        A Python object containing the Jinja2 environment template
        object.

    """

    # Collect the Jinja2-formatted template file attributes.
    (_, basename) = _get_template_file_attrs(tmpl_path=tmpl_path)

    # Establish the Jinja2 environment.
    env = _get_env(tmpl_path=tmpl_path)

    # Define the Jinja2-formatted template.
    tmpl = env.get_template(basename)

    return tmpl


# ----


def _get_template_file_attrs(tmpl_path: str) -> Tuple[str, str]:
    """
    Description
    -----------

    This function returns the template file name attributes.

    Parameters
    ----------

    tmpl_path: str

        A Python string defining the path to the Jinja2-formatted
        template file.

    Returns
    -------

    dirname: str

        A Python string specifying the directory tree path within for
        the Jinja2 templated file define upon entry.

    basename: str

        A Python string specifying the base-filename for the Jinja2
        templated file path defined upon entry.

    """

    # Collect the Jinja2-formatted template file attributes.
    (dirname, basename) = [os.path.dirname(
        tmpl_path), os.path.basename(tmpl_path)]

    return (dirname, basename)


# ----


def _get_template_vars(tmpl_path: str) -> List:
    """
    Description
    -----------

    This function collects the template variable names from a
    Jinja2-formatted template file.

    Parameters
    ----------

    tmpl_path: str

        A Python string defining the path to the Jinja2-formatted
        template file.

    Returns
    -------

    variables: List

        A Python list of Jinja2-formatted template file variables.

    """

    # Define the Jinja2 templating attributes.
    env = _get_env(tmpl_path=tmpl_path)
    tmpl = _get_template(tmpl_path=tmpl_path)

    # Collect the templated variable names.
    variables = list(meta.find_undeclared_variables(env.parse(tmpl)))

    return variables


# ----


def _replace_tmplmarkers(tmpl_path: str) -> str:
    """
    Description
    -----------

    This function replaces specified non-Jinja2-formatted template
    string-values with the respective Jinja2-formatted template
    indicators; the updated template file is written to a temporary
    (e.g., virtual) file path and returned to the calling function;
    the non-Jinja2-formatted template string-values are defined bu the
    `confs/template_interface.py` module attribute `TMPL_ITEM_LIST`.

    Parameters
    ----------

    tmpl_path: str

        A Python string defining the path to the template file
        containing non-Jinja2-formatted template string-values.

    Returns
    -------

    virtfile: str

        A Python string defining the path to the temporary (i.e.,
        virtual) file path containing the Jinja2-formatted template
        defined from the attributes contained within `tmpl_path` upon
        entry.

    """

    # Read the non-Jinja2-formatted template file.
    with open(tmpl_path, "r", encoding="utf-8") as file:
        inputs = file.read().split("\n")

    # Parse the contents of the non-Jinja2-formatted template file;
    # update any encountered non-Jinja2-formatted template
    # string-values with the appropriate Jinja2-formatted template
    # string-values.
    virtfile = fileio_interface.virtual_file().name

    with open(virtfile, "w", encoding="utf-8") as file:
        for string in inputs:
            for item in TMPL_ITEM_LIST:
                tmplstr = item.split("%s")

                if (tmplstr[0] in string) and (tmplstr[1] in string):
                    string = string.replace(tmplstr[0].strip(), "{{ ")
                    string = string.replace(tmplstr[1].strip(), " }}")
                    break

            file.write(f"{string}\n")

    return virtfile


# ----


def write_from_template(
    tmpl_path: str,
    output_file: str,
    in_dict: Dict,
    fail_missing: bool = False,
    rpl_tmpl_mrks: bool = False,
    f90_bool: bool = False,
) -> None:
    """
    Description
    -----------

    This function writes a Jinja2-formatted file established from a
    templated Jinja2-formatted file.

    Parameters
    ----------

    tmpl_path: str

        A Python string defining the path to the Jinja2-formatted
        template file.

    output_file: str

        A Python string containing the full-path to the
        Jinja2-formatted file to be written.

    in_dict: Dict

        A Python dictionary containing the Jinja2-formatted file
        template variable key and value pairs.

    Keywords
    --------

    fail_missing: bool, optional

        A Python boolean valued variable specifying whether to fail if
        variables within the Jinja2-formatted template file have not
        been specified within the Python dictionary containing the
        Jinja2-formatted file template variable key and value pairs
        (in_dict).

    rpl_tmpl_mrks: bool, optional

        A Python boolean valued variable specifying whether to replace
        any pre-defined template markers (see
        `confs/template_interface.py`, prior to populating the
        Jinja2-formatted template.

    f90_bool: bool

        A Python boolean valued variable specifying whether to
        transform boolean variables to a FORTRAN 90 format.

    Raises
    ------

    Jinja2InterfaceError:

        - raised if an exception is encountered while writing the
          Jinja2-formatted file.

    """

    if rpl_tmpl_mrks:
        tmpl_path = _replace_tmplmarkers(tmpl_path=tmpl_path)

    if fail_missing:
        _fail_missing_vars(tmpl_path=tmpl_path, in_dict=in_dict)

    if f90_bool:
        for (key, value) in in_dict.items():
            in_dict[key] = parser_interface.f90_bool(value)

    # Open the Jinja2-formatted template file, update the Jinja2
    # template variable(s), and write the results to the output file
    # path.
    try:
        tmpl = _get_template(tmpl_path=tmpl_path)

        print(vars(tmpl))
        quit()

        with open(output_file, "w", encoding="utf-8") as file:
            file.write(tmpl.render(in_dict, env=os.environ))

    except Exception as errmsg:
        msg = (
            f"Rendering Jinja2-formatted file {output_file} failed with "
            f"error {errmsg}. Aborting!!!"
        )
        raise Jinja2InterfaceError(msg=msg)

    if rpl_tmpl_mrks:
        os.unlink(tmpl_path)


# ----


def write_jinja2(jinja2_file: str, in_dict: Dict) -> None:
    """
    Description
    -----------

    This function writes a Jinja2-formatted file using the specified
    Python dictionary.

    Parameters
    ----------

    jinja2_file: str

        A Python string containing the full-path to the
        Jinja2-formatted file to be written.

    in_dict: Dict

        A Python dictionary containing the attributes to be written to
        the Jinja2 file.

    Raises
    ------

    Jinja2InterfaceError:

        - raised if an exception is encountered while writing the
          Jinja2-formatted file.

    """

    # Open and write the dictionary contents to the specified
    # Jinja2-formatted file path; proceed accordingly.
    msg = f"Writing Jinja2 formatted file {jinja2_file}."
    logger.info(msg=msg)

    try:
        with open(jinja2_file, "w", encoding="utf-8") as file:
            file.write("#!Jinja2\n")
            for key in in_dict.keys():
                value = in_dict[key]

                if isinstance(value, str):
                    string = f'set {key} = "{value}"'
                else:
                    string = f"set {key} = {value}"

                file.write("{%% %s %%}\n" % string)

    except Exception as errmsg:
        msg = f"Writing Jinja2-formatted file {jinja2_file} failed with error {errmsg}. Aborting!!!"
        raise Jinja2InterfaceError(msg=msg)
