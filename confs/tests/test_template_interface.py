# =========================================================================

# Module: confs/tests/test_template_interface.py

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

    test_template_interface.py

Description
-----------

    This module provides unit-tests for the respective
    template_interface module functions.

Classes
-------

    TestTemplateMethods()

        This is the base-class object for all template_interface
        unit-tests; it is a sub-class of TestCase.

Requirements
------------

- pytest; https://docs.pytest.org/en/7.2.x/

- pytest-order; https://github.com/pytest-dev/pytest-order

Author(s)
---------

    Henry R. Winterbottom; 19 April 2023

History
-------

    2023-04-19: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=undefined-variable

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

import os
from collections import OrderedDict
from unittest import TestCase

import pytest
from confs.template_interface import Template
from tools import fileio_interface
from utils.exceptions_interface import TemplateInterfaceError

# ----


class TestTemplateMethods(TestCase):
    """
    Description
    -----------

    This is the base-class object for all template_interface
    unit-tests; it is a sub-class of TestCase.

    """

    def setUp(self: TestCase) -> None:
        """
        Description
        -----------

        This method defines the base-class attributes for all
        template_interface unit-tests.

        """

        # Define the base-class attributes.
        self.tmpl1_dict = OrderedDict(
            {
                "EGGS": 2,
                "HAM": 1,
                "JUST_HAM": False,
                "DINNER": "spam",
                "DESSERT": "Always!",
            }
        )

        self.tmpl2_dict = OrderedDict(
            {
                "EGGS": 2,
                "HAM": 1,
                "JUST_HAM": True,
                "DINNER": "spam",
                "DESSERT": "Always!",
            }
        )

        # Define the file paths required for the test method(s).
        dirpath = os.path.join(os.getcwd(), "tests")
        self.tmpl_check = os.path.join(dirpath, "test_files", "template.check")
        self.tmpl_path = os.path.join(dirpath, "template.test")
        self.template_path = os.path.join(dirpath, "test_files", "template.template")

        # Define the message to accompany any unit-test failures.
        self.unit_test_msg = "The unit-test for template_interface failed."

    @pytest.mark.order(100)
    def test_cleanup(self: TestCase) -> None:
        """
        Description
        -----------

        This method removes the test files used for the respective
        template_interface function unit-tests; it is not an actual
        unit-test but is simply used to remove the test files file
        following the completion of the actual (i.e., valid)
        unit-tests; this should be the last test that is executed by
        pytest.

        """

        # Define the list of (the) test file(s) to be removed.
        filelist = [self.tmpl_path]

        # Remove the specified files.
        fileio_interface.removefiles(filelist=filelist)

    @pytest.mark.order(1)
    def test_template(self: TestCase) -> None:
        """
        Description
        -----------

        This method provides a unit-test for the yaml_interface
        module.

        """

        # Write the output file using the input template.
        Template().write_tmpl(
            attr_dict=self.tmpl1_dict,
            tmpl_path=self.tmpl_path,
            template_path=self.template_path,
            f90_bool=False,
            fail_missing=True,
        )

        # Read the generated file and the example template file.
        with open(self.tmpl_check, "r", encoding="utf-8") as file:
            tmpl_check = file.read().rstrip().split("\n")
        with open(self.tmpl_path, "r", encoding="utf-8") as file:
            tmpl_path = file.read().rstrip().split("\n")

        assert set(tmpl_check) == set(tmpl_path), self.unit_test_msg

        try:
            Template().write_tmpl(
                attr_dict=self.tmpl2_dict,
                tmpl_path=self.tmpl_path,
                template_path=self.template_path,
                f90_bool=True,
                fail_missing=True,
            )
            assert True

        except TemplateInterfaceError:
            assert True


# ----
if __name__ == "__main__":
    unittest.main()
