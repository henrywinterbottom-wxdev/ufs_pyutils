# =========================================================================

# Module: utils/decorator_interface.py

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

    decorator_interface.py

Description
-----------

    This module contains various decorator functions available to all
    applications.

Functions
---------

    msg_except_handle(err_cls):

        This function provides a decorator to be used to raise
        specified exceptions

    private(member):

        This function provides a decorator to be used to desinated
        `private` methods within classes.

Author(s)
---------

    Henry R. Winterbottom; 06 April 2023

History
-------

    2023-04-06: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=protected-access
# pylint: disable=unused-argument

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

import functools
import sys
from collections.abc import Callable

# ----

__all__ = ["msg_except_handle", "private"]

# ----


def msg_except_handle(err_cls: object) -> Callable:
    """
    Description
    -----------

    This function provides a decorator to be used to raise specified
    exceptions.

    Parameters
    ----------

    err_cls: object

        A Python object containing the Error subclass to be used for
        exception raises.

    Returns
    -------

    decorator: Callable

        A Python decorator.

    """

    # Define the decorator function.
    def decorator(func: Callable):

        # Execute the caller function; proceed accordingly.
        def call_function(msg: str) -> None:

            # If an exception is encountered, raise the respective
            # exception.
            raise err_cls(msg=msg)

        return call_function

    return decorator


# ----


def private(member: object) -> Callable:
    """
    Description
    -----------

    This function provides a decorator to be used to desinated
    `private` methods within classes.

    Parameters
    ----------

    member: object

        A Python object containing the respective base-class within
        which the respective private method exists.

    Returns
    -------

    wrapper: Callable

        A Python decorator.

    """

    # Define the decorator function.
    @functools.wraps(member)
    def wrapper(*func_args):

        # Define the names for the respective class and calling
        # functions.
        name = member.__name__
        caller = sys._getframe(1).f_code.co_name

        # Check that the method is not being called from outside the
        # base-class; proceed accordingly.
        if (not caller in dir(func_args[0])) and (not caller in name):
            msg = f"{name} called by {caller} is a private method. Aborting!!!"
            raise Exception(msg)

        return member(*func_args)

    return wrapper
