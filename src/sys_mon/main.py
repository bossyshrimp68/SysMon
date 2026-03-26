import argparse
import datetime
import os.path
import sys
import time

from sys_mon import collector, display, logger, report

"""
Excepts the flags from the parser, unites the logger, collector and display.
This class initiates all the threads and calls the display.
"""

DEFAULT_INTERVAL_VALUE = 2

parser = argparse.ArgumentParser()
parser.add_argument("--interval", required=False, type=int, help="Interval for cpu calculations, default is 2 seconds")
parser.add_argument("--log", required=False, type=str, help="A path for logging")

subparsers = parser.add_subparsers(dest='command', help="Subcommands")

report_parser = subparsers.add_parser('report', help="Generate reports from a given log file and date")
report_parser.add_argument('--date', required=True, type=str, help="Date for the report")
report_parser.add_argument("--rlog", required=True, type=str, help="Log file for the report")

args = parser.parse_args()


def generate_report():
    date = args.date
    log_path = args.rlog

    try:
        date = datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")  # format to double-digit, removes time
    except ValueError:
        print("Invalid date format! must be yyyy-mm-dd")
        sys.exit(-1)

    if not os.path.exists(log_path):
        print("Path doesn't exist!")
        sys.exit(-1)

    return report.generate_report(date, log_path)


def get_interval():
    interval = args.interval
    if interval:
        return interval
    else:
        return DEFAULT_INTERVAL_VALUE


def get_log_path():
    log_path = args.log
    if log_path:
        if not os.path.exists(log_path):
            print("Path doesn't exist!")
            sys.exit(-1)
    return log_path


def main():
    try:
        if args.command == 'report':
            display.report_display(generate_report())
        else:
            collector.initiate_threads(get_interval())
            logger.initiate_logging(get_log_path())
            display.display()

    except KeyboardInterrupt:
        print("Closing...")
        if get_log_path():
            logger.flush()


if __name__ == "__main__":
    main()
