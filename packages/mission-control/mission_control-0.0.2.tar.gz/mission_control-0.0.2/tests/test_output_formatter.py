import unittest
import datetime
from mission_control.models import *
from mission_control.output_formatter import *
from mission_control.main_helper import *


class TestOutputFormatter(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.output_formatter = OutputFormatter(
            sort_key="timestamp",
            reverse=True,
            indent=4,
            format_time_fn=format_time,
            format_threshold_fn=format_threshold,
        )

    # def test_parse_reading(self) -> None:
    #     """test_parse_reading tests reading creation"""

    #     inp = "20180101 23:01:05.001|1001|101|98|25|20|99.9|TSTAT"
    #     dt = datetime.datetime(2018, 1, 1, 23, 1, 5, 1000)
    #     expected = SatelliteStatusReading(
    #         timestamp=dt,
    #         satellite_id=1001,
    #         red_high_limit=101,
    #         yellow_high_limit=98,
    #         yellow_low_limit=25,
    #         red_low_limit=20,
    #         raw_value=99.9,
    #         component="TSTAT",
    #     )
    #     actual = self.parser.parse_reading(inp)
    #     self.assertEqual(expected, actual)

    def test_date_creation(self) -> None:
        """test_date_creation tests formatting for displaying datetime"""
        inp = datetime.datetime(2018, 1, 1, 23, 1, 38, 1000)
        expected = "2018-01-01T23:01:38.001Z"
        actual = format_time(inp)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
