import unittest
import datetime
from mission_control.models import *
from mission_control.output_formatter import *
from mission_control.cli import *


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

if __name__ == "__main__":
    unittest.main()
