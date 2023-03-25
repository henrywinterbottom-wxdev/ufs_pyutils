# =========================================================================

# Module: ioapps/tcvitals_interface.py

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

    tcvitals_interface.py

Description
-----------

    This module contains functions to read and write TC-vitals
    records.

Functions
---------

    __scalegeo__(lat, lon)

        This function scales the geographical location coordinates for
        the TC-vitals record according.

    __scaleintns__(mslp, vmax)

        This function scales the minimum sea-level pressure (`mslp`)
        and maximum wind speed (`vmax`) intensity values to their
        corresponding MKS units.

    __scalesize__(poci, rmw, roci)

        This function scales the tropical cyclone size metric values
        to their corresponding MKS units.

    read_tcvfile(filepath)

        This function reads a TC-vitals formatted file and returns a
        Python object containing the TC-vitals attributes for all
        records within the filepath.

    scale_tcvrec(tcv_dict)

        This function scales the relavant tropical cyclone records to
        their respective MKS representations and returns a Python
        object containing the respective scaled values.

    write_tcvfile(filepath, tcvstr)

        This function writes a user-specified TC-vitals record(s) to a
        specified filepath.

    write_tcvstr(tcvit_obj)

        This function writes a string formatted in accordance with the
        TC-vitals format.

Author(s)
---------

    Henry R. Winterbottom; 03 December 2022

History
-------

    2022-12-02: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=consider-using-f-string

# ----


from collections import OrderedDict
from typing import Dict, Tuple

import numpy
from tools import parser_interface
from utils import constants_interface
from utils.constants_interface import hPa2Pa, kn2m
from utils.exceptions_interface import TCVitalsInterfaceError
from utils.logger_interface import Logger

# ----

# Define all available functions.
__all__ = ["read_tcvfile", "scale_tcvrec", "write_tcvfile", "write_tcvstr"]

# ----

logger = Logger()

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

TCV_34QUAD_DICT = OrderedDict(
    {
        "tcv_center": {"idx": 0, "spval": None},
        "tcid": {"idx": 1, "spval": None},
        "event_name": {"idx": 2, "spval": None},
        "time_ymd": {"idx": 3, "spval": None},
        "time_hm": {"idx": 4, "spval": None},
        "lat": {"idx": 5, "spval": None},
        "lon": {"idx": 6, "spval": None},
        "stormdir": {"idx": 7, "spval": "-99"},
        "stormspeed": {"idx": 8, "spval": "-99"},
        "mslp": {"idx": 9, "spval": None},
        "poci": {"idx": 10, "spval": "-999"},
        "roci": {"idx": 11, "spval": "-999"},
        "vmax": {"idx": 12, "spval": None},
        "rmw": {"idx": 13, "spval": "-99"},
        "NE34": {"idx": 14, "spval": "-999"},
        "SE34": {"idx": 15, "spval": "-999"},
        "SW34": {"idx": 16, "spval": "-999"},
        "NW34": {"idx": 17, "spval": "-999"},
        "stormdepth": {"idx": 18, "spval": "X"},
    }
)

# ----


def __scalegeo__(lat: str, lon: str) -> Tuple[float, float]:
    """
    Description
    -----------

    This function scales the geographical location coordinates for the
    TC-vitals record according.

    Parameters
    ----------

    lat: str

        A Python string defining the geographical location latitude
        coordinate for the respective TC-vitals record.

    lon: str

        A Python string defining the geographical location longitude
        coordinate for the respective TC-vitals record.

    Returns
    -------

    lat_out: float

        A Python float value defining the scaled geographical location
        latitude coordinate; units are degrees.

    lon_out: float

        A Python float value defining the scaled geographical location
        longitude coordinate; units are degrees.

    """

    # Initialize the respective TC-vitals attribute variables.
    (lat_in, lon_in) = (lat, lon)

    # Define the scaling values accordingly.
    (lat_scale, lon_scale) = [1.0 / 10.0 for idx in range(2)]

    if "S" in lat_in:
        lat_scale = -1.0 / 10.0

    if "E" in lon_in:
        lon_scale = -1.0 / 10.0

    # Rescale the geographical location values.
    lat_out = lat_scale * int(lat_in[:-1])
    lon_out = lon_scale * int(lon_in[:-1])

    return (lat_out, lon_out)


# ----


def __scaleintns__(mslp: str, vmax: str) -> Tuple[float, float]:
    """
    Description
    -----------

    This function scales the minimum sea-level pressure (`mslp`) and
    maximum wind speed (`vmax`) intensity values to their
    corresponding MKS units.

    Parameters
    ----------

    mslp: str

        A Python string defining the minimum sea-level pressure value.

    vmax: str

        A Python string defining the maximum wind speed intensity
        value.

    Returns
    -------

    mslp_out: float

        A Python float value defining the formatted minimum sea-level
        pressure value; units are Pascals.

    vmax_out: float

        A Python float value defining the formatted maxmimum wind
        speed value; units are meters per second.

    """

    # Initialize the respective TC-vitals attribute variables.
    (mslp_in, vmax_in) = (mslp, vmax)

    # Scale the values accordingly.
    mslp_out = int(mslp_in) * hPa2Pa
    vmax_out = float(vmax_in)

    return (mslp_out, vmax_out)


# ----


def __scalesize__(poci: str, rmw: str, roci: str) -> Tuple[float, float, float]:
    """
    Description
    -----------

    This function scales the tropical cyclone size metric values to
    their corresponding MKS units.

    Parameters
    ----------

    poci: str

        A Python string defining the pressure of the outer-most closed
        isobar relative to the respective TC event.

    rmw: str

        A Python string defining the radius of maximum wind speed
        relative to the respective TC event.

    roci: str

        A Python string defining the radius of the outer-most closed
        isobar relative to the respective TC event.

    Returns
    -------

    poci_out: float

        A Python float value defining the pressure of the outer-most
        closed isobar; units are Pascals; if NoneType upon entry,
        NoneType is returned.

    rmw_out: float

        A Python float value defining the radius of maximum winds;
        units are meters; if NoneType upon entry, NoneType is
        returned.

    roci_out: float

        A Python float value defining the radius of the outer-most
        closed isobar; units are meters; if NoneType upon entry,
        NoneType is returned.

    """

    # Initialize the respective TC-vitals attribute variables.
    (poci_in, rmw_in, roci_in) = (poci, rmw, roci)
    (poci_out, rmw_out, roci_out) = [None for idx in range(3)]

    # Scale the values accordingly.
    if poci_in is not None:
        poci_out = int(poci_in) * hPa2Pa

    if rmw_in is not None:
        rmw_out = int(rmw_in) * kn2m

    if roci_in is not None:
        roci_out = int(roci_in) * kn2m

    return (poci_out, rmw_out, roci_out)


# ----


def read_tcvfile(filepath: str) -> object:
    """
    Description
    -----------

    This function reads a TC-vitals formatted file and returns a
    Python object containing the TC-vitals attributes for all records
    within the filepath.

    Parameters
    ----------

    filepath: str

        A Python string specifying the file path for the TC-vitals
        formatted file.

    Returns
    -------

    tcvobj: object

        A Python object containing the attributes for each TC record
        within the file path specified upon entry.

    """

    # Read in TC-vitals records.
    with open(filepath, "r", encoding="utf-8") as file:
        tcvdata = file.read()

    # Collect the attributes for the respective TC-vitals record(s);
    # proceed accordingly.
    tcvobj = parser_interface.object_define()

    for (idx, tcv) in enumerate(tcvdata.split("\n")):

        # Collect the attributes for the current TC-vitals record;
        # proceed accordingly.
        if tcv.strip():
            tcvdict = {}

            # Determine the appropriate Python dictionary to be used
            # for parsing and assigning values for the TC-vitals
            # records.
            msg = f"Parsing TC-vitals record {tcv}."
            logger.info(msg)
            tcvrec = tcv.split()

            if len(tcvrec) == 19:
                tcvrec_dict = TCV_34QUAD_DICT
            else:
                msg = (
                    "Too many attributes were found for TC-vitals "
                    f"record {tcvrec}; found {len(tcvrec)}. Aborting!!!"
                )
                raise TCVitalsInterfaceError(msg=msg)

            for item in tcvrec_dict:

                # Collect the record index and the missing value
                # indicator for the respective attribute and update
                # the local values accordingly.
                tcvidx = parser_interface.dict_key_value(
                    dict_in=tcvrec_dict[item], key="idx", no_split=True
                )
                attr_value = parser_interface.dict_key_value(
                    dict_in=tcvrec_dict[item], key="spval", no_split=True
                )

                # Collect the respective TC-vitals attribute; proceed
                # accordingly.
                tcvdict[item] = tcvrec[tcvidx]

                if attr_value is not None:
                    if str(attr_value) == str(tcvdict[item]):

                        # Update the missing datum with NoneType.
                        tcvdict[item] = None

            # Update the local Python object.
            tcvobj = parser_interface.object_setattr(
                object_in=tcvobj, key=f"TC{idx}", value=tcvdict
            )

    return tcvobj


# ----


def scale_tcvrec(tcv_dict: Dict) -> object:
    """
    Description
    -----------

    This function scales the relavant tropical cyclone records to
    their respective MKS representations and returns a Python object
    containing the respective scaled values.

    Parameters
    ----------

    tcv_dict: dict

        A Python dictionary containing the TC-vitals record
        attributes.

    Returns
    -------

    tcv_obj: object

        A Python object containing the MKS values for the respective
        TC-vitals record attributes.

    """

    # Collect the relevant attributes from the TC-vitals record.
    tcv_obj = parser_interface.object_define()
    (lat, lon, mslp, poci, rmw, roci, vmax) = [
        parser_interface.dict_key_value(
            dict_in=tcv_dict, key=key, no_split=True)
        for key in ["lat", "lon", "mslp", "poci", "rmw", "roci", "vmax"]
    ]

    # Scale the TC-vitals record attributes accordingly.
    (tcv_obj.lat, tcv_obj.lon) = __scalegeo__(lat=lat, lon=lon)

    (tcv_obj.mslp, tcv_obj.vmax) = __scaleintns__(mslp=mslp, vmax=vmax)

    (tcv_obj.poci, tcv_obj.rmw, tcv_obj.roci) = __scalesize__(
        poci=poci, roci=roci, rmw=rmw
    )

    return tcv_obj


# ----


def write_tcvfile(filepath: str, tcvstr: str) -> None:
    """
    Description
    -----------

    This function writes a user-specified TC-vitals record(s) to a
    specified filepath.

    Parameters
    ----------

    filepath: str

        A Python string specifying the file path to which to write the
        TC-vitals record(s).

    tcvstr: str

        A Python string containing the TC-vitals record(s).

    """

    # Write the TC-vitals record(s) to the specified filepath.
    msg = f"Writing TC-Vitals file {filepath}."
    logger.info(msg=msg)
    with open(filepath, "w", encoding="utf-8") as file:
        file.write(tcvstr)


# ----


def write_tcvstr(tcvit_obj: object) -> str:
    """
    Description
    -----------

    This function writes a string formatted in accordance with the
    TC-vitals format.

    Parameters
    ----------

    tcvit_obj: object

        A Python object containing the TC-vitals record attributes;
        the Python object attributes are as follows:

        Required Attributes
        -------------------

        lat: a Python float valued variable specifying the latitude
        geographical coordinate position; a negative value denotes a
        position in the Southern Hemisphere; input values range is
        -90.0 to 90.0; units are degrees.

        lon: a Python float valued variable specifying the longitude
        geographical coordinate position; a negative value denotes a
        position in the Western Hemisphere; input values range is
        -180.0 to 180.0 degrees; units are degrees.

        mslp: a Python float valued variable specifying minimum
        sea-level pressure intensity; units are hectoPascals (e.g.,
        millibars).

        tcid: a Python string variable specifying the TC identifier
        (e.g, 01L, for the first TC in the North Atlantic basin); this
        string has a 3-character maximum length.

        time_ymd: a Python string specifying the year/month/day
        attribute for the respective TC-vitals record; this string
        assumes the POSIX UNIX time-stamp convention %Y%m%d; this
        string has a 8-character maximum length.

        time_hm: a Python string specifying the hour/minute attribute
        for the respective TC-vitals record; this string assumes the
        POSIX UNIX time-stamp convention %H%M; this string has a
        4-character maximum length.

        vmax: a Python float valued variable specifying maximum wind
        speed intensity; units are meters per second.

        Optional Attributes
        -------------------

        event_name: a Python string specifying the name assigned by
        the respective forecast center (if any); if one has not been
        specified, a value of 'NAMELESS' will be assigned; this string
        has a 9-character maximum length.

        NE34, SE34, SW34, NW34: a Python float value specifying the
        radius of the 34-knot wind in the respective quadrant of the
        TC; units are kilometers; if one has not been specified, a
        value of -999 will be assigned.

        poci: a Python float value specifying the pressure of the
        outer-most closed isobar relative to the TC geographical
        coordinates position (above); units are hectoPascals (e.g.,
        millibars); if one has not been specified, a value of -999
        will be assigned.

        rmw: a Python float value specifying the radius of maximum
        wind speed; units are kilometers; if one has not been
        specified, a value of -99 will be assigned.

        roci: a Python float value specifying the radius of the
        outer-most closed isobar relative to the TC geographical
        coordinates position (above); units are kilometers; if one has
        not been specified, a value of -999 will be assigned.

        tcv_center: a Python string variable specifying the
        forecasting center from which the TC-vitals record corresponds
        or was created (from); if one has not been specified, a value
        of 'XXXX' will be assigned.

        stormdepth: a Python string value specifying the TC depth
        (e.g., 'S' for top of circulation at 700-hPa, 'M' for top of
        circulation at 400-hPa, and 'D' for top of circulation at
        200-hPa); if one has not been specified, a value of 'X' will
        be assigned.

        stormdir: a Python float value specifying the translational
        direction for the TC in the respective TC-vitals record; units
        are degrees relative to North; if one has been specified, a
        value of -99 will be assigned.

        stormspeed: a Python string specifying the translational speed
        for the TC in the respective TC-vitals record; units are
        meters per second; if one has been specified, a value of -99
        will be assigned.

    Returns
    -------

    tcvstr: str

        A Python string containing the TC-vitals record.

    Raises
    ------

    TCVitalsInterfaceError:

        * raised if the TC-vitals attribute object provided upon entry
          does not contain a mandatory TC-vitals record
          attribute/value.

    """

    # Define the TC-vitals record attributes.
    tcvstr = str()
    tcvobj = parser_interface.object_define()
    tcvstr_frmt = (
        "%-4s %-3s %-9s %s %s %s %s %03d %03d %04d %04d %04d "
        "%02d %03d %04d %04d %04d %04d %s\n"
    )

    # Check that all mandatory TC-vitals record attributes are
    # specified; proceed accordingly.
    mand_attr_list = ["lat", "lon", "mslp",
                      "tcid", "time_hm", "time_ymd", "vmax"]

    for mand_attr in mand_attr_list:
        if not parser_interface.object_hasattr(object_in=tcvit_obj, key=mand_attr):
            msg = (
                "The input TC-vitals variable object does not contain "
                f"the mandatory attribute {mand_attr}. Aborting!!!"
            )
            raise TCVitalsInterfaceError(msg=msg)

        # Build the TC-vitals record object.
        value = parser_interface.object_getattr(
            object_in=tcvit_obj, key=mand_attr)
        tcvobj = parser_interface.object_setattr(
            object_in=tcvobj, key=mand_attr, value=value
        )

    # Check the TC-vitals record attributes; proceed accordingly.
    if (
        (tcvobj.lat is None)
        or (tcvobj.lon is None)
        or (tcvobj.mslp is None)
        or (tcvobj.vmax is None)
    ):
        msg = (
            "Received a NoneType value for a required TC vitals record; no "
            "TC-vitals string will be created."
        )
        logger.warn(msg=msg)

        return tcvstr

    # Convert the wind speed units from knots to meters-per-second.
    tcvobj.vmax = (tcvobj.vmax * constants_interface.kts2mps).value

    # Define default values for the optional TC-vitals record
    # attributes.
    opt_attr_dict = {
        "event_name": "NAMELESS",
        "NE34": -999,
        "SE34": -999,
        "SW34": -999,
        "NW34": -999,
        "poci": -999,
        "rmw": -99,
        "roci": -999,
        "tcv_center": "XXXX",
        "stormdepth": "X",
        "stormdir": -99,
        "stormspeed": -99,
    }

    # Define the optional TC-vitals record attributes in accordance
    # with the values provided upon entry.
    for (opt_attr, _) in opt_attr_dict.items():

        # Collect the TC-vitals record attribute; proceed accordingly.
        if parser_interface.object_hasattr(object_in=tcvit_obj, key=opt_attr):
            value = parser_interface.object_getattr(object_in=tcvit_obj, key=opt_attr)
        else:
            value = parser_interface.dict_key_value(
                dict_in=opt_attr_dict, key=opt_attr, no_split=True
            )

        # Define the TC-vitals record attribute.
        tcvobj = parser_interface.object_setattr(
            object_in=tcvobj, key=opt_attr, value=value
        )

    # Check that the TC-vitals records are valid; proceed accordingly.
    if (tcvobj.lat is not None) and (tcvobj.lon is not None):

        # Scale the hemisphere values accordingly.
        hemip = "N" if (tcvobj.lat > 0) else "S"
        hemim = "E" if (tcvobj.lon < 0) else "W"
        tcvobj.lat = "%03d%s" % (numpy.abs(numpy.rint(tcvobj.lat * 10)), hemip)
        tcvobj.lon = "%04d%s" % (numpy.abs(numpy.rint(tcvobj.lon * 10)), hemim)

        # Write the TC-vitals record.
        tcvstr = tcvstr_frmt % (
            tcvobj.tcv_center,
            tcvobj.tcid,
            tcvobj.event_name,
            tcvobj.time_ymd,
            tcvobj.time_hm,
            tcvobj.lat,
            tcvobj.lon,
            tcvobj.stormdir,
            tcvobj.stormspeed,
            tcvobj.mslp,
            tcvobj.poci,
            tcvobj.roci,
            tcvobj.vmax,
            tcvobj.rmw,
            tcvobj.NE34,
            tcvobj.SE34,
            tcvobj.SW34,
            tcvobj.NW34,
            tcvobj.stormdepth,
        )
        msg = f"Constructed the following TC-vitals record:\n{tcvstr}"
        logger.info(msg=msg)

    return tcvstr
