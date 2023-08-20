# =========================================================================

# Module: tools/datetime_interface.py

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

    datetime_interface.py

Description
-----------

    This module contains functions in order to manipulate date and
    time strings as required by the caller application.

Functions
---------

    _get_dateobj(datestr, frmttyp)

        This function builds/defines and returns the Python datetime
        object relative to the attributes provided upon entry.

    compare_crontab(datestr, cronstr, frmttyp)

        This function compares the user-specified date to the a
        crontab formatted value and returns a boolean value specifying
        whether the crontab string (specifying when to execute an
        action) and user-specified date match.

    current_date(frmttyp, is_utc=False)

        This function returns the current time (at invocation of this
        function) formatted according to the parameter values
        specified upon entry.

    datestrcomps(datestr, frmttyp)

        This function returns a Python object containing the specified
        date string component values; the following attributes are
        returned:

        year (year)

        month of year (month)

        day of month (day)

        hour of day (hour)

        minute of hour (minute)

        second of minute (second)

        full month name (month_name_long)

        abbreviated month name (month_name_short)

        full day name (weekday_long)

        abbreviated day name (weekday_short)

        2-digit century (e.g., 2015 is 20; century_short)

        2-digit year (e.g., year without the century value;
        year_short)

        date string (date_string; formatted as %Y-%m-%d_%H:%M:%S,
        assuming the POSIX convention)

        cycle string (cycle_string; formatted as %Y%m%d%H%M%S,
        assuming the POSIX convention)

        Julian date (julian_day)

        The HH:MM:SS as the total elapsed seconds, formatted as
        5-digit integer (total_seconds_of_day)

        The day of the year (day_of_year); begins from day 1 of
        respective year.

        epoch (seconds since 0000 UTC 01 January 1970).

    datestrfrmt(datestr, frmttyp, offset_seconds=None)

        This function ingests a date string and computes and returns a
        (newly/different) formatted date string; the format of the
        respective date string is defined by the `frmttyp` parameter
        specified upon entry; an optional keyword `offset_seconds`
        defines a datestr relative to the value for parameter
        `datestr` and the the specified number of seconds; both
        positive and negative values for `offset_seconds` is
        supported.

    datestrupdate(datestr, in_frmttyp, out_frmttyp,
                  offset_seconds=None)

        This function ingests a date string and an optional argument
        `offset_seconds` to define a new datestr relative to the user
        provided `datestr` and the number of seconds and the input and
        output date string formats; this function also permits
        non-POSIX standard time attributes, as determined by
        datestrcomps (above) and user specified template values
        (denoted between < > in the `out_frmttyp` parameter).

    elapsed_seconds(start_datestr, start_frmttyp, stop_datestr,
                    stop_frmttyp)

        This function computes and returns the total number of seconds
        (e.g., the difference) between two input date strings.

    epoch_to_datestr(epoch_seconds, out_frmttyp=None)

        This function transforms the epoch time (e.g., the number of
        seconds relative to 0000 UTC 01 January 1970) to the
        (optional) date-string format (`out_frmttyp`).

Requirements
------------

- croniter; https://github.com/kiorky/croniter

Author(s)
---------

   Henry R. Winterbottom; 03 December 2022

History
-------

   2022-12-03: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=consider-using-f-string
# pylint: disable=no-member

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

import datetime
import sqlite3
import time
from types import SimpleNamespace
from typing import List

import croniter
from utils import timestamp_interface
from utils.exceptions_interface import DateTimeInterfaceError

from tools import parser_interface

# ----

# Define all available functions.
__all__ = [
    "compare_crontab",
    "current_date",
    "datestrcomps",
    "datestrfrmt",
    "datestrlist",
    "datestrupdate",
    "elapsed_seconds",
    "epoch_to_datestr",
]

# ----


def _get_dateobj(datestr: str, frmttyp: str) -> datetime.datetime:
    """
    Description
    -----------

    This function builds/defines and returns the Python datetime
    object relative to the attributes provided upon entry.

    Parameters
    ----------

    datestr: str

        A Python string containing a date string.

    frmttyp: str

        A Python string specifying the format of the timestamps
        string; this assumes POSIX convention date attribute
        characters.

    Returns
    -------

    dateobj: datetime.datetime

        A Python datetime.datetime object defined relative to the
        attributes provided upon entry.

    """

    # Define the datetime object.
    dateobj = datetime.datetime.strptime(datestr, frmttyp)

    return dateobj


# ----


def compare_crontab(datestr: str, cronstr: str, frmttyp: str) -> bool:
    """
    Description
    -----------

    This function compares the user-specified date to the a crontab
    formatted value and returns a boolean value specifying whether the
    crontab string (specifying when to execute an action) and
    user-specified date match.

    Parameters
    ----------

    datestr: str

        A Python string containing a date string.

    cronstr: str

        A Python string specifying a crontab formatted date string for
        which to perform an action.

    frmttyp: str

        A Python string specifying the format of the timestamps
        string; this assumes POSIX convention date attribute
        characters.

    Returns
    -------

    crontab_match: bool

        A Python boolean valued variable specifying whether the
        crontab string (specifying when to execute an action) and a
        date match.

    """

    # Compare the date string and crontab formatted datastring and
    # determine whether they match.
    dateobj = _get_dateobj(datestr, frmttyp)
    crontab_match = croniter.croniter.match(cronstr, dateobj)

    return crontab_match


# ----


def current_date(frmttyp: str, is_utc: bool = False) -> str:
    """
    Description
    -----------

    This function returns the current time (at invocation of this
    function) formatted according to the parameter values specified
    upon entry.

    Parameters
    ----------

    frmttyp: str

        A Python string specifying the format of the output timestamp
        string; this assumes POSIX convention date attribute
        characters.

    Keywords
    --------

    is_utc: bool, optional

        A Python boolean valued variable specifying whether to return
        the current date/timestamp in Coordinated Universal Time.

    Returns
    -------

    timestamp: str

        A Python string containing the current time (at invocation of
        this function) formatted according to the user specifications.

    """

    # Determine the timestamp corresponding to the current time upon
    # function entry; proceed accordingly.
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime(frmttyp)
    if is_utc:
        dateobj = _get_dateobj(datestr=timestamp, frmttyp=frmttyp).utcnow()
        timestamp = datetime.datetime.strftime(dateobj, frmttyp)

    return timestamp


# ----


def datestrcomps(datestr: str, frmttyp: str) -> SimpleNamespace:
    """
    Description
    -----------

    This function returns a Python object containing the specified
    date string component values; the following attributes are
    returned:

       - year (year)

       - month of year (month)

       - day of month (day)

       - hour of day (hour)

       - minute of hour (minute)

       - second of minute (second)

       - full month name (month_name_long)

       - abbreviated month name (month_name_short)

       - full day name (weekday_long)

       - abbreviated day name (weekday_short)

       - 2-digit century (e.g., 2015 is 20; century_short)

       - 2-digit year (e.g., year without the century value;
         year_short)

       - date string (date_string; formatted as %Y-%m-%d_%H:%M:%S,
         assuming the POSIX convention)

       - cycle string (cycle_string; formatted as %Y%m%d%H, assuming
         the POSIX convention)

       - Julian date (julian_day)

       - The HH:MM:SS as the total elapsed seconds, formatted as
         5-digit integer (total_seconds_of_day)

       - The day of the year (day_of_year); begins from day 1 of
         respective year.

       - epoch (seconds since 0000 UTC 01 January 1970).

    Parameters
    ----------

    datestr: str

        A Python string containing a date string.

    frmttyp: str

        A Python string specifying the format for the input date
        string (`datestr`).

    Returns
    -------

    date_comps_obj: SimpleNamespace

        A Python SimpleNamespace object containing the date string
        component values for the user specfied date string.

    """

    # Initialize the Python datetime objects.
    date_comps_obj = parser_interface.object_define()
    dateobj = _get_dateobj(datestr, frmttyp)

    # Loop through timestamp attributes and append values to local
    # list.
    date_comps_dict = {
        "year": "%Y",
        "month": "%m",
        "day": "%d",
        "hour": "%H",
        "minute": "%M",
        "second": "%S",
        "month_name_long": "%B",
        "month_name_short": "%b",
        "century_short": "%C",
        "year_short": "%y",
        "weekday_long": "%A",
        "weekday_short": "%a",
        "date_string": timestamp_interface.GENERAL,
        "cycle": timestamp_interface.GLOBAL,
        "day_of_year": "%j",
    }

    for (key, item) in date_comps_dict.items():
        value = datetime.datetime.strftime(dateobj, item)
        date_comps_obj = parser_interface.object_setattr(
            object_in=date_comps_obj, key=key, value=value
        )

    # Define connect object for SQlite3 library and define the
    # timestamp values accordingly.
    connect = sqlite3.connect(":memory:")
    datestr = "{0}-{1}-{2} {3}:{4}:{5}".format(
        date_comps_obj.year,
        date_comps_obj.month,
        date_comps_obj.day,
        date_comps_obj.hour,
        date_comps_obj.minute,
        date_comps_obj.second,
    )

    # Collect the Julian attribute using SQLite3 and proceed
    # accordingly.
    value = list(connect.execute(f'select julianday("{datestr}")'))[0][0]
    date_comps_obj.julian_day = value

    # Collect the total number of seconds of the day corresponding to
    # the respective timestamp provided upon entry.
    timedate = time.strptime(datestr, "%Y-%m-%d %H:%M:%S")

    value = datetime.timedelta(
        hours=timedate.tm_hour, minutes=timedate.tm_min, seconds=timedate.tm_sec
    ).total_seconds()
    value = f"{int(value):05d}"
    date_comps_obj.total_seconds_of_day = value

    # Define the epoch time (seconds) corresponding to the respective
    # timestamp.
    value = datetime.datetime(
        int(date_comps_obj.year),
        int(date_comps_obj.month),
        int(date_comps_obj.day),
        int(date_comps_obj.hour),
        int(date_comps_obj.minute),
        int(date_comps_obj.second),
    ).timestamp()
    date_comps_obj.epoch = value

    # Add the date and time component list corresponding to the
    # respective timestamp provided upon entry.
    date_comps_obj.comps_list = vars(date_comps_obj)

    return date_comps_obj


# ----


def datestrfrmt(datestr: str, frmttyp: str, offset_seconds: int = None) -> str:
    """ "
    Description
    -----------

    This function ingests a date string and computes and returns a
    (newly/different) formatted date string; the format of the
    respective date string is defined by the `frmttyp` parameter
    specified upon entry; an optional keyword `offset_seconds` defines
    a datestr relative to the value for parameter `datestr` and the
    the specified number of seconds; both positive and negative values
    for `offset_seconds` is supported.

    Parameters
    ----------

    datestr: str

        A Python string containing a date string; the input date
        string is assumed to have format %Y-%m-%d_%H:%M:%S assuming
        the POSIX convention.

    frmttyp: str

        A Python string specifying the format of the timestamps
        string; this assumes POSIX convention date attribute
        characters.

    Keywords
    --------

    offset_seconds: int, optional

        A Python integer defining the total number of `offset-seconds`
        relative to the `datestr` variable (see above) for the output
        time-stamp/date-string; the default is NoneType.

    Returns
    -------

    outdatestr: str

        A Python string containing the appropriately formatted
        time-stamp/date-string.

    """

    # Define the specified format for the respective date and
    # timestamp provided upon entry.
    dateobj = _get_dateobj(datestr, "%Y-%m-%d_%H:%M:%S")

    if offset_seconds is not None:
        dateobj = dateobj + datetime.timedelta(0, offset_seconds)

    outdatestr = datetime.datetime.strftime(dateobj, frmttyp)

    return outdatestr


# ----


def datestrlist(
    datestr_start: str,
    datestr_stop: str,
    offset_seconds: int,
    in_frmttyp: str,
    out_frmttyp: str,
) -> List:
    """
    Description
    -----------

    This function defines and returns a list of timestamp strings in
    accordance with the parameter attributes specified upon entry.

    Parameters
    ----------

    datestr_start: str

        A Python string defining the start timestamp for the interval.

    datestr_stop: str

        A Python string defining the stop timestamp for the interval.

    offset_seconds: int

        A Python integer defining the interval in seconds for
        timestamp string definition within the interval defined by
        `datestr_start` and `datestr_stop` upon entry.

    in_frmttyp: str

        A Python string specifying the POSIX convention for the
        `datestr_start` and `datestr_stop` variables upon input.

    out_frmttyp: str

        A Python string specifying the POSIX convention for format of
        the timestamps within the returned list.

    Returns
    -------

    datestr_list: List

        A Python list of formatted timestamp strings comprising the
        interval defined by `datestr_start`, `datestr_stop`, and
        `offset_seconds` upon entry.

    Raises
    ------

    DateTimeInterfaceError:

        - raised if the `offset_seconds` parameter is less than or
          equal to 0 upon entry.

    """

    # Define and return a list of timestamp strings in accordance with
    # the parameter attributes specified upon entry.
    if offset_seconds <= 0:
        msg = (
            f"For timestamp lists the `offset_seconds` parameter must be "
            f"greater than 0; received {offset_seconds} upon entry. "
            "Aborting!!!"
        )
        raise DateTimeInterfaceError(msg=msg)

    # Define the components of the respective date strings.
    start_comps = datestrcomps(datestr=datestr_start, frmttyp=in_frmttyp)
    stop_comps = datestrcomps(datestr=datestr_stop, frmttyp=in_frmttyp)
    ndatestr = int((stop_comps.epoch - start_comps.epoch) / offset_seconds) + 1

    # Define the list of datestrings.
    datestr_list = [
        datestrupdate(
            datestr=datestr_start,
            in_frmttyp=in_frmttyp,
            out_frmttyp=out_frmttyp,
            offset_seconds=(idx * offset_seconds),
        )
        for idx in range(ndatestr)
    ]

    return datestr_list


# ----


def datestrupdate(
    datestr: str, in_frmttyp: str, out_frmttyp: str, offset_seconds: int = None
) -> str:
    """
    Description
    -----------

    This function ingests a date string and an optional argument
    `offset_seconds` to define a new datestr relative to the user
    provided `datestr` and the number of seconds and the input and
    output date string formats; this function also permits non-POSIX
    standard time attributes, as determined by datestrcomps (above)
    and user specified template values (denoted between < > in the
    `out_frmttyp` parameter).

    Parameters
    ----------

    datestr: str

        A Python string containing a date string of format
        `in_frmttyp` (see below).

    in_frmttyp: str

        A Python string specifying the POSIX convention for the
        `datestr` variable upon input.

    out_frmttyp: str

        A Python string specifying the POSIX convention for the
        `datestr` variable upon output.

    Keywords
    --------

    offset_seconds: int, optional

        A Python integer defining the total number of offset-seconds
        relative to the `datestr` variable(see above) for the output
        time-stamp/date-string; the default is NoneType.

    Returns
    -------

    outdatestr: str

        A Python string containing the appropriately formatted
        time-stamp/date-string.

    """

    # Update the date and timestamp in accordance with the specified
    # arguments.
    dateobj = _get_dateobj(datestr, in_frmttyp)

    if offset_seconds is not None:
        dateobj = dateobj + datetime.timedelta(0, offset_seconds)

    outdatestr = datetime.datetime.strftime(dateobj, out_frmttyp)
    date_comps_obj = datestrcomps(datestr=datestr, frmttyp=in_frmttyp)

    comps_list = date_comps_obj.comps_list

    for item in comps_list:
        if f"<{item}>" in outdatestr:
            time_attr = parser_interface.object_getattr(
                date_comps_obj, key=item)
            outdatestr = outdatestr.replace(f"<{item}>", time_attr)

    return outdatestr


# ----


def elapsed_seconds(
    start_datestr: str, start_frmttyp: str, stop_datestr: str, stop_frmttyp: str
) -> float:
    """
    Description
    -----------

    This function computes and returns the total number of seconds
    (e.g., the difference) between two input date strings.

    Parameters
    ----------

    start_datestr: str

        A Python string containing a date string of format
        `start_frmttyp` (below).

    start_frmttyp: str

       A Python string specifying the POSIX convention for the
       `start_datestr` variable.

    stop_datestr: str

        A Python string containing a date string of format
        `stop_frmttyp` (below).

    stop_frmttyp: str

        A Python string specifying the POSIX convention for the
        `stop_datestr` variable.

    Returns
    -------

    seconds: float

        A Python float value specifying the total number of seconds
        between the two input date strings.

    """

    # Compute the total number of seconds between the specified
    # datestrings upon entry.
    start_dateobj = _get_dateobj(start_datestr, start_frmttyp)
    stop_dateobj = _get_dateobj(stop_datestr, stop_frmttyp)

    seconds = float((stop_dateobj - start_dateobj).total_seconds())

    return seconds


# ----


def epoch_to_datestr(epoch_seconds: int, out_frmttyp: str = None) -> str:
    """
    Description
    -----------

    This function transforms the epoch time (e.g., the number of
    seconds relative to 0000 UTC 01 January 1970) to the (optional)
    date-string format (`out_frmttyp`).

    Parameters
    ----------

    epoch_seconds: int

        A Python integer specifying the epoch seconds.

    Keywords
    --------

    out_frmttyp: str, optional

        A Python string defining the date-string format for the epoch
        time format.

    Returns
    -------

    epoch_datestr: str

        A Python string defining the epoch time (seconds) represented
        as date-string characters.

    """

    # Define the epoch time (seconds) date-string.
    datestr = out_frmttyp or timestamp_interface.GLOBAL

    epoch_datestr = datetime.datetime.fromtimestamp(
        epoch_seconds).strftime(datestr)

    return epoch_datestr
