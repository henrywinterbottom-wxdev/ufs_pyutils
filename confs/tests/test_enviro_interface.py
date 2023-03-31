# =========================================================================

# Module: confs/tests/test_enviro_interface.py

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

    test_enviro_interface.py

Description
-----------

    This module provides unit-tests for the respective
    enviro_interface module functions.

Classes
-------

    TestEnviroMethods()

        This is the base-class object for all enviro_interface
        unit-tests; it is a sub-class of TestCase.

Requirements
------------

- pytest; https://docs.pytest.org/en/7.2.x/

Author(s)
---------

    Henry R. Winterbottom; 21 March 2023

History
-------

    2023-03-21: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=undefined-variable

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

from unittest import TestCase

from confs import enviro_interface
from tools import parser_interface

# ----


class TestEnviroMethods(TestCase):
    """
    Description
    -----------

    This is the base-class object for all enviro_interface unit-tests;
    it is a sub-class of TestCase.

    """

    def setUp(self: TestCase) -> None:
        """
        Description
        -----------

        This method defines the base-class attributes for all
        enviro_interface unit-tests.

        """

        # Define the message to accompany any unit-test failures.
        self.unit_test_msg = "The unit-test for enviro_interface failed."

    def test_enviro_to_obj(self: TestCase) -> None:
        """
        Description
        -----------

        This method provides a unit-test for the enviro_interface
        enviro_to_obj function.

        """

        # Collect the environment variable.
        user = parser_interface.enviro_get(envvar="USER")

        # Cast the run-time enviroment as a Python object.
        envobj = enviro_interface.enviro_to_obj()

        assert envobj.USER == user, self.unit_test_msg


# ----
if __name__ == "__main__":
    unittest.main()
