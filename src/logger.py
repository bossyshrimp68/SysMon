import logging
import main

LOG_FILE = main.get_log_path()


def configure_logger():
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

def get_logger():
    return logging.getLogger("sysmon")



