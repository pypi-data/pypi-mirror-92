import argparse
from typing import Dict
import os
import datetime
from mission_control.telemetry_processor import *
from mission_control.telemetry_file_parser import *
from mission_control.alert_finder import *
from mission_control import models
from mission_control.output_formatter import *
from dataclasses import dataclass



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


def main():
  """
    Assumptions:
      - python file name length limitations
      - assuming file will always be readable (permissions)
      - no newline at the end of the input ASCII text file
      - python file name length limitations
      - files are not too big (file not too big to fit in memory)
  """

  parser = argparse.ArgumentParser(prog="mission_control")
  parser.add_argument(
      "filename", type=str, help="the satellite telemetry ASCII text file to operate on"
  )
  args = parser.parse_args()

  if os.path.exists(args.filename):
      with open(args.filename, "r") as inf:
          tel_parser = TelemetryFileParser(ingest_time_format="%Y%m%d %H:%M:%S.%f")
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
          telemetry_processor = TelemetryProcessor(
              parser=tel_parser, alert_finder=alert_finder, outputter=output_formatter
          )
          print(telemetry_processor.process(inf))
