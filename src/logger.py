import logging
import threading
import time
from pythonjsonlogger.json import JsonFormatter
import collector

LOGGER_NAME = "sysmon"
LOG_INTERVALS_SECONDS = 5
HANDLER_INDEX = 0

logger = logging.getLogger(LOGGER_NAME)
start_time = time.time()


def initiate_logging(path):
    handler = logging.FileHandler(filename=path)
    handler.setFormatter(JsonFormatter(
        "%(asctime)s %(levelname)s"
    ))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    logger_thread = threading.Thread(target=log_info, daemon=True)
    logger_thread.start()


def log_info():
    global start_time
    while True:
        current_time = time.time()
        if (current_time - start_time) >= LOG_INTERVALS_SECONDS:
            logger.log(logging.INFO, collector.get_all_data())
            start_time = current_time


def log_warning(message, data=None):
    if not data:
        data = {}
    logger.warning(message, extra=data)


def log_error(message, data=None):
    if not data:
        data = {}
    logger.error(message, extra=data)


def flush():
    logger.handlers[HANDLER_INDEX].flush()
