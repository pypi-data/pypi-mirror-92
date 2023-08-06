import argparse
from mission_control.main_helper import default_filter, format_threshold, format_time
import os
import datetime
from mission_control.telemetry_processor import *
from mission_control.telemetry_file_parser import *
from mission_control.alert_finder import *
from mission_control.models import *
from mission_control.output_formatter import *

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
