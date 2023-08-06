from typing import Any, List, Dict, Callable
import json
import datetime
from . import models


class OutputFormatter(models.AbstractOutputFormatter):
    def __init__(
        self,
        sort_key: str,
        reverse: bool,
        indent: int,
        format_time_fn: Callable[[datetime.datetime], str],
        format_threshold_fn: Callable[[models.Threshold], str],
    ):
        self.sort_key = sort_key
        self.reverse = reverse
        self.indent = indent
        self.format_time_fn = format_time_fn
        self.format_threshold_fn = format_threshold_fn

    def format_alert(self, alert: models.SatelliteAlert) -> Dict[str, Any]:
        alert_dict: Dict[str, Any] = {}

        alert_dict["satelliteId"] = alert.satellite_id
        alert_dict["severity"] = self.format_threshold_fn(alert.severity)
        alert_dict["component"] = alert.component
        alert_dict["timestamp"] = self.format_time_fn(alert.timestamp)

        return alert_dict

    def format_alerts(self, alerts: List[models.SatelliteAlert]) -> str:
        """Formats alerts and returns a json string of the format:
        {
          "satelliteId": 1234,
          "severity": "severity",
          "component": "component",
          "timestamp": "timestamp"
        }
        Assumptions:
          output is sorted by timestamp (most recent first)
          output keys are ordered as shown above
        """
        alert_dicts: List[Dict[str, Any]] = []
        for alert in alerts:
            alert_dicts.append(self.format_alert(alert))
        # sort by key
        alert_dicts = sorted(
            alert_dicts, key=lambda k: k[self.sort_key], reverse=self.reverse
        )
        return json.dumps(alert_dicts, indent=self.indent)
