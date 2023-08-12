# =========================================================================
# File: confs/lua_interface.py
# Author: Henry R. Winterbottom
# Date: 11 August 2023
# Version: 0.0.1
# License: LGPL v2.1
# =========================================================================

"""
Module
------

    lua_interface.py

Description
-----------

    This module contains functions to build and write LUA User Access
    (LUA) formatted file.

Functions
---------

    
Author(s)
---------

   Henry R. Winterbottom; 12 August 2023

History
-------

   2023-08-12: Henry Winterbottom -- Initial implementation.

"""

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

from utils.logger_interface import Logger
from tools import parser_interface
from tools import datetime_interface
from tools import system_interface

from typing import Dict, Union

# ----


def __append(lua_str: str) -> str:
    """
    Description
    -----------

    This function appends an `end-of-line` to the LUA string specified
    upon entry.

    Parameters
    ----------

    lua_str: str

        A Python string containing the respective LUA attribute(s).

    Returns
    -------

    lua_str: str

        A Python string containing the updated LUA attribute(s)
        string.

    """

    # Append an `end-of-line` to the LUA string.
    lua_str = lua_str + "\n"

    return lua_str

# ----


def __conflict(lua_dict: Dict) -> Union[str, None]:
    """
    Description
    -----------

    This function defines a LUA formatted `conflict` statement(s).

    Parameters
    ----------

    lua_dict: Dict

        A Python dictionary containing the LUA attributes for the
        respective module.

    Returns
    -------

    lua_str: Union[str, None]

        A Python string containing the respective LUA attribute(s).

    """

    # Build the LUA `conflict` attributes.
    try:
        lua_str = "-- Conflict(s).\n"
        conflicts_list = parser_interface.dict_key_value(
            dict_in=lua_dict, key="conflicts", force=True, no_split=True)
        for conflict in conflicts_list:
            lua_str = lua_str + "conflict(\"{}\")\n".format(conflict)
        lua_str = __append(lua_str=lua_str)
    except TypeError:
        return

    return lua_str


# ----


def __description(lua_dict: Dict) -> Union[str, None]:
    """
    Description
    -----------

    This function defines a LUA formatted `description` statement.

    Parameters
    ----------

    lua_dict: Dict

        A Python dictionary containing the LUA attributes for the
        respective module.

    Returns
    -------

    lua_str: Union[str, None]

        A Python string containing the respective LUA attribute(s).

    """

    # Build the LUA `description` attributes.
    value = parser_interface.dict_key_value(
        dict_in=lua_dict, key="description", force=True,
        no_split=True)
    if value is not None:
        lua_str = """\
--
-- {lua_description}
--

local pkgName = myModuleName()
local pkgVersion = myModuleVersion()
local pkgNameVer = myModuleFullName()

whatis("Name: " .. pkgName)
whatis("Version: " ... pkgVersion)
whatis("Description: {lua_description}")
""".format(lua_description=value)
    lua_str = __append(lua_str=lua_str)

    return lua_str

# ---


def __family(lua_dict: Dict) -> Union[str, None]:
    """
    Description
    -----------

    This function defines a LUA formatted `family` statement(s).

    Parameters
    ----------

    lua_dict: Dict

        A Python dictionary containing the LUA attributes for the
        respective module.

    Returns
    -------

    lua_str: Union[str, None]

        A Python string containing the respective LUA attribute(s).

    """

    # Build the LUA `family` attributes.
    try:
        lua_str = "-- Family.\n"
        family_list = parser_interface.dict_key_value(
            dict_in=lua_dict, key="family", force=True, no_split=True)
        for family in family_list:
            lua_str = lua_str + "family(\"{}\")\n".format(family)
        lua_str = __append(lua_str=lua_str)
    except TypeError:
        return

    return lua_str


# ---


def __help(lua_dict: Dict) -> Union[str, None]:
    """
    Description
    -----------

    This function defines a LUA formatted `help` statement.

    Parameters
    ----------

    lua_dict: Dict

        A Python dictionary containing the LUA attributes for the
        respective module.

    Returns
    -------

    lua_str: Union[str, None]

        A Python string containing the respective LUA attribute(s).

    """

    # Build the LUA `help` attributes.
    value = parser_interface.dict_key_value(
        dict_in=lua_dict, key="help", force=True, no_split=True)
    if value is not None:
        lua_str = """\
help([[
{lua_help}
]])
""".format(lua_help=value)
        lua_str = __append(lua_str=lua_str)
    else:
        return

    return lua_str


# ----


def __initlua() -> str:
    """
    Description
    -----------

    This function initializes a LUA formatted statement string.

    Returns
    -------

    lua_str: str

        A Python string containing the initialized LUA statement
        string.

    """

    # Initialize the LUA statement strings accordingly.
    lua_str = """\
-- -*- lua -*-
-- Author: {author}
-- Created: {timestamp}
""".format(timestamp=datetime_interface.current_date(frmttyp="%Y-%m-%d %H:%M:%S",
                                                     is_utc=True), author=system_interface.user())
    lua_str = __append(lua_str=lua_str)

    return lua_str

# ----


def __load(lua_dict: Dict) -> Union[str, None]:
    """
    Description
    -----------

    This function defines the LUA formatted `load` statements.

    Parameters
    ----------

    lua_dict: Dict

        A Python dictionary containing the LUA attributes for the
        respective module.

    Returns
    -------

    lua_str: Union[str,None]

        A Python string containing the respective LUA attribute(s).

    """

    # Build the LUA `load` attributes.
    load_list = parser_interface.dict_key_value(
        dict_in=lua_dict, key="load", force=True, no_split=True)
    if load_list is not None:
        lua_str = "-- Load packages and versions.\n"
        for item in load_list:
            if isinstance(item, str):
                lua_str = lua_str + """\
load(\"{item}\")\n""".format(item=item)
            if isinstance(item, dict):
                for (key, value) in item.items():
                    lua_str = lua_str + """\
load(pathJoin(\"{key}\", \"{value}\"))\n""".format(key=key, value=value)
        lua_str = __append(lua_str=lua_str)
    else:
        return

    return lua_str


# ----

def __prepend_path(lua_dict: Dict) -> Union[str, None]:
    """
    Description
    -----------

    This function defines the LUA formatted `prepend_path` statements.

    Parameters
    ----------

    lua_dict: Dict

        A Python dictionary containing the LUA attributes for the
        respective module.

    Returns
    -------

    lua_str: Union[str, None]

        A Python string containing the respective LUA attribute(s).    

    """

    # Build the LUA `prepend_path` attributes.
    prepend_path_dict = parser_interface.dict_key_value(
        dict_in=lua_dict, key="prepend_path", force=True, no_split=True)
    if prepend_path_dict is not None:
        lua_str = "-- Prepend paths.\n"
        for (prepend_key, prepend_value) in prepend_path_dict.items():
            lua_str = lua_str + "prepend_path(\"{}\", \"{}\")\n".format(
                prepend_key, "\", \"".join(prepend_value))
        lua_str = __append(lua_str=lua_str)
    else:
        return

    return lua_str

# ----


def __setenv(lua_dict: Dict) -> Union[str, None]:
    """ 
    Description
    -----------

    This function defines a LUA formatted `setenv` statement(s).

    Parameters
    ----------

    lua_dict: Dict

        A Python dictionary containing the LUA attributes for the
        respective module.

    Returns
    -------

    lua_str: Union[str, None]

        A Python string containing the respective LUA attribute(s).

    """

    # Build the LUA `setenv` attributes.
    try:
        lua_str = "-- Environment variables.\n"
        setenv_list = parser_interface.dict_key_value(
            dict_in=lua_dict, key="setenv", force=True, no_split=True)
        for setenv_dict in setenv_list:
            for (setenv_key, setenv_value) in setenv_dict.items():
                lua_str = lua_str + "setenv(\"{}\", \"{}\")\n".format(
                    setenv_key, setenv_value)
        lua_str = __append(lua_str=lua_str)
    except TypeError:
        return

    return lua_str

# ----


def write_lua(lua_dict: Dict, lua_path: str) -> None:
    """
    Description
    -----------

    This function builds the LUA-formatted file path.

    Parameters
    ----------

    lua_dict: Dict

        A Python dictionary containing the LUA attributes for the
        respective module.

    lua_path: str

        A Python string specifying the LUA-formatted file path.

    """

    # Build and write the LUA formatted file.
    function_list = [__description(lua_dict=lua_dict),
                     __help(lua_dict=lua_dict),
                     __conflict(lua_dict),
                     __family(lua_dict),
                     __setenv(lua_dict=lua_dict),
                     __prepend_path(lua_dict=lua_dict),
                     __load(lua_dict=lua_dict)
                     ]
    with open(lua_path, "w", encoding="utf-8") as lua_out:
        lua_str = __initlua()
        for function in function_list:
            if function is not None:
                lua_str = lua_str + function
        lua_out.write(lua_str)
