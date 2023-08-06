import unittest
import datetime
from mission_control.models import *
from mission_control.cli import *


class TestCLI(unittest.TestCase):
    def test_date_creation(self) -> None:
        """test_date_creation tests formatting for displaying datetime"""
        inp = datetime.datetime(2018, 1, 1, 23, 1, 38, 1000)
        expected = "2018-01-01T23:01:38.001Z"
        actual = format_time(inp)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
