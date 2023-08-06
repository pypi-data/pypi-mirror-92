import unittest
import json
import datetime
from mission_control.message_processor import *
from unittest.mock import patch, mock_open


class TestMessageProcessing(unittest.TestCase):

    # test_parse_reading tests reading creation
    def test_parse_reading(self) -> None:
        inp = '20180101 23:01:05.001|1001|101|98|25|20|99.9|TSTAT'
        dt = datetime.datetime(2018, 1, 1, 23, 1, 5, 1000)
        expected = SatelliteStatusReading(
            timestamp=dt,
            satellite_id=1001,
            red_high_limit=101,
            yellow_high_limit=98,
            yellow_low_limit=25,
            red_low_limit=20,
            raw_value=99.9,
            component='TSTAT',
        )
        actual = parse_reading(inp)
        self.assertEqual(expected, actual)

    # test_date_creation tests date formatting for creating and displaying
    def test_date_creation(self) -> None:
        inp = "20180101 23:01:38.001"
        expected = "2018-01-01T23:01:38.001Z"
        dt = ingest_time(inp)
        actual = format_time(dt)
        self.assertEqual(expected, actual)

    # test_basic is the basic use case that's outlined in the spec
    def test_basic(self) -> None:
        mock_input = """
20180101 23:01:05.001|1001|101|98|25|20|99.9|TSTAT
20180101 23:01:09.521|1000|17|15|9|8|7.8|BATT
20180101 23:01:26.011|1001|101|98|25|20|99.8|TSTAT
20180101 23:01:38.001|1000|101|98|25|20|102.9|TSTAT
20180101 23:01:49.021|1000|101|98|25|20|87.9|TSTAT
20180101 23:02:09.014|1001|101|98|25|20|89.3|TSTAT
20180101 23:02:10.021|1001|101|98|25|20|89.4|TSTAT
20180101 23:02:11.302|1000|17|15|9|8|7.7|BATT
20180101 23:03:03.008|1000|101|98|25|20|102.7|TSTAT
20180101 23:03:05.009|1000|101|98|25|20|101.2|TSTAT
20180101 23:04:06.017|1001|101|98|25|20|89.9|TSTAT
20180101 23:04:11.531|1000|17|15|9|8|7.9|BATT
20180101 23:05:05.021|1001|101|98|25|20|89.9|TSTAT
20180101 23:05:07.421|1001|17|15|9|8|7.9|BATT
        """.strip()
        with patch("builtins.open", mock_open(read_data=mock_input)):
            with open("mockfile.dne") as inf:
                expected = json.loads(
                    """
                [
                    {
                        "satelliteId": 1000,
                        "severity": "RED HIGH",
                        "component": "TSTAT",
                        "timestamp": "2018-01-01T23:01:38.001Z"
                    },
                    {
                        "satelliteId": 1000,
                        "severity": "RED LOW",
                        "component": "BATT",
                        "timestamp": "2018-01-01T23:01:09.521Z"
                    }
                ]
                """
                )

                actual = process(inf)
                self.assertEqual(actual, expected)

    # test_empty_file tests what happens when there are no readings
    def test_empty_file(self) -> None:
        mock_input = """
        """.strip()
        with patch("builtins.open", mock_open(read_data=mock_input)):
            with open("mockfile.dne") as inf:
                expected = json.loads('[]')
                actual = process(inf)
                self.assertEqual(actual, expected)

    # test_no_alerts tests valid data but no 3-reading alerts within 5 minutes of one another
    def test_no_alerts(self) -> None:
        mock_input = """
20170101 23:01:05.001|1001|101|98|25|20|99.9|TSTAT
20170101 23:01:09.521|1000|17|15|9|8|8.8|BATT
20170101 23:01:26.011|1001|101|98|25|20|120.8|TSTAT
20180101 23:01:38.001|1000|101|98|25|20|102.9|TSTAT
20180101 23:01:05.001|1001|101|98|25|20|99.9|TSTAT
20180101 23:01:09.521|1000|17|15|9|8|8.8|BATT
20180101 23:01:26.011|1001|101|98|25|20|99.8|TSTAT
20180101 23:01:38.001|1000|101|98|25|20|99.9|TSTAT
20180101 23:01:49.021|1000|101|98|25|20|87.9|TSTAT
20180101 23:02:09.014|1001|101|98|25|20|89.3|TSTAT
20180101 23:02:10.021|1001|101|98|25|20|89.4|TSTAT
20180101 23:02:11.302|1000|17|15|9|8|8.7|BATT
20180101 23:03:03.008|1000|101|98|25|20|100.7|TSTAT
20180101 23:04:06.017|1001|101|98|25|20|89.9|TSTAT
20180101 23:04:11.531|1000|17|15|9|8|8.9|BATT
20180101 23:05:05.021|1001|101|98|25|20|89.9|TSTAT
20180101 23:05:07.421|1001|17|15|9|8|8.9|BATT
        """.strip()
        with patch("builtins.open", mock_open(read_data=mock_input)):
            with open("mockfile.dne") as inf:
                expected = json.loads('[]')
                actual = process(inf)
                self.assertEqual(actual, expected)

    # test_no_alerts tests when battery/thermostat hits the limit but does not exceed it
    def test_no_alerts_at_limit(self) -> None:
        mock_input = """
20170101 23:01:05.001|1001|101|98|25|20|99.9|TSTAT
20170101 23:01:09.521|1000|17|15|9|8|8|BATT
20170101 23:01:26.011|1001|101|98|25|20|101|TSTAT
20180101 23:01:38.001|1000|101|98|25|20|101|TSTAT
20180101 23:01:05.001|1001|101|98|25|20|99.9|TSTAT
20180101 23:01:09.521|1000|17|15|9|8|8|BATT
20180101 23:01:26.011|1001|101|98|25|20|101|TSTAT
20180101 23:01:38.001|1000|101|98|25|20|101|TSTAT
20180101 23:01:49.021|1000|101|98|25|20|87.9|TSTAT
20180101 23:02:09.014|1001|101|98|25|20|89.3|TSTAT
20180101 23:02:10.021|1001|101|98|25|20|89.4|TSTAT
20180101 23:02:11.302|1000|17|15|9|8|8|BATT
20180101 23:03:03.008|1000|101|98|25|20|100.7|TSTAT
20180101 23:04:06.017|1001|101|98|25|20|89|TSTAT
20180101 23:04:11.531|1000|17|15|9|8|8|BATT
20180101 23:05:05.021|1001|101|98|25|20|89.9|TSTAT
20180101 23:05:07.421|1001|17|15|9|8|8|BATT
        """.strip()
        with patch("builtins.open", mock_open(read_data=mock_input)):
            with open("mockfile.dne") as inf:
                expected = json.loads('[]')
                actual = process(inf)
                self.assertEqual(actual, expected)

    # test_overlapping_alerts tests when thermostat exceeds the limit but with overlapping readings over 5 minutes
    def test_overlapping_alerts(self) -> None:
        self.maxDiff = None
        mock_input = """
20180101 23:01:38.001|1000|101|98|25|20|102.9|TSTAT
20180101 23:01:49.021|1000|101|98|25|20|87.9|TSTAT
20180101 23:03:03.008|1000|101|98|25|20|102.7|TSTAT
20180101 23:05:05.009|1000|101|98|25|20|101.2|TSTAT
20180101 23:06:06.008|1000|101|98|25|20|102.7|TSTAT
20180101 23:07:07.009|1000|101|98|25|20|101.2|TSTAT
20180101 23:07:11.009|1000|101|98|25|20|101.2|TSTAT
20180101 23:08:06.008|1000|101|98|25|20|102.7|TSTAT
20180101 23:09:07.009|1000|101|98|25|20|101.2|TSTAT
        """.strip()
        with patch("builtins.open", mock_open(read_data=mock_input)):
            with open("mockfile.dne") as inf:
                expected = json.loads(
                    """
                [
                    {
                        "satelliteId": 1000,
                        "severity": "RED HIGH",
                        "component": "TSTAT",
                        "timestamp": "2018-01-01T23:01:38.001Z"
                    }
                ]
                """
                )

                actual = process(inf)
                self.assertEqual(actual, expected)

    # test_alerts_on_multiple_satellites tests when thermostat exceeds the limit on different satellites with different thresholds
    def test_alerts_on_multiple_satellites(self) -> None:
        mock_input = """
20180101 23:01:05.001|1001|100|98|25|20|99.9|TSTAT
20180101 23:01:05.017|1001|17|15|9|7|6.2|BATT
20180101 23:01:09.521|1000|17|15|9|8|7.8|BATT
20180101 23:01:26.011|1001|100|98|25|20|100.8|TSTAT
20180101 23:01:27.017|1001|17|15|9|7|6.2|BATT
20180101 23:01:38.001|1000|101|98|25|20|102.9|TSTAT
20180101 23:01:49.021|1000|101|98|25|20|87.9|TSTAT
20180101 23:02:09.014|1001|100|98|25|20|100.3|TSTAT
20180101 23:02:10.021|1001|100|98|25|20|100.4|TSTAT
20180101 23:02:11.017|1001|17|15|9|7|6.2|BATT
20180101 23:02:11.270|1001|17|15|9|7|8.2|BATT
20180101 23:02:11.302|1000|17|15|9|8|7.7|BATT
20180101 23:03:03.008|1000|101|98|25|20|102.7|TSTAT
20180101 23:03:05.009|1000|101|98|25|20|101.2|TSTAT
20180101 23:04:06.017|1001|100|98|25|20|89.9|TSTAT
20180101 23:04:06.029|1001|17|15|9|7|8.2|BATT
20180101 23:04:11.531|1000|17|15|9|8|7.9|BATT
20180101 23:05:05.021|1001|100|98|25|20|89.9|TSTAT
20180101 23:05:07.421|1001|17|15|9|7|7.9|BATT
        """.strip()
        with patch("builtins.open", mock_open(read_data=mock_input)):
            with open("mockfile.dne") as inf:
                expected = json.loads(
                    """
                [
                    {
                        "satelliteId": 1000,
                        "severity": "RED HIGH",
                        "component": "TSTAT",
                        "timestamp": "2018-01-01T23:01:38.001Z"
                    },
                    {
                        "satelliteId": 1001,
                        "severity": "RED HIGH",
                        "component": "TSTAT",
                        "timestamp": "2018-01-01T23:01:26.011Z"
                    },
                    {
                        "satelliteId": 1000,
                        "severity": "RED LOW",
                        "component": "BATT",
                        "timestamp": "2018-01-01T23:01:09.521Z"
                    },
                    {
                        "satelliteId": 1001,
                        "severity": "RED LOW",
                        "component": "BATT",
                        "timestamp": "2018-01-01T23:01:05.017Z"
                    }
                ]
                """
                )

                actual = process(inf)
                self.assertEqual(actual, expected)

    # test_almost_alert tests what happens when an alerting reading falls just outside the 5 minute window
    def test_almost_alert(self) -> None:
        mock_input = """
20180101 23:01:00.000|1000|101|98|25|20|100.0|TSTAT
20180101 23:02:00.000|1000|101|98|25|20|103.0|TSTAT
20180101 23:03:00.000|1000|101|98|25|20|102.0|TSTAT
20180101 23:04:00.000|1000|101|98|25|20|100.0|TSTAT
20180101 23:05:00.000|1000|101|98|25|20|100.0|TSTAT
20180101 23:06:00.000|1000|101|98|25|20|100.0|TSTAT
20180101 23:07:00.001|1000|101|98|25|20|102.0|TSTAT
20180101 23:08:00.000|1000|101|98|25|20|100.0|TSTAT
20180101 23:09:00.000|1000|101|98|25|20|100.0|TSTAT
        """.strip()
        with patch("builtins.open", mock_open(read_data=mock_input)):
            with open("mockfile.dne") as inf:
                expected = json.loads(
                    """
                []
                """
                )

                actual = process(inf)
                self.assertEqual(actual, expected)

    # test_daybreak_alert tests what happens when an alert breaks the day boundary
    def test_daybreak_alert(self) -> None:
        mock_input = """
20180101 23:59:56.000|1000|101|98|25|20|100.0|TSTAT
20180101 23:59:57.000|1000|101|98|25|20|103.0|TSTAT
20180101 23:59:58.000|1000|101|98|25|20|102.0|TSTAT
20180101 23:59:59.000|1000|101|98|25|20|100.0|TSTAT
20180101 00:00:00.000|1000|101|98|25|20|100.0|TSTAT
20180101 00:00:01.000|1000|101|98|25|20|100.0|TSTAT
20180101 00:00:02.000|1000|101|98|25|20|102.0|TSTAT
20180101 00:00:03.000|1000|101|98|25|20|100.0|TSTAT
20180101 00:00:04.000|1000|101|98|25|20|100.0|TSTAT
        """.strip()
        with patch("builtins.open", mock_open(read_data=mock_input)):
            with open("mockfile.dne") as inf:
                expected = json.loads(
                    """
                [
                    {
                        "satelliteId": 1000,
                        "severity": "RED HIGH",
                        "component": "TSTAT",
                        "timestamp": "2018-01-01T23:59:57.000Z"
                    }
                ]
                """
                )

                actual = process(inf)
                self.assertEqual(actual, expected)

    # test_custom_component tests what happens when an alert is used for a different component than thermostat and battery
    def test_custom_component(self) -> None:
        mock_input = """
20180101 23:59:56.000|1000|101|98|25|20|100.0|ALTMT
20180101 23:59:57.000|1000|101|98|25|20|103.0|ALTMT
20180101 23:59:58.000|1000|101|98|25|20|102.0|ALTMT
20180101 23:59:59.000|1000|101|98|25|20|100.0|ALTMT
20180101 00:00:00.000|1000|101|98|25|20|100.0|ALTMT
20180101 00:00:01.000|1000|101|98|25|20|100.0|ALTMT
20180101 00:00:02.000|1000|101|98|25|20|102.0|ALTMT
20180101 00:00:03.000|1000|101|98|25|20|100.0|ALTMT
20180101 00:00:04.000|1000|101|98|25|20|100.0|ALTMT
        """.strip()
        with patch("builtins.open", mock_open(read_data=mock_input)):
            with open("mockfile.dne") as inf:
                expected = json.loads(
                    """
                [
                    {
                        "satelliteId": 1000,
                        "severity": "RED HIGH",
                        "component": "ALTMT",
                        "timestamp": "2018-01-01T23:59:57.000Z"
                    }
                ]
                """
                )

                actual = process(inf)
                self.assertEqual(actual, expected)


# test for file permission failure (no permission to read)

if __name__ == "__main__":
    unittest.main()