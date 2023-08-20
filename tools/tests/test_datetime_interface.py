# =========================================================================
# File: tools/tests/test_datetime_interface.py
# Author: Henry R. Winterbottom
# Date: 17 August 2023
# Version: 0.0.1
# License: LGPL v2.1
# =========================================================================

"""


"""

# ----


# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

import time
import unittest
import datetime
from unittest.mock import patch
from tools.datetime_interface import compare_crontab, datestrcomps

from types import SimpleNamespace


# ----

class TestDateTimeInterface(unittest.TestCase):
    """


    """

    # The following are unit tests for the function `compare_crontab`.
    @patch('tools.datetime_interface._get_dateobj')
    @patch('croniter.croniter')
    def test_compare_crontab(self, mock_croniter, mock_get_dateobj):
        mock_dateobj = 'mock_date_object'
        mock_get_dateobj.return_value = mock_dateobj
        mock_croniter.return_value.match.return_value = True
        datestr = '2023-08-16'
        cronstr = '0 0 * * *'
        frmttyp = '%Y-%m-%d'
        result = compare_crontab(datestr, cronstr, frmttyp)
        mock_get_dateobj.assert_called_once_with(datestr, frmttyp)
        mock_croniter.match.assert_called_once()
        self.assertTrue(result)

    # The following are unit test for the function `datestrcomps`.
    @patch('tools.datetime_interface._get_dateobj')
    @patch('datetime.datetime')
    @patch('tools.parser_interface')
    @patch('utils.timestamp_interface')
    def test_datestrcomps(self, mock_timestamp_interface, mock_parser_interface,
                          mock_datetime, mock_get_dateobj):
        # Mock the _get_dateobj function to return a specific date object
        # mock_dateobj = datetime.datetime(2023, 8, 16, 12, 0, 0)
        # mock_get_dateobj.return_value = mock_dateobj

        # Mock datetime.datetime.strftime to return formatted values
        # mock_datetime.strftime.side_effect = lambda obj, fmt: str(obj)

        # Mock parser_interface.object_define and object_setattr
        # mock_date_comps_obj = SimpleNamespace()
        # mock_parser_interface.object_define.return_value = mock_date_comps_obj
        # mock_parser_interface.object_setattr.side_effect = lambda obj, key, value: setattr(
        #    obj, key, value)

        # Mock timestamp_interface.GENERAL and timestamp_interface.GLOBAL
        # mock_timestamp_interface.GENERAL = "2023-08-16 12:00:00"
        # mock_timestamp_interface.GLOBAL = "2023081612"

        frmttyp = '%Y-%m-%d %H:%M:%S'
        result = datestrcomps(datestr='2023-08-16 12:00:00', frmttyp=frmttyp)

        # mock_get_dateobj.assert_called_once_with(
        #    '2023-08-16 12:00:00', frmttyp)
        # mock_datetime.strftime.assert_called()
        # mock_parser_interface.object_define.assert_called_once()
        # self.assertEqual(result, mock_date_comps_obj)


# ----
if __name__ == "__main__":
    unittest.main()
