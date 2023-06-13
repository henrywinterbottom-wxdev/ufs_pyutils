# =========================================================================

# Module: utils/logger_interface.py

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

    logger_interface.py

Description
-----------

    This module contains wrapper methods for the Python logging
    package.

Classes
-------

    Logger(caller_name=None)

        This is the base-class for all Python logging instances.

Author(s)
---------

    Henry R. Winterbottom; 09 February 2022

History
-------

    2023-02-09: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=missing-function-docstring

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

import logging
import sys
from abc import abstractmethod
from importlib import reload
from typing import Generic

from utils.decorator_interface import privatemethod

# ----


class Logger:
    """
    Description
    -----------

    This is the base-class object for all logger-type messages.

    Keywords
    --------

    caller_name: str

        A Python string usually designating the caller instance name
        to appended to the message string (`msg`); if NoneType upon
        entry the `msg` is not modified.

    """

    def __init__(self: Generic, caller_name: str = None):
        """
        Description
        -----------

        Creates a new Logger object.

        """

        # Define the base-class attributes.
        self.log_format = "%(asctime)s :: %(levelname)s :: %(message)s"
        self.date_format = "%Y-%m-%d %H:%M:%S"
        self.stream = sys.stdout
        self.caller_name = caller_name

        # Define the logger object format string colors; note that all
        # supported base-class logger level types must be defined
        # here.
        self.colors_dict = {
            "CRITICAL": "\x1b[1;41m",
            "DEBUG": "\x1b[38;5;46m",
            "INFO": "\x1b[37;21m",
            "ERROR": "\x1b[1;41m",
            "WARNING": "\x1b[38;5;226m",
            "RESET": "\x1b[0m",
            "STATUS": "\033[1;36m",
        }

    @privatemethod
    def format(self: Generic, loglev: str) -> str:
        """
        Description
        -----------

        This method defines the logger message string format in
        accordance with the logger level specified upon entry.

        Parameters
        ----------

        loglev: str

            A Python string defining the logger level; case
            insensitive.

        Returns
        -------

        format_str: str

            A Python string defining the logger message string format.

        """

        # Define the format string for the respective logger message.
        format_str = (
            self.colors_dict[loglev.upper()]
            + self.log_format
            + self.colors_dict["RESET"]
        )

        return format_str

    @privatemethod
    def level(self: Generic, loglev: str) -> object:
        """
        Description
        -----------

        This method defines the logging level object.

        Parameters
        ----------

        loglev: str

            A Python string defining the logger level; case
            insensitive.

        Returns
        -------

        level_obj: object

            A Python logging level object.

        """

        # Check that the logger level type is supported.
        if loglev.upper() not in self.colors_dict:
            msg = f"Logger level {loglev.upper()} not supported. Aborting!!!"
            self.stream.write(
                (self.colors_dict["ERROR"] + msg + self.colors_dict["RESET"])
            )
            raise KeyError

        # Define the logging level object.
        level_obj = getattr(logging, f"{loglev.upper()}")

        return level_obj

    @privatemethod
    def reset(self: Generic) -> None:
        """
        Description
        -----------

        This method shutsdown and subsequently reloads the logging
        module; this is step is necessary in order to reset the
        attributes of the logger handlers and allow for different
        logger levels to be instantiated from the same calling
        class/module.

        """

        # Shutdown and reload the Python logging library.
        logging.shutdown()
        reload(logging)

    @privatemethod
    def write(
        self: Generic, loglev: str, msg: str = None, custom_loglev: str = None
    ) -> None:
        """
        Description
        -----------

        This method resets the base-class imported logging object,
        defines the logging level and message string format, and
        writes the logger message in accordance with the logging level
        specified upon entry.

        Parameters
        ----------

        loglev: str

            A Python string defining the logger level; case
            insensitive.

        msg: str

            A Python string containing a message to accompany the
            logging level.

        Keywords
        --------

        custom_loglev: str, optional

            A Python string specifying a custom logger level; if
            specified a matching (case-insensitive) key must be define
            within the base-class attribute `colors_dict`.

        """

        # Reset the Python logging library.
        self.reset()

        # Define the attributes of and the logger object.
        # log = logging
        level_obj = self.level(loglev=loglev)
        if custom_loglev is not None:
            format_str = self.format(loglev=custom_loglev)
        else:
            format_str = self.format(loglev=loglev)
        logging.basicConfig(
            stream=self.stream,
            level=level_obj,
            datefmt=self.date_format,
            format=format_str,
        )

        # Write the respective logger level message.
        if self.caller_name is not None:
            msg = f"{self.caller_name}: " + msg
        getattr(logging, f"{loglev}")(msg)

    # The base-class logger CRITICAL level interface.
    @abstractmethod
    def critical(self: object, msg: str) -> None:
        self.write(loglev="critical", msg=msg)

    # The base-class logger DEBUG level interface.
    @abstractmethod
    def debug(self: object, msg: str) -> None:
        self.write(loglev="debug", msg=msg)

    # The base-class logger ERROR level interface.
    @abstractmethod
    def error(self: object, msg: str) -> None:
        self.write(loglev="error", msg=msg)

    # The base-class logger INFO level interface.
    @abstractmethod
    def info(self: object, msg: str) -> None:
        self.write(loglev="info", msg=msg)

    # The base-class logger STATUS level interface.
    @abstractmethod
    def status(self: object, msg: str) -> None:
        self.write(loglev="info", msg=msg, custom_loglev="STATUS")

    # The base-class logger WARNING level interface.
    @abstractmethod
    def warn(self: object, msg: str) -> None:
        self.write(loglev="warning", msg=msg)
