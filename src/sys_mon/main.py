import argparse
import datetime
import os.path
import sys
import time

from sys_mon import collector, display, logger, report, threshold_monitor

"""
Excepts the flags from the parser, unites the logger, collector and display.
This class initiates all the threads and calls the display.
"""

DEFAULT_INTERVAL_VALUE = 2

parser = argparse.ArgumentParser()
parser.add_argument("--interval", required=False, type=int, help="Interval for cpu calculations, default is 2 seconds")
parser.add_argument("--log", required=False, type=str, help="A path for logging")
parser.add_argument("--cpu-warn", required=False, type=int, help="Threshold for total cpu percentage")
parser.add_argument("--mem-warn", required=False, type=int, help="Threshold for ram percentage")

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
    return None


def get_thresholds():
    cpu_threshold = valid_threshold(args.cpu_warn)
    ram_threshold = valid_threshold(args.mem_warn)
    return cpu_threshold, ram_threshold


def valid_threshold(threshold):
    if threshold:
        if not 0 < threshold < 100:
            print("Threshold must be between 0 and 100!")
            sys.exit(-1)
        return threshold
    return 100


def main():
    try:
        if args.command == 'report':
            display.report_display(generate_report())
        else:
            collector.initiate_collector(get_interval())
            logger.initiate_logging(get_log_path())
            threshold_monitor.initiate_monitor(get_thresholds())
            display.display()

    except KeyboardInterrupt:
        print("Closing...")
        if get_log_path():
            logger.flush()


if __name__ == "__main__":
    main()
