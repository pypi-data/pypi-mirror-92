import datetime
from typing import Dict
from dataclasses import dataclass
from mission_control import models


@dataclass(eq=True, frozen=True)
class SatelliteReadingFilterKey:
    """SatelliteReadingFilterKey is used to determine whether we care about a limit-breaking telemetry reading"""

    component: str
    threshold: models.Threshold


filter_map: Dict[SatelliteReadingFilterKey, bool] = {
    SatelliteReadingFilterKey(
        component="TSTAT", threshold=models.Threshold.BEYOND_UPPER
    ): True,
    SatelliteReadingFilterKey(
        component="BATT", threshold=models.Threshold.BENEATH_LOWER
    ): True,
}


def default_filter(
    reading: models.SatelliteStatusReading, threshold: models.Threshold
) -> bool:
    """default_filter makes sure we only care when TSTAT.raw_value > red_high_limit and BATT.raw_value < red_low_limit; it ensures that we discard entries for TSTAT.raw_value < red_low_limit and BATT.raw_value > red_high_limit"""

    return (
        filter_map.get(
            SatelliteReadingFilterKey(component=reading.component, threshold=threshold)
        )
        or False
    )


threshold_map: Dict[models.Threshold, str] = {
    models.Threshold.BENEATH_LOWER: "RED LOW",
    models.Threshold.BEYOND_UPPER: "RED HIGH",
}


def format_threshold(threshold: models.Threshold) -> str:
    """format_threshold formats an exceeding threshold entry as RED HIGH and a sub threshold entry as RED LOW for display"""

    return threshold_map[threshold]


def format_time(dt: datetime.datetime) -> str:
    """format_time formats datetimes for display according to the spec, ex: 2018-01-01T23:01:38.001Z"""

    return dt.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
