# =========================================================================

# Module: confs/template_interface.py

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

    template_interface.py

Description
-----------

    This module contains the base-class object for all file template
    rendering.

Classes
-------

    Template()

        This is the base-class object for all file template rendering.

Author(s)
---------

    Henry R. Winterbottom; 19 April 2023

History
-------

    2023-04-19: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=too-many-arguments

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# -----

from typing import Any, Dict

from tools import parser_interface
from utils.decorator_interface import privatemethod
from utils.exceptions_interface import TemplateInterfaceError
from utils.logger_interface import Logger

# -----

TMPL_ITEM_LIST = ["[@%s]", "{@%s}", "{%%%s%%}", "{{%% %s %%}}", "<%s>",
                  "{%% %s %%}", "{{ %s }}"]

# ----


class Template:
    """
    Description
    -----------

    This is the base-class object for all file template rendering.

    """

    def __init__(self: object):
        """
        Description
        -----------

        Creates a new Template object.

        """

        # Define the base-class attributes.
        self.logger = Logger()

    @staticmethod
    def f90_bool(value: Any) -> Any:
        """
        Description
        -----------

        This method will transform boolean type values to a FORTRAN 90
        boolean format; if the variable `value` specified upon entry
        is not of boolean format the value is return unaltered.

        Parameters
        ----------

        value: Any

            A Python variable to be evaluated as a boolean type value;
            if a boolean type the corresponding value is returned as a
            FORTRAN 90 boolean format.

        Returns
        -------

        value: Any

            An evaluated Python variable; if `value` was boolean type
            upon entry the returned value is of FORTRAN 90 boolean
            format; if not, the unaltered input value is returned.

        """

        # Check the type for the respective input value; proceed
        # accordingly.
        if isinstance(value, bool):
            if value:
                value = "T"
            if not value:
                value = "F"

        return value

    def read_tmpl(self: object, tmpl_path: str) -> str:
        """
        Description
        -----------

        This method reads a template file path and returns a Python
        string containing the attributes collected from the file.

        Parameters
        ----------

        tmpl_path: str

            A Python string defining the template file path.

        Returns
        -------

        tmpl_str_in: str

            A Python string containing the attributes collected from
            the template file path.

        """

        # Read and return the attributes within the template file
        # path.
        with open(tmpl_path, "r", encoding="utf-8") as file:
            tmpl_str = file.read().split("\n")
        tmpl_str_in = " ".join([f"{item}\n" for item in tmpl_str])

        return tmpl_str_in

    @privatemethod
    def render_tmpl(
        self: object,
        tmpl_obj: object,
        tmpl_str_in: str,
        fail_missing: bool,
        f90_bool: bool,
    ) -> str:
        """
        Description
        -----------

        This method renders a Python template string using the
        attributes specified in `tmpl_obj` upon entry and returns a
        Python string updated accordingly.

        Parameters
        ----------

        tmpl_obj: object

            A Python object containing the template attributes.

        tmpl_str_in: str

            A Python string containing template characters.

        fail_missing: bool

            A Python boolean valued variable specifying whether to
            fail if a template string cannot be fully rendered.

        f90_bool: bool

            A Python boolean valued variable specifying whether to
            transform boolean variables to a FORTRAN 90 format.

        Returns
        -------

        tmpl_str_out: str

            A Python string for which template characters have been
            rendered and otherwise identical to `tmpl_str_in`.

        Raises
        ------

        TemplateInterfaceError

            - raised if a template string has not been rendered and
              `fail_missing` is `True` upon entry.

        """

        # Initialize the output string.
        tmpl_str_out = tmpl_str_in

        # Replace any instances of templated strings with specified
        # attributes accordingly.
        for (attr_key, attr_value) in vars(tmpl_obj).items():
            for tmpl_item in TMPL_ITEM_LIST:

                try:
                    check_str = tmpl_item % attr_key
                    value = parser_interface.dict_key_value(
                        dict_in=vars(tmpl_obj), key=attr_key, force=True, no_split=True
                    )

                    # Update value accordingly.
                    if value is not None:
                        if f90_bool:
                            value = self.f90_bool(value=value)
                        attr_value = value

                        tmpl_str_out = tmpl_str_out.replace(
                            check_str, str(attr_value))

                except TypeError:
                    pass

        # Define all characters that represent templated values.
        tmpl_char_list = set(
            list("".join([item.replace("%s", "") for item in TMPL_ITEM_LIST]))
        )

        tmpl_char_list = [item for item in tmpl_char_list if item != " "]

        # Check whether any templated strings remain; proceed
        # accordingly.
        tmpl_str_list = []
        for tmpl_str in tmpl_str_out.split("\n"):
            if any(item for item in tmpl_char_list if item in tmpl_str):
                tmpl_str_list.append(tmpl_str.strip())

        msg = (
            "The following template(s) was (were) not rendered: "
            f"{', '.join(tmpl_str_list)}."
        )

        if (len(tmpl_str_list) > 0):
            if fail_missing:
                msg = msg + " Aborting!!!"
                raise TemplateInterfaceError(msg=msg)

            if not fail_missing:
                self.logger.warn(msg=msg)

        return tmpl_str_out

    @privatemethod
    def tmpl_obj(self: object, attr_dict: Dict) -> object:
        """
        Description
        -----------

        This method builds a Python object containing the attributes
        within the Python dictionary `attr_dict` upon entry.

        Parameters
        ----------

        attr_dict: Dict

            A Python dictionary containing the attributes to be used
            for updating a specified template.

        Returns
        -------

        tmpl_obj: object

            A Python object containing the template attributes
            provided by `attr_dict` upon entry and cast as an object.

        """

        # Collect the attributes within the Python dictionary provided
        # upon entry and builds a Python object.
        tmpl_obj = parser_interface.object_define()
        for attr in attr_dict.keys():
            value = parser_interface.dict_key_value(
                dict_in=attr_dict, key=attr, no_split=True
            )

            tmpl_obj = parser_interface.object_setattr(
                object_in=tmpl_obj, key=attr, value=value
            )

        return tmpl_obj

    def write_tmpl(
        self: object,
        attr_dict: Dict,
        tmpl_path: str,
        template_path: str,
        fail_missing: bool = False,
        f90_bool: bool = False,
    ) -> None:
        """
        Description
        -----------

        This method collects attribute values, renders a string
        containing template attributes, and writes the updated
        template to a specified file path `tmpl_path`.

        Parameters
        ----------

        attr_dict: Dict

            A Python dictionary containing the attributes to be used
            for updating a specified template.

        tmpl_path: str

            A Python string specifying the rendered (e.g., output)
            file path.

        template_path: str

            A Python string specifying the template file path to be
            rendered.

        Keywords
        --------

        fail_missing: bool, optional

            A Python boolean valued variable specifying whether to
            fail if a template string cannot be fully rendered.

        f90_bool: bool, optional

            A Python boolean valued variable specifying whether to
            transform boolean variables to a FORTRAN 90 format.

        """

        # Collect the attributes to render the template.
        tmpl_obj = self.tmpl_obj(attr_dict=attr_dict)

        # Read and render the template file.
        tmpl_str_in = self.read_tmpl(tmpl_path=template_path)

        tmpl_str_out = self.render_tmpl(
            tmpl_obj=tmpl_obj,
            tmpl_str_in=tmpl_str_in,
            fail_missing=fail_missing,
            f90_bool=f90_bool,
        )

        # Write out the template.
        with open(tmpl_path, "w", encoding="utf-8") as file:
            for item in tmpl_str_out.split("\n"):
                file.write(f"{item.strip()}\n")
