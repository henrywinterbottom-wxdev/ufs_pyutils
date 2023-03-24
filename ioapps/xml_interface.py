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

import io
import os
import re
import json

from typing import Dict

from tools import fileio_interface

from lxml import etree
from bs4 import BeautifulSoup as soup
from xml.dom import minidom

import yaml

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

    # Read the XML-formatted file.
    with open(xml_path, "r", encoding="utf-8") as file:
        xml_contents = file.read().replace("&", "__ENTITY__")

    # Define the XML parser object and parse the XML-formatted file
    # contents.
    parser = etree.XMLParser(remove_comments=remove_comments)
    xml_str = minidom.parseString(etree.tostring(
        etree.fromstring(xml_contents, parser))).toprettyxml(indent=5*" ")

    xml_dict = xmltodict.parse(xml_str)

    xml_str = [json.dumps(xml_dict).replace(key, value)
               for (key, value) in {"__ENTITY__": "&"}.items()][0]

    xml_dict = json.loads(xml_str)

    print((xml_dict))
    quit()

    for key in xml_dict:
        #        key = [item for item in {"__ENTITY__": "&"}.keys() if item in key]

        print(key)

    quit()

    # xml_dict[key] = [item for item in {"__ENTITY__": "&"} if

    # print(address)

#    xml_dict = xml_dict.get("__ENTITY__", "&")

    return xml_dict
