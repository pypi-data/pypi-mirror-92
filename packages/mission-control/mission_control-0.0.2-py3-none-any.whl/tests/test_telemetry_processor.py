import unittest
import json
import datetime
from mission_control.telemetry_processor import *
from mission_control.telemetry_file_parser import *
from mission_control.alert_finder import *
from mission_control.models import *
from mission_control.output_formatter import *
from unittest.mock import patch, mock_open
from mission_control.main_helper import *


class TestTelemetryProcessor(unittest.TestCase):
    """
    TestTelemetryProcessor is essentially an integration test class
    """

    def setUp(self) -> None:
        super().setUp()
        parser = TelemetryFileParser(ingest_time_format="%Y%m%d %H:%M:%S.%f")
        alert_finder = AlertFinder(
            interval=datetime.timedelta(0, 0, 0, 0, 5),
            frequency=3,
            filter_fn=default_filter,
        )
        output_formatter = OutputFormatter(
            sort_key="timestamp",
            reverse=True,
            indent=4,
            format_time_fn=format_time,
            format_threshold_fn=format_threshold,
        )
        self.telemetry_processor = TelemetryProcessor(
            parser=parser, alert_finder=alert_finder, outputter=output_formatter
        )

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

                actual = json.loads(self.telemetry_processor.process(inf))
                self.assertEqual(actual, expected)

    # test_empty_file tests what happens when there are no readings
    def test_empty_file(self) -> None:
        mock_input = """
        """.strip()
        with patch("builtins.open", mock_open(read_data=mock_input)):
            with open("mockfile.dne") as inf:
                expected = json.loads("[]")
                actual = json.loads(self.telemetry_processor.process(inf))
                self.assertEqual(actual, expected)

    # test_nonsensical_temp_high_python_int_limit_break tests what happens when the thermostat has nonsensical readings way too high and break python's int limitations
    def test_nonsensical_temp_high_python_int_limit_break(self) -> None:
        mock_input = """
20170101 23:01:05.001|1000|101|98|25|20|92233720368547758071922337203685477580719223372036854775807192233720368547758071|TSTAT
20170101 23:01:26.011|1001|101|98|25|20|92233720368547758071922337203685477580719223372036854775807192233720368547758071|TSTAT
20180101 23:01:05.001|1001|101|98|25|20|92233720368547758071922337203685477580719223372036854775807192233720368547758071|TSTAT
20180101 23:01:26.011|1001|101|98|25|20|92233720368547758071922337203685477580719223372036854775807192233720368547758071|TSTAT
20180101 23:01:38.001|1000|101|98|25|20|92233720368547758071922337203685477580719223372036854775807192233720368547758071|TSTAT
20180101 23:01:49.021|1000|101|98|25|20|92233720368547758071922337203685477580719223372036854775807192233720368547758071|TSTAT
20180101 23:02:09.014|1001|101|98|25|20|92233720368547758071922337203685477580719223372036854775807192233720368547758071|TSTAT
20180101 23:02:10.021|1001|101|98|25|20|92233720368547758071922337203685477580719223372036854775807192233720368547758071|TSTAT
        """.strip()
        with patch("builtins.open", mock_open(read_data=mock_input)):
            with open("mockfile.dne") as inf:
                expected = json.loads(
                    """
                [
                    {
                        "satelliteId": 1001,
                        "severity": "RED HIGH",
                        "component": "TSTAT",
                        "timestamp": "2018-01-01T23:01:05.001Z"
                    }
                ]
                """
                )
                actual = json.loads(self.telemetry_processor.process(inf))
                self.assertEqual(actual, expected)

    # test_nonsensical_temp_high tests what happens when the thermostat has nonsensical readings way too high
    def test_nonsensical_temp_high(self) -> None:
        mock_input = """
20170101 23:01:05.001|1000|101|98|25|20|9223372036854775807|TSTAT
20170101 23:01:26.011|1001|101|98|25|20|9223372036854775807|TSTAT
20180101 23:01:05.001|1001|101|98|25|20|9223372036854775807|TSTAT
20180101 23:01:26.011|1001|101|98|25|20|9223372036854775807|TSTAT
20180101 23:01:38.001|1000|101|98|25|20|9223372036854775807|TSTAT
20180101 23:01:49.021|1000|101|98|25|20|9223372036854775807|TSTAT
20180101 23:02:09.014|1001|101|98|25|20|9223372036854775807|TSTAT
20180101 23:02:10.021|1001|101|98|25|20|9223372036854775807|TSTAT
        """.strip()
        with patch("builtins.open", mock_open(read_data=mock_input)):
            with open("mockfile.dne") as inf:
                expected = json.loads(
                    """
                [
                    {
                        "satelliteId": 1001,
                        "severity": "RED HIGH",
                        "component": "TSTAT",
                        "timestamp": "2018-01-01T23:01:05.001Z"
                    }
                ]
                """
                )
                actual = json.loads(self.telemetry_processor.process(inf))
                self.assertEqual(actual, expected)

    # test_nonsensical_battery tests what happens when the battery has nonsensical readings (below 0)
    def test_nonsensical_battery(self) -> None:
        mock_input = """
20170101 23:01:09.521|1000|17|15|9|8|-22.8|BATT
20180101 23:01:09.522|1000|17|15|9|8|-21.6|BATT
20180101 23:02:11.302|1000|17|15|9|8|-25.4|BATT
20180101 23:04:11.531|1000|17|15|9|8|-28.2|BATT
20180101 23:05:07.421|1001|17|15|9|8|-18.0|BATT
        """.strip()
        with patch("builtins.open", mock_open(read_data=mock_input)):
            with open("mockfile.dne") as inf:
                expected = json.loads(
                    """
                [
                    {
                        "satelliteId": 1000,
                        "severity": "RED LOW",
                        "component": "BATT",
                        "timestamp": "2018-01-01T23:01:09.522Z"
                    }
                ]
                """
                )
                actual = json.loads(self.telemetry_processor.process(inf))
                self.assertEqual(actual, expected)

    # test_no_alerts_for_high_battery tests what happens when the battery is over limit
    def test_no_alerts_for_high_battery(self) -> None:
        mock_input = """
20170101 23:01:09.521|1000|17|15|9|8|22.8|BATT
20180101 23:01:09.522|1000|17|15|9|8|21.6|BATT
20180101 23:02:11.302|1000|17|15|9|8|25.4|BATT
20180101 23:04:11.531|1000|17|15|9|8|28.2|BATT
20180101 23:05:07.421|1001|17|15|9|8|18.0|BATT
        """.strip()
        with patch("builtins.open", mock_open(read_data=mock_input)):
            with open("mockfile.dne") as inf:
                expected = json.loads("[]")
                actual = json.loads(self.telemetry_processor.process(inf))
                self.assertEqual(actual, expected)

    # test_no_alerts_for_low_temperature tests what happens when the temperature is super low
    def test_no_alerts_for_low_temperature(self) -> None:
        mock_input = """
20170101 23:01:05.001|1001|101|98|25|20|0|TSTAT
20170101 23:01:26.011|1001|101|98|25|20|-20|TSTAT
20180101 23:01:38.001|1000|101|98|25|20|-373|TSTAT
20180101 23:01:05.001|1001|101|98|25|20|-200|TSTAT
20180101 23:01:26.011|1001|101|98|25|20|-200.5|TSTAT
20180101 23:01:38.001|1000|101|98|25|20|-45.5|TSTAT
20180101 23:01:49.021|1000|101|98|25|20|9.2|TSTAT
20180101 23:02:09.014|1001|101|98|25|20|7.2|TSTAT
20180101 23:02:10.021|1001|101|98|25|20|8.8|TSTAT
        """.strip()
        with patch("builtins.open", mock_open(read_data=mock_input)):
            with open("mockfile.dne") as inf:
                expected = json.loads("[]")
                actual = json.loads(self.telemetry_processor.process(inf))
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
                expected = json.loads("[]")
                actual = json.loads(self.telemetry_processor.process(inf))
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
                expected = json.loads("[]")
                actual = json.loads(self.telemetry_processor.process(inf))
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

                actual = json.loads(self.telemetry_processor.process(inf))
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

                actual = json.loads(self.telemetry_processor.process(inf))
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

                actual = json.loads(self.telemetry_processor.process(inf))
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

                actual = json.loads(self.telemetry_processor.process(inf))
                self.assertEqual(actual, expected)

    # test_custom_component tests what happens when an alert is used for a different component than thermostat and battery
    def test_custom_component(self) -> None:
        filter_dict: Dict[SatelliteReadingFilterKey, bool] = {
            SatelliteReadingFilterKey(
                component="ALTMT", threshold=models.Threshold.BEYOND_UPPER
            ): True
        }

        def custom_filter(
            reading: models.SatelliteStatusReading, threshold: models.Threshold
        ) -> bool:
            return (
                filter_dict.get(
                    SatelliteReadingFilterKey(
                        component=reading.component, threshold=threshold
                    )
                )
                or False
            )

        alert_finder = AlertFinder(
            interval=datetime.timedelta(0, 0, 0, 0, 5),
            frequency=3,
            filter_fn=custom_filter,
        )
        self.telemetry_processor.alert_finder = alert_finder

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

                actual = json.loads(self.telemetry_processor.process(inf))
                self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
