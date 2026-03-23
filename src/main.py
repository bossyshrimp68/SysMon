import argparse
import os.path

import display
import collector
import logger

"""
Excepts the flags from the parser, unites the logger, collector and display.
This class initiates all the threads and calls the display.
"""

DEFAULT_INTERVAL_VALUE = 2

parser = argparse.ArgumentParser()
parser.add_argument("--interval", help="set the polling frequency (default: 2 seconds)", type=int)
parser.add_argument("--log", help="log file path", type=str)
args = parser.parse_args()


def get_interval():
    interval = args.interval
    if interval:
        return interval
    else:
        return DEFAULT_INTERVAL_VALUE


def get_log_path():
    log_path = args.log
    if log_path:
        if os.path.exists(log_path):
            return log_path
        else:
            raise FileNotFoundError(f"The given file '{log_path}' does not exist!")
    return None


def main():
    collector.initiate_threads(get_interval())

    log_path = get_log_path()
    if log_path:
        logger.initiate_logging(log_path)

    try:
        display.display()
    except KeyboardInterrupt:
        print("Closing...")
        logger.flush()


if __name__ == "__main__":
    main()
