# =========================================================================

# Module: utils/exceptions_interface.py

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

    exceptions_interface.py

Description
-----------

    This module loads the exceptions package.

Classes
-------

    ArgumentsInterfaceError()

        This is the base-class for exceptions encountered within the
        utils/arguments_interface module; it is a sub-class of Error.

    AWSCLIInterfaceError()

        This is the base-class for exceptions encountered within the
        utils/awscli_interface module; it is a sub-class of Error.

    Boto3InterfaceError()

        This is the base-class for exceptions encountered within the
        utils/boto3_interface module; it is a sub-class of Error.

    CurlInterfaceError()

        This is the base-class for exceptions encountered within the
        utils/curl_interface module; it is a sub-class of Error.

    GRIBInterfaceError()

        This is the base-class for exceptions encountered within the
        utils/grib_interface module; it is a sub-class of Error.

    HashLibInterfaceError()

        This is the base-class for exceptions encountered within the
        utils/hashlib_interface module; it is a sub-class of Error.

    NetCDF4InterfaceError()

        This is the base-class for exceptions encountered within the
        utils/netcdf4_interface module; it is a sub-class of Error.

    NOAAHPSSInterfaceError()

        This is the base-class for exceptions encountered within the
        utils/noaahpss_interface module; it is a sub-class of Error.

    ParserInterfaceError()

        This is the base-class for exceptions encountered within the
        tools/parser_interface module; it is a sub-class of Error.        

    SchemaInterfaceError()

        This is the base-class for exceptions encountered within the
        utils/schema_interface module; it is a sub-class of Error.

    SQLite3InterfaceError()

        This is the base-class for exceptions encountered within the
        ioapps/sqlite3_interface module; it is a sub-class of Error.

    TimestampsInterfaceError()

        This is the base-class for exceptions encountered within the
        utils/timestamp_interface module; it is a sub-class of Error.

Author(s)
---------

    Henry R. Winterbottom; 28 December 2022

History
-------

    2022-12-28: Henry Winterbottom -- Initial implementation.

"""

# ----

from utils.error_interface import Error

# ----

# Define all available attributes.
__all__ = [
    "ArgumentsInterfaceError",
    "AWSCLIInterfaceError",
    "Boto3InterfaceError",
    "CurlInterfaceError",
    "ParserInterfaceError",
    "SchemaInterfaceError",
    "SQLite3InterfaceError",
    "TarFileInterfaceError",
    "TCVitalsInterfaceError",
    "TimestampsInterfaceError",
]

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----


class ArgumentsInterfaceError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    utils/arguments_interface module; it is a sub-class of Error.

    """

# ----


class AWSCLIInterfaceError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    ioapps/awscli_interface module; it is a sub-class of Error.

    """

# ----


class Boto3InterfaceError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    ioapps/boto3_interface module; it is a sub-class of Error.

    """

# ----


class CurlInterfaceError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    ioapps/curl_interface module; it is a sub-class of Error.

    """

# ----


class GRIBInterfaceError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    ioapps/grib_interface module; it is a sub-class of Error.

    """

# ----


class HashLibInterfaceError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    ioapps/hashlib_interface module; it is a sub-class of Error.

    """

# ----


class NetCDF4InterfaceError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    ioapps/netcdf4_interface module; it is a sub-class of Error.

    """

# ----


class NOAAHPSSInterfaceError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    ioapps/noaahpss_interface module; it is a sub-class of Error.

    """

# ----


class ParserInterfaceError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    tools/parser_interface module; it is a sub-class of Error.

    """

# ----


class SchemaInterfaceError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    utils/schema_interface module; it is a sub-class of Error.

    """

# ----


class SQLite3InterfaceError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    ioapps/sqlite3_interface module; it is a sub-class of Error.

    """

# ----


class TarFileInterfaceError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    ioapps/tarfile_interface module; it is a sub-class of Error.

    """

# ----


class TCVitalsInterfaceError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    ioapps/tcvitals_interface module; it is a sub-class of Error.

    """

# ----


class TimestampsInterfaceError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    utils/timestamp_interface module; it is a sub-class of Error.

    """


# ----


class URLInterfaceError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    ioapps/url_interface module; it is a sub-class of Error.

    """
