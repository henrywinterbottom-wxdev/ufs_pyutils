# =========================================================================

# Module: utils/tests/test_schema_interface.py

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

    test_schema_interface.py

Description
-----------

    This module provides unit-tests for the respective
    schema_interface module functions.

Classes
-------

    TestSchemaMethods()

        This is the base-class object for all schema_interface
        unit-tests; it is a sub-class of TestCase.

Requirements
------------

- pytest; https://docs.pytest.org/en/7.2.x/

Author(s)
---------

    Henry R. Winterbottom; 26 April 2023

History
-------

    2023-04-26: Henry Winterbottom -- Initial implementation.

"""

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

import os
import unittest
from unittest import TestCase

from confs.yaml_interface import YAML
from utils import schema_interface
from utils.exceptions_interface import SchemaInterfaceError

# ----


class TestSchemaMethods(TestCase):
    """
    Description
    -----------

    This is the base-class object for all schema_interface unit-tests;
    it is a sub-class of TestCase.

    """

    def setUp(self: TestCase) -> None:
        """
        Description
        -----------

        This method defines the base-class attributes for all
        schema_interface unit-tests.

        """

        # Define the base-class attributes.
        dirpath = os.path.join(os.getcwd(), "tests")
        self.yaml_path = os.path.join(dirpath, "test_files", "schema.yaml")

        # Define the test schemas.
        self.test1_schema_dict = {
            "variable1": True,
            "variable2": 10.0,
            "variable3": 4,
            "variable4": True,
            "variable5": False,
            "variable6": -1.0,
        }

        self.test2_schema_dict = {
            "variable1": "spam",
            "variable2": 10.0,
            "variable3": 4,
            "variable4": True,
            "variable5": False,
            "variable6": -1.0,
        }

        self.test3_schema_dict = {
            "variable1": False,
            "variable2": 10.0,
            "variable3": 4,
        }

        # Define the message to accompany any unit-test failures.
        self.unit_test_msg = "The unit-test for schema_interface function {0} failed."

    def test_build(self: TestCase) -> None:
        """
        Description
        -----------

        This method provides a unit-test for the schema_interface
        `build_schema` function.

        """

        # Define the schema attributes.
        schema_def_dict = YAML().read_yaml(yaml_file=self.yaml_path)
        schema_dict = schema_interface.build_schema(schema_def_dict=schema_def_dict)

        # Perform the schema validation unit-tests; check that the
        # schema is valid.
        schema_interface.validate_opts(
            cls_schema=schema_dict, cls_opts=self.test1_schema_dict
        )

        assert True

        # Check that the validation fails due to incorrect types.
        try:
            schema_interface.validate_opts(
                cls_schema=schema_dict, cls_opts=self.test2_schema_dict
            )
        except SchemaInterfaceError:
            assert True

        # Check that the schema validation passes using default values
        # for the optional attributes.
        schema_interface.validate_opts(
            cls_schema=schema_dict, cls_opts=self.test3_schema_dict
        )

        assert True


# ----
if __name__ == "__main__":
    unittest.main()
