# =========================================================================

# Module: ioapps/xml_interface.py

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

    xml_interface.py

Description
-----------

    This module contains functions to read and write Extensible Markup
    Language (XML) formatted files.

Functions
---------

    read_xml(xml_path)

        This function parses an XML-formatted file and returns the
        contents of the file formatted as a Python dictionary.

Requirements
------------

- lxml; https://github.com/lxml/lxml

- xmltodict; https://github.com/martinblech/xmltodict

Author(s)
---------

    Henry R. Winterbottom; 24 March 2023

History
-------

    2023-03-24: Henry Winterbottom -- Initial implementation.

"""

# ----

import json
from typing import Dict
from xml.dom import minidom
import yaml
from yaml import SafeLoader

import xmltodict
from lxml import etree
from tools import fileio_interface
from utils.exceptions_interface import XMLInterfaceError
from utils.logger_interface import Logger

# ----

# Define all available functions.
__all__ = ["read_xml"]

# ----

logger = Logger()

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

XML_CHAR_DICT = {"__ENTITY__": "&"}

# ----


def read_xml(xml_path: str, remove_comments: bool = False) -> Dict:
    """
    Description
    -----------

    This function parses an XML-formatted file and returns the
    contents of the file formatted as a Python dictionary.

    Parameters
    ----------

    xml_path: str

        A Python string specifying the path to the XML-formatted file
        to be read.

    Keywords
    --------

    remove_comments: bool, optional

        A Python boolean valued variable specifying whether to include
        XML-formatted comment strings when parsing the XML-formatted
        file.

    Returns
    -------

    xml_dict: dict

        A Python dictionary containing the contents of the
        XML-formatted file path `xml_path`.

    Raises
    ------

    XMLInterfaceError:

        * raised if the XML-formatted file path does not exist.

        * raised if an exception is encountered while reading the
          XML-formatted file path.

        * raised if an exception is encountered while replacing any
          defined special characters in the XML-formatted file path
          contents.

        * raised if an exception is encountered while parsing and
          defining the Python dictionary containing the contents of
          the XML-formatted file path specified upon entry
          (`xml_path`).

        * raised if an exception is encountered while creating a
          Python dictionary from the formatted contents of the
          XML-formatted file path specified upon entry (`xml_path`).

    """

    # Read the XML-formatted file; proceed accordingly.
    exist = fileio_interface.fileexist(path=xml_path)
    if not exist:
        msg = f"The XML-formatted file path {xml_path} does not exist. Aborting!!!"
        raise XMLInterfaceError(msg=msg)

    # Read the XML-formatted file; proceed accordingly.
    try:
        with open(xml_path, "r", encoding="utf-8") as file:
            xml_contents_in = file.read()

    except Exception as errmsg:
        msg = (
            f"Reading XML-formatted file path {xml_path} failed with error "
            f"{errmsg}. Aborting!!!"
        )
        raise XMLInterfaceError(msg=msg) from errmsg

    # Replace any defined special character strings; proceed
    # accordingly.
    try:
        xml_contents_out = xml_contents_in
        for (key, value) in XML_CHAR_DICT.items():
            xml_contents_out = xml_contents_in.replace(value, key)

    except Exception as errmsg:
        msg = (
            f"Replacing special characters {XML_CHAR_DICT.items()[1]} "
            f"failed with error {errmsg}. Aborting!!!"
        )
        raise XMLInterfaceError(msg=msg) from errmsg

    # Define the XML parser object and define the XML-formatted
    # string; proceed accordingly.
    try:
        parser = etree.XMLParser(remove_comments=remove_comments)
        xml_str = minidom.parseString(
            etree.tostring(etree.fromstring(xml_contents_out, parser))
        ).toprettyxml(indent=5 * " ")

        # Define the Python dictionary containing the XML contents.
        xml_dict = xmltodict.parse(xml_str)

    except Exception as errmsg:
        msg = (
            f"Parsing XML-formatted file path {xml_path} contents failed with "
            f"error {errmsg}. Aborting!!!"
        )
        raise XMLInterfaceError(msg=msg) from errmsg

    # Update (e.g., replace) any special character strings.
    try:

        xml_str_in = xmltodict.unparse(xml_dict)
        xml_str_out = xml_str_in
        for (key, value) in XML_CHAR_DICT.items():
            xml_str_out = xml_str_in.replace(key, value)

        parser = etree.XMLParser(resolve_entities=False)
        xml_str = minidom.parseString(
            etree.tostring(etree.fromstring(xml_str_out.encode(), parser))).toprettyxml(indent=5 * " ")

        # , Loader=SafeLoader)
        # xml_dict = xmltodict.parse(xml_str_out)

        # print(type(xml_dict))
        # quit()

        # print(xml_dict)

#        yaml_dict = xmltodict.parse(xml_str_out)
#        quit()

        # print(yaml_dict)
        quit()

    except Exception as errmsg:
        msg = (
            f"Defining a Python dictionary from the contents of XML-formatted "
            f"file path {xml_path} failed with error {errmsg}. Aborting!!!"
        )
        raise XMLInterfaceError(msg=msg) from errmsg

    return xml_dict
