# =========================================================================
# File: tools/tests/test_parser_interface.py
# Author: Henry R. Winterbottom
# Date: 14 August 2023
# Version: 0.0.1
# License: LGPL v2.1
# =========================================================================

"""

"""

# ----

import pytest
import os
import getpass
import time
import unittest
import tempfile
from unittest.mock import patch, MagicMock

from tools.fileio_interface import virtual_file
from tools.system_interface import _get_stack, app_path, chown, get_app_path, get_pid, sleep, task_exit, user
from utils.logger_interface import Logger

logger = Logger()

# ----


class TestSystemInterface(unittest.TestCase):
    """

    """

    def setUp(self: unittest.TestCase) -> None:
        self.temp_file = virtual_file().name

    # The following are unit tests for the function `app_path`.
    @patch('subprocess.Popen')
    def test_app_path_with_path(self, mock_popen):
        mock_output = b'app: /path/to/app\n'
        mock_popen.return_value.communicate.return_value = (mock_output, b'')
        result = app_path('app')
        self.assertEqual(result, '/path/to/app')

    # The following are unit tests for the function `chown`.
    @patch('subprocess.Popen')
    def test_app_path_without_path(self, mock_popen):
        mock_popen.return_value.communicate.return_value = (b'', b'')
        result = app_path('app')
        self.assertIsNone(result)

    @pytest.mark.order(1)
    def test_chown_invalid_user(self):
        user = 'nonexistentuser'
        group = 'groupname'
        with self.assertRaises(LookupError):
            chown(path=self.temp_file, user=user, group=group)

    @pytest.mark.order(2)
    def test_chown_invalid_group(self):
        user = 'username'
        group = 'nonexistentgroup'
        with self.assertRaises(LookupError):
            chown(path=self.temp_file, user=user, group=group)

    @pytest.mark.order(3)
    def test_chown_invalid_path(self):
        user = 'username'
        group = 'groupname'
        invalid_path = 'nonexistent_path'
        with self.assertRaises(LookupError):
            chown(path=invalid_path, user=user, group=group)

    @pytest.mark.order(4)
    def test_destroy_virtual_file(self) -> None:
        try:
            os.unlink(self.temp_file)
        except FileNotFoundError:
            pass

    # The following are unit tests for the function `get_app_path`.
    def test_existing_app(self):
        app_path = get_app_path("python")
        self.assertIsNotNone(app_path)
        self.assertTrue(app_path.endswith("python"))

    def test_non_existing_app(self):
        app_path = get_app_path("nonexistent_app")
        self.assertIsNone(app_path)

    def test_empty_app_name(self):
        app_path = get_app_path("")
        self.assertIsNone(app_path)

    def test_none_app_name(self):
        with self.assertRaises(TypeError):
            app_path = get_app_path(None)

    # The following are unit tests for the function `get_pid`.
    def test_get_pid(self):
        pid = get_pid()
        self.assertIsInstance(pid, int)
        self.assertGreater(pid, 0)

    # The following are unit tests for the function `sleep`.
    def test_sleep_zero_seconds(self):
        start_time = time.time()
        sleep(0)
        end_time = time.time()
        elapsed_time = end_time - start_time
        self.assertAlmostEqual(elapsed_time, 0, places=1)

    def test_sleep_positive_seconds(self):
        sleep_duration = 2
        start_time = time.time()
        sleep(sleep_duration)
        end_time = time.time()
        elapsed_time = end_time - start_time
        self.assertAlmostEqual(elapsed_time, sleep_duration, places=1)

    # The following are unit tests for the function `task_exit`.
    @patch('utils.logger_interface.Logger')
    @patch('tools.system_interface._get_stack')
    def test_task_exit(self, mock_get_stack, mock_logger):
        mock_stack_frame = ('module_name', 'file_name.py',
                            42, 'function_name', 'code')
        mock_get_stack.return_value = [mock_stack_frame]
        with self.assertRaises(IndexError):
            task_exit()
            mock_get_stack.assert_called_once()
            mock_logger.warn.assert_called_once_with(
                msg='Task exit called from file file_name.py line number 42.')
            sys.exit.assert_called_once_with(0)

    # The following are unit tests for the function `user`.
    @patch('tools.system_interface.getpass')
    def test_user(self, mock_getpass):
        expected_username = 'test_user'
        mock_getpass.getuser.return_value = expected_username
        result = user()
        mock_getpass.getuser.assert_called_once()
        self.assertEqual(result, expected_username)

# ----


if __name__ == "__main__":
    unittest.main()
