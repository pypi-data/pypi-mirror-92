import unittest
import datetime
from mission_control.telemetry_file_parser import *
from mission_control.models import *


class TestTelemetryParser(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.parser = TelemetryFileParser(ingest_time_format="%Y%m%d %H:%M:%S.%f")

    def test_parse_reading(self) -> None:
        """test_parse_reading tests reading creation"""

        inp = "20180101 23:01:05.001|1001|101|98|25|20|99.9|TSTAT"
        dt = datetime.datetime(2018, 1, 1, 23, 1, 5, 1000)
        expected = SatelliteStatusReading(
            timestamp=dt,
            satellite_id=1001,
            red_high_limit=101,
            yellow_high_limit=98,
            yellow_low_limit=25,
            red_low_limit=20,
            raw_value=99.9,
            component="TSTAT",
        )
        actual = self.parser.parse_reading(inp)
        self.assertEqual(expected, actual)

    def test_date_parsing(self) -> None:
        """test_date_parsing tests date creation for parsing/analyzing"""

        inp = "20180101 23:01:38.001"
        expected = datetime.datetime(2018, 1, 1, 23, 1, 38, 1000)
        actual = self.parser.ingest_time(inp)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
