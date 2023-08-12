# =========================================================================
# File: confs/lua_interface.py
# Author: Henry R. Winterbottom
# Date: 11 August 2023
# Version: 0.0.1
# License: LGPL v2.1
# =========================================================================

"""

"""

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

from utils.logger_interface import Logger
from tools import parser_interface

from typing import Dict

# ----


def __append(lua_str: str) -> str:
    """
    Description
    -----------

    Parameters
    ----------

    Returns
    -------

    lua_str: str

        A Python string containing the respective LUA attribute(s).

    """

    lua_str = lua_str + "\n"

    return lua_str

# ----


def __description(lua_dict: Dict) -> str:
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

    lua_str: str

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
""".format(lua_description=value)
    lua_str = __append(lua_str=lua_str)

    return lua_str

# ---


def __help(lua_dict: Dict) -> str:
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

    lua_str: str

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

    lua_str = """\
-- -*- lua -*-
"""
    lua_str = __append(lua_str=lua_str)

    return lua_str

# ----


def __load(lua_dict: Dict) -> str:
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

    lua_str: str

        A Python string containing the respective LUA attribute(s).

    """

    # Build the LUA `load` attributes.
    lua_str = "-- Load packages and versions.\n"
    load_list = parser_interface.dict_key_value(
        dict_in=lua_dict, key="load", force=True, no_split=True)
    for item in load_list:
        if isinstance(item, str):
            lua_str = lua_str + """\
load(\"{item}\")\n""".format(item=item)
        if isinstance(item, dict):
            for (key, value) in item.items():

                lua_str = lua_str + """\
load(pathJoin(\"{key}\", \"{value}\"))\n""".format(key=key, value=value)
    lua_str = __append(lua_str=lua_str)

    return lua_str


# ----

def __prepend_path(lua_dict: Dict) -> str:
    """ """

    lua_str = "-- Prepend paths.\n"
    prepend_path_dict = parser_interface.dict_key_value(
        dict_in=lua_dict, key="prepend_path", force=True, no_split=True)
    for (prepend_key, prepend_value) in prepend_path_dict.items():
        lua_str = lua_str + "prepend_path(\"{}\", \"{}\")\n".format(
            prepend_key, "\", \"".join(prepend_value))
    lua_str = __append(lua_str=lua_str)

    return lua_str

# ----


def __setenv(lua_dict: Dict) -> str:
    """ """

    lua_str = "-- Environment variables.\n"
    setenv_list = parser_interface.dict_key_value(
        dict_in=lua_dict, key="setenv", force=True, no_split=True)
    for setenv_dict in setenv_list:
        for (setenv_key, setenv_value) in setenv_dict.items():
            lua_str = lua_str + "setenv(\"{}\", \"{}\")\n".format(
                setenv_key, setenv_value)
    lua_str = __append(lua_str=lua_str)

    return lua_str

# ----


def write_lua(lua_dict: Dict, lua_path: str) -> None:
    """

    """

    # TODO: See if this can be better "Pythonized".

    # Build and write the LUA formatted file.
    with open(lua_path, "w", encoding="utf-8") as lua_out:
        lua_str = __initlua()
        if "description" in lua_dict:
            lua_str = lua_str + __description(lua_dict=lua_dict)
        if "help" in lua_dict:
            lua_str = lua_str + __help(lua_dict=lua_dict)
        if "setenv" in lua_dict:
            lua_str = lua_str + __setenv(lua_dict=lua_dict)
        if "prepend_path" in lua_dict:
            lua_str = lua_str + __prepend_path(lua_dict=lua_dict)
        if "setenv" in lua_dict:
            lua_str = lua_str + __setenv(lua_dict=lua_dict)
        if "load" in lua_dict:
            lua_str = lua_str + __load(lua_dict=lua_dict)

        lua_out.write(lua_str)
