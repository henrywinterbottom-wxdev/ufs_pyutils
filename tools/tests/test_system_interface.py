# =========================================================================
# File: tools/tests/test_system_interface.py
# Author: Henry R. Winterbottom
# Date: 17 August 2023
# Version: 0.0.1
# License: LGPL v2.1
# =========================================================================

"""
Module
------

    test_system_interface.py

Description
-----------

    This module contains unit tests for the tools.system_interface
    module.

Classes
-------

    TestSystemInterface()

        This is the base-class object for all tools.system_interface
        module unit tests; it is a sub-class of unittest.TestCase.

Author(s)
---------

    Henry R. Winterbottom; 17 August 2023

History
-------

    2023-08-17: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=missing-function-docstring
# pylint: disable=redefined-outer-name
# pylint: disable=unused-variable

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

import os
import sys
import time
import unittest
from unittest.mock import patch

import pytest
from tools.fileio_interface import virtual_file
from tools.system_interface import (
    app_path,
    chown,
    get_app_path,
    get_pid,
    sleep,
    task_exit,
    user,
)

# ----


class TestSystemInterface(unittest.TestCase):
    """
    Description
    -----------

    This is the base-class object for all tools.system_interface
    module unit tests; it is a sub-class of unittest.TestCase.

    """

    # Define the unit test variables.
    def setUp(self: unittest.TestCase) -> None:
        self.temp_file = virtual_file().name

    # The following are unit tests for the function `app_path`.
    @patch("subprocess.Popen")
    def test_app_path_with_path(self: unittest.TestCase, mock_popen) -> None:
        mock_output = b"app: /path/to/app\n"
        mock_popen.return_value.communicate.return_value = (mock_output, b"")
        result = app_path("app")
        self.assertEqual(result, "/path/to/app")

    # The following are unit tests for the function `chown`.
    @patch("subprocess.Popen")
    def test_app_path_without_path(self, mock_popen) -> None:
        mock_popen.return_value.communicate.return_value = (b"", b"")
        result = app_path("app")
        self.assertIsNone(result)

    @pytest.mark.order(1)
    def test_chown_invalid_user(self: unittest.TestCase) -> None:
        user = "nonexistentuser"
        group = "groupname"
        with self.assertRaises(LookupError):
            chown(path=self.temp_file, user=user, group=group)

    @pytest.mark.order(2)
    def test_chown_invalid_group(self: unittest.TestCase) -> None:
        user = "username"
        group = "nonexistentgroup"
        with self.assertRaises(LookupError):
            chown(path=self.temp_file, user=user, group=group)

    @pytest.mark.order(3)
    def test_chown_invalid_path(self: unittest.TestCase) -> None:
        user = "username"
        group = "groupname"
        invalid_path = "nonexistent_path"
        with self.assertRaises(LookupError):
            chown(path=invalid_path, user=user, group=group)

    @pytest.mark.order(4)
    def test_destroy_virtual_file(self) -> None:
        try:
            os.unlink(self.temp_file)
        except FileNotFoundError:
            pass

    # The following are unit tests for the function `get_app_path`.
    def test_existing_app(self: unittest.TestCase) -> None:
        app_path = get_app_path("python")
        self.assertIsNotNone(app_path)
        self.assertTrue(app_path.endswith("python"))

    def test_non_existing_app(self: unittest.TestCase) -> None:
        app_path = get_app_path("nonexistent_app")
        self.assertIsNone(app_path)

    def test_empty_app_name(self: unittest.TestCase) -> None:
        app_path = get_app_path("")
        self.assertIsNone(app_path)

    def test_none_app_name(self: unittest.TestCase) -> None:
        with self.assertRaises(TypeError):
            app_path = get_app_path(None)

    # The following are unit tests for the function `get_pid`.
    def test_get_pid(self: unittest.TestCase) -> None:
        pid = get_pid()
        self.assertIsInstance(pid, int)
        self.assertGreater(pid, 0)

    # The following are unit tests for the function `sleep`.
    def test_sleep_zero_seconds(self: unittest.TestCase) -> None:
        start_time = time.time()
        sleep(0)
        end_time = time.time()
        elapsed_time = end_time - start_time
        self.assertAlmostEqual(elapsed_time, 0, places=1)

    def test_sleep_positive_seconds(self: unittest.TestCase) -> None:
        sleep_duration = 2
        start_time = time.time()
        sleep(sleep_duration)
        end_time = time.time()
        elapsed_time = end_time - start_time
        self.assertAlmostEqual(elapsed_time, sleep_duration, places=1)

    # The following are unit tests for the function `task_exit`.
    @patch("utils.logger_interface.Logger")
    @patch("tools.system_interface._get_stack")
    def test_task_exit(self: unittest.TestCase, mock_get_stack, mock_logger) -> None:
        mock_stack_frame = ("module_name", "file_name.py", 42, "function_name", "code")
        mock_get_stack.return_value = [mock_stack_frame]
        with self.assertRaises(IndexError):
            task_exit()
            mock_get_stack.assert_called_once()
            mock_logger.warn.assert_called_once_with(
                msg="Task exit called from file file_name.py line number 42."
            )
            sys.exit.assert_called_once_with(0)

    # The following are unit tests for the function `user`.
    @patch("tools.system_interface.getpass")
    def test_user(self: unittest.TestCase, mock_getpass) -> None:
        expected_username = "test_user"
        mock_getpass.getuser.return_value = expected_username
        result = user()
        mock_getpass.getuser.assert_called_once()
        self.assertEqual(result, expected_username)


# ----


if __name__ == "__main__":
    unittest.main()
