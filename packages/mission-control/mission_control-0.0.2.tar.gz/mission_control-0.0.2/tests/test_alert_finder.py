import unittest
import datetime
from mission_control.models import *
from mission_control.alert_finder import *
from mission_control.main_helper import *


class TestAlertFinder(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.alert_finder = AlertFinder(
            interval=datetime.timedelta(0, 0, 0, 0, 5),
            frequency=3,
            filter_fn=default_filter,
        )

    def test_custom_filtering(self) -> None:
        """test_custom_filtering tests custom filtration on the alert_finder"""

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

        self.alert_finder.filter_fn = custom_filter
        dt = datetime.datetime(2018, 1, 1, 23, 1, 38, 1000)
        inp: List[SatelliteStatusReading] = [
            SatelliteStatusReading(
                timestamp=dt + datetime.timedelta(0, 0),
                satellite_id=1001,
                red_high_limit=101,
                yellow_high_limit=98,
                yellow_low_limit=25,
                red_low_limit=20,
                raw_value=991.9,
                component="ALTMT",
            ),
            SatelliteStatusReading(
                timestamp=dt + datetime.timedelta(0, 1),
                satellite_id=1001,
                red_high_limit=101,
                yellow_high_limit=98,
                yellow_low_limit=25,
                red_low_limit=20,
                raw_value=991.9,
                component="ALTMT",
            ),
            SatelliteStatusReading(
                timestamp=dt + datetime.timedelta(0, 2),
                satellite_id=1001,
                red_high_limit=101,
                yellow_high_limit=98,
                yellow_low_limit=25,
                red_low_limit=20,
                raw_value=991.9,
                component="ALTMT",
            ),
        ]
        expected = [
            SatelliteAlert(
                satellite_id=1001,
                severity=Threshold.BEYOND_UPPER,
                component="ALTMT",
                timestamp=dt,
            )
        ]
        actual = self.alert_finder.find_alerts(inp)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
