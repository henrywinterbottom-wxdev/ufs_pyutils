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

    write_xml(xml_path, xml_dict, doc_name:, dtd_path, indent = 5)

        This function writes a XML-formatted file `xml_path`
        containing the attributes within the Python dictionary
        `xml_dict` and the attributes defined by `doc_name` and
        `dtd_path`.

Example
-------

    The following example describes the document type/name and entity
    attribute resolutions.

    <!DOCTYPE doc_name SYSTEM dtd_path>

    In the above example, `doc_name` is the name of the XML-document;
    note that this may be different than the XML-formatted file path
    `xml_path. For example, a name of `workflow` would result in the
    string constructed as follows.

    <!DOCTYPE workflow SYSTEM dtd_path>

    The `dtd_path` attributes is a string specifying the full-path to
    the file path containing the entities and their corresponding
    values. For the example above, a `dtd_path` value of
    /path/to/dtd/file would result in the string constructed as
    follows.

    <!DOCTYPE workflow SYSTEM "/path/to/dtd/file">

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

from typing import Dict
from xml.dom import minidom

import xmltodict
from lxml import etree
from tools import fileio_interface, parser_interface
from utils.exceptions_interface import XMLInterfaceError
from utils.logger_interface import Logger

# ----

# Define all available functions.
__all__ = ["read_xml", "write_xml"]

# ----

logger = Logger()

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

# Define the substitution value Python dictionary for reading
# XML-formatted files.
XML_SCHAR_DICT = {
    "__ENTITY__": "&",
}

# Define the Python dictionary containing the special symbols (keys)
# and their substitution values (values).
XML_SSYMS_DICT = {
    "&amp;": "&",
}

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
    msg = f"Reading XML-formatted file path {xml_path}."
    logger.info(msg=msg)

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
        for (key, value) in XML_SCHAR_DICT.items():
            xml_contents_out = xml_contents_in.replace(value, key)

    except Exception as errmsg:
        msg = (
            f"Replacing special characters {XML_SCHAR_DICT.items()[1]} "
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

        xml_str = xmltodict.unparse(xml_dict)
        xml_str = minidom.parseString(xml_str).toprettyxml(indent=5 * " ")

        xml_dict = xmltodict.parse(xml_str)

        for (key, value) in XML_SCHAR_DICT.items():
            xml_dict = parser_interface.dict_replace_value(
                in_dict=xml_dict, old=f"{key}", new=f"{value}"
            )

    except Exception as errmsg:
        msg = (
            f"Defining a Python dictionary from the contents of XML-formatted "
            f"file path {xml_path} failed with error {errmsg}. Aborting!!!"
        )
        raise XMLInterfaceError(msg=msg) from errmsg

    return xml_dict


# ----


def write_xml(
    xml_path: str, xml_dict: Dict, doc_name: str, dtd_path: str, indent: int = 5
) -> None:
    """
    Description
    -----------

    This function writes a XML-formatted file `xml_path` containing
    the attributes within the Python dictionary `xml_dict` and the
    attributes defined by `doc_name` and `dtd_path`.

    Parameters
    ----------

    xml_path: str

        A Python string specifying the path to the XML-formatted file
        to be written.

    xml_dict: dict

        A Python dictionary containing the XML-attributes to be
        written to file path `xml_path`.

    doc_name: str

        A Python string defining the XML-formatted document name; see
        the example in the module documentation (above).

    dtd_path: str

        A Python string specifying the path to the document type
        definition (DTD) formatted file; this file contains the
        reference attributes to be resolved within the final
        XML-formatted file path; additional information regarding
        DTD-formatted files can be found here
        https://tinyurl.com/xml-dtd-example.

    Keywords
    --------

    indent: int, optional

        A Python integer specifying the total number of spaces for
        indenting when formatting the output XML-formatted file path
        `xml_path`.

    Raises
    ------

    XMLInterfaceError:

        * raised if an exception is encountered while building the
          output XML-formatted file path `xml_path`.

    """

    # Build the XML-formatted document string; this includes the path
    # to the DTD-formatted file.
    doctype = f"<!DOCTYPE {doc_name} SYSTEM '{dtd_path}'>"

    # Build the XML-formatted string from the Python dictionary
    # `xml_dict` specified upon entry; proceed accordingly.
    xml_str = xmltodict.unparse(xml_dict)
    xml_str = minidom.parseString(xml_str).toprettyxml(indent=indent * " ")

    for (key, value) in XML_SSYMS_DICT.items():
        msg = f"Replacing XML-formatted string symbol {key} with {value}."
        logger.info(msg=msg)
        xml_str = xml_str.replace(f"{key}", f"{value}")

    # Update the script acccordingly; this step is necessary due to
    # the order of operations related to parsing Python dictionaries
    # and constructing XML-formatted files.
    xml_str = doctype + xml_str.replace('<?xml version="1.0" ?>', "").replace(
        '<?xml version="1.0"?>', ""
    )
    xml_str = '<?xml version="1.0" ?>\n' + xml_str

    # Parse the XML-formatted file attributes; update (e.g., resolve)
    # the XML entities and write the XML-formatted file; proceed
    # accordingly.
    msg = "Parsing the XML-formatted attributes and resolving entities."
    logger.info(msg=msg)

    try:
        parser = etree.XMLParser(load_dtd=True, resolve_entities=True)
        tree = etree.XML(xml_str, parser=parser)

        xml_str = etree.tostring(tree, xml_declaration=True, doctype=doctype)
        xml_str = minidom.parseString(xml_str).toprettyxml(
            indent=indent * " ", newl="")

        msg = f"Writing XML-formatted file path {xml_path}."
        logger.info(msg=msg)

        with open(xml_path, "w", encoding="utf-8") as file:
            file.write(xml_str)

    except Exception as errmsg:
        msg = (
            f"Writing XML-formatted file path {xml_path} failed with "
            f"error {errmsg}. Aborting!!!"
        )
        raise XMLInterfaceError(msg=msg) from errmsg
