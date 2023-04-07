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

    Logger()

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
from importlib import reload

from utils.decorator_interface import private

# ----


class Logger:
    """
    Description
    -----------

    This is the base-class object for all logger-type messages.

    """

    def __init__(self: object):
        """
        Description
        -----------

        Creates a new Logger object.

        """

        # Define the base-class attributes.
        self.log_format = "%(asctime)s :: %(levelname)s :: %(message)s"
        self.date_format = "%Y-%m-%d %H:%M:%S"
        self.stream = sys.stdout

        # Define the logger object format string colors; note that all
        # supported base-class logger level types must be defined
        # here.
        self.colors_dict = {
            "CRITICAL": "\x1b[1;43m",
            "DEBUG": "\x1b[38;5;46m",
            "INFO": "\x1b[37;21m",
            "ERROR": "\x1b[1;41m",
            "WARNING": "\x1b[38;5;226m",
            "RESET": "\x1b[0m",
        }

    @private
    def level(self: object, loglev: str) -> object:
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

    @private
    def format(self: object, loglev: str) -> object:
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

        format_str = (
            self.colors_dict[loglev.upper()]
            + self.log_format
            + self.colors_dict["RESET"]
        )

        return format_str

    @private
    def reset(self: object) -> None:
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

    @private
    def write(self: object, loglev: str, msg: str = None) -> None:
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

        """

        # Reset the Python logging library.
        self.reset()

        # Define the attributes of and the logger object.
        log = logging
        level_obj = self.level(loglev=loglev)
        format_str = self.format(loglev=loglev)

        log.basicConfig(
            stream=self.stream,
            level=level_obj,
            datefmt=self.date_format,
            format=format_str,
        )

        # Write the respective logger level message.
        getattr(log, f"{loglev}")(msg)

    # The base-class logger CRITICAL level interface.
    def critical(self: object, msg: str) -> None:
        self.write(loglev="critical", msg=msg)

    # The base-class logger DEBUG level interface.
    def debug(self: object, msg: str) -> None:
        self.write(loglev="debug", msg=msg)

    # The base-class logger ERROR level interface.
    def error(self: object, msg: str) -> None:
        self.write(loglev="error", msg=msg)

    # The base-class logger INFO level interface.
    def info(self: object, msg: str) -> None:
        self.write(loglev="info", msg=msg)

    # The base-class logger WARNING level interface.
    def warn(self: object, msg: str) -> None:
        self.write(loglev="warning", msg=msg)
