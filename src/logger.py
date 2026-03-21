import logging
import threading
import time
import datetime

from rich import json

import collector

LOGGER_NAME = "sysmon"
LOG_INTERVALS_SECONDS = 5

logger = logging.getLogger(LOGGER_NAME)
start_time = time.time()


def log_as_json(data: dict):
    date_time = datetime.datetime.now()
    data["time"] = date_time.strftime("%Y-%m-%d %H:%M:%S")
    json_str = json.dumps(data)
    logger.log(logging.INFO, json_str)


def log():
    global start_time
    while True:
        current_time = time.time()
        if (current_time - start_time) >= LOG_INTERVALS_SECONDS:
            log_as_json(collector.get_all_data())
            start_time = current_time


def initiate_logging(path):
    logging.basicConfig(
        filename=path,
        level=logging.INFO,
        format="%(message)s",
    )
    logger_thread = threading.Thread(target=log, daemon=True)
    logger_thread.start()
