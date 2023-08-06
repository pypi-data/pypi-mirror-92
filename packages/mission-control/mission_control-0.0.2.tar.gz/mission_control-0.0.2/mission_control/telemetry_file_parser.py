from typing import TextIO, List
from dataclasses import dataclass, asdict
import datetime
from . import models


class InvalidTelemetryRowError(RuntimeError):
    """Error generated if an invalid telemetry row is given."""


class TelemetryFileParser(models.AbstractTelemetryFileParser):
    def __init__(self, ingest_time_format: str) -> None:
        """Initializes a TelemetryFileParser with the ingest_time_format
        timestamp example format: "%Y%m%d %H:%M:%S.%f"
        """
        self.ingest_time_format = ingest_time_format

    def parse_reading(self, row: str) -> models.SatelliteStatusReading:
        """Parses a telemetry row in the format <timestamp>|<satellite-id>|<red-high-limit>|<yellow-high-limit>|<yellow-low-limit>|<red-low-limit>|<raw-value>|<component>
        timestamp example format: 20180101 23:01:05.001
        Raises:
            InvalidTelemetryRowError: If row is not in expected format
        """
        r = row.strip().split("|")
        dt = self.ingest_time(r[0])
        try:
            out = models.SatelliteStatusReading(
                timestamp=dt,
                satellite_id=int(r[1]),
                red_high_limit=int(r[2]),
                yellow_high_limit=int(r[3]),
                yellow_low_limit=int(r[4]),
                red_low_limit=int(r[5]),
                raw_value=float(r[6]),
                component=r[7],
            )
            return out
        except Exception as e:
            raise InvalidTelemetryRowError from e  # chain the exceptions so we don't lose the original

    def parse_file(self, inf: TextIO) -> List[models.SatelliteStatusReading]:
        """Parses a telemetry row and returns a list of readings
        Assumptions:
          each data row is ASCII text in the format: <timestamp>|<satellite-id>|<red-high-limit>|<yellow-high-limit>|<yellow-low-limit>|<red-low-limit>|<raw-value>|<component>
          data is timestamp sorted (earliest first)
          TextIO stream is not too large to fit into memory
        Raises:
            InvalidTelemetryRowError: If row is not in expected format
        """
        rows: List[models.SatelliteStatusReading] = []
        for line in inf:
            r = self.parse_reading(line)
            rows.append(r)
        return rows

    def ingest_time(self, t: str) -> datetime.datetime:
        """Ingests the timestamp and uses the instance's ingest_time_format attribute to determine the datetime."""
        return datetime.datetime.strptime(t, self.ingest_time_format)
