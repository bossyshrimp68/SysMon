import logging
import threading
import time
from pythonjsonlogger.json import JsonFormatter
from sys_mon import collector

"""
Logs the data from collector every logging interval, allows warning and error logging.
All in json format, with timestamps.
Main.py verifies that the path is correct.
"""

LOGGER_NAME = "sysmon"
LOG_INTERVALS_SECONDS = 5
HANDLER_INDEX = 0

logger = logging.getLogger(LOGGER_NAME)
start_time = time.time()


def initiate_logging(path=None):
    if path is None:
        logger.addHandler(logging.NullHandler())
        return

    handler = logging.FileHandler(filename=path)
    handler.setFormatter(JsonFormatter(
        "%(asctime)s %(levelname)s"
    ))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    logger_thread = threading.Thread(target=thread_function, daemon=True)
    logger_thread.start()


def log_info():
    global start_time
    current_time = time.time()
    if (current_time - start_time) >= LOG_INTERVALS_SECONDS:
        logger.info(collector.get_all_data())
        start_time = current_time


def thread_function():
    while True:
        log_info()


def log_warning(message, data=None):
    message = {"message": message}
    if data is None:
        logger.warning(message)
    else:
        logger.warning(message, extra={"extra": data})


def log_error(message, data=None):
    message = {"message": message}
    if data is None:
        logger.error(message)
    else:
        logger.error(message, extra={"extra": data})


def flush():
    logger.handlers[HANDLER_INDEX].flush()
