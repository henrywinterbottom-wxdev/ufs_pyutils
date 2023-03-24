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


"""

# ----

import os

from typing import Dict

from tools import fileio_interface

from lxml import etree
from bs4 import BeautifulSoup
from xml.dom import minidom

import xmltodict

from utils.exceptions_interface import XMLInterfaceError


# ----

def read_xml(xml_path: str, remove_comments: bool = False,
             resolve_entities: bool = True) -> Dict:
    """
    Description
    -----------

    This function parses an XML-formatted file and returns the
    contents of the file formatted as a Python Dictionary.

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

    resolve_entities: bool, optional

        A Python boolean valued variable specifying whether to expand
        any entity references with the XML-formatted file path (if
        applicable).

    Returns
    -------

    xml_dict: dict

        A Python dictionary containing the contents of the
        XML-formatted file path `xml_path`.

    """

    # Read the XML-formatted file; proceed accordingly.
    exist = fileio_interface.fileexist(path=xml_path)
    if not exist:
        msg = f"The XML-formatted file path {xml_path} does not exist. Aborting!!!"
        raise XMLInterfaceError(msg=msg)

    with open(xml_path, "r", encoding="utf-8") as file:

        if resolve_entities:
            xml_contents = file.read()

        if not resolve_entities:
            xml_contents = file.read().replace("&amp;", "&amp;amp;")

        # Define the XML parser object.
        parser = etree.XMLParser(resolve_entities=resolve_entities,
                                 attribute_defaults=attribute_defaults,
                                 remove_comments=remove_comments,
                                 remove_pis=remove_pis)

    # Read the XML-formatted file.
    xmlstr = minidom.parseString(etree.tostring(
        etree.fromstring(xml_contents, parser))).toprettyxml(indent=5*" ")

    xml_dict = xmltodict.parse(xmlstr)

    return xml_dict
