# =========================================================================

# Module: confs/tests/test_jinja2_interface.py

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

    test_jinja2_interface.py

Description
-----------

    This module provides unit-tests for the respective
    jinja2_interface module functions.

Classes
-------

    TestJinja2Methods()

        This is the base-class object for all jinja2_interface
        unit-tests; it is a sub-class of TestCase.

Requirements
------------

- pytest; https://docs.pytest.org/en/7.2.x/

- pytest-order; https://github.com/pytest-dev/pytest-order


Author(s)
---------

    Henry R. Winterbottom; 28 February 2023

History
-------

    2023-02-28: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=undefined-variable

# ----

import os
from unittest import TestCase

import pytest
from confs import jinja2_interface
from tools import fileio_interface

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----


class TestJinja2Methods(TestCase):
    """
    Description
    -----------

    This is the base-class object for all jinja2_interface unit-tests;
    it is a sub-class of TestCase.

    """

    def setUp(self: TestCase) -> None:
        """
        Description
        -----------

        This method defines the base-class attributes for all
        jinja2_interface unit-tests.

        """

        # Define the base-class attributes.
        self.jinja2_test_dict = {"NAME1": "ham",
                                 "NAME2": "eggs", "NAME3": "spam"}

        # Define the file paths required for the test method(s).
        dirpath = os.path.join(os.getcwd(), "tests")
        self.jinja2_template = os.path.join(
            dirpath, "test_files", "jinja2.template")
        self.jinja2_check = os.path.join(dirpath, "test_files", "jinja2.check")
        self.jinja2_file = os.path.join(dirpath, "jinja2.test")

        # Define the message to accompany any unit-test failures.
        self.unit_test_msg = "The unit-test for jinja2_interface failed."

    @pytest.mark.order(100)
    def test_cleanup(self: TestCase) -> None:
        """
        Description
        -----------

        This method removes the test files used for the respective
        jinja2_interface function unit-tests; it is not an actual
        unit-test but is simply used to remove the test files file
        following the completion of the actual (i.e., valid)
        unit-tests; this should be the last test that is executed by
        pytest.

        """

        # Define the list of (the) test file(s) to be removed.
        filelist = [self.jinja2_file]

        # Remove the specified files.
        fileio_interface.removefiles(filelist=filelist)

    @pytest.mark.order(1)
    def test_write_from_template(self: TestCase) -> None:
        """
        Description
        -----------

        This method provides a unit-test for the jinja2_interface
        module write_from_template function.

        """

        # Write the Jinja2-formatted file from the Jinja2-formatted
        # template file.
        jinja2_interface.write_from_template(
            tmpl_path=self.jinja2_template,
            output_file=self.jinja2_file,
            in_dict=self.jinja2_test_dict,
            fail_missing=True,
        )

        assert True

        # Compare the generated Jinja2-formatted file to the example
        # Jinja2-formatted file.
        with open(self.jinja2_check, "r", encoding="utf-8") as file:
            jinja2_check = file.read().rstrip()
        with open(self.jinja2_check, "r", encoding="utf-8") as file:
            jinja2_file = file.read().rstrip()

        assert jinja2_check == jinja2_file, self.unit_test_msg


# ----


if __name__ == "__main__":
    unittest.main()
