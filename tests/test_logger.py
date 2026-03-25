import ast
import tempfile
from pathlib import Path

import sys_mon.logger as logger


def initiate_logging(mocker):
    mocker.patch("threading.Thread")  # don't start the thread

    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.close()

    logger.initiate_logging(Path(temp_file.name))
    return temp_file.name


def read_json_line(file_path):
    with open(file_path, 'r') as file:
        content = file.readline()
    return ast.literal_eval(content)


def test_log_info(mocker):
    file_path = initiate_logging(mocker)

    mocker.patch("sys_mon.logger.start_time", -5)
    mocker.patch("sys_mon.collector.get_all_data", return_value={"data": "info"})

    logger.log_info()
    content = read_json_line(file_path)

    assert content.__contains__("asctime")
    assert content["levelname"] == "INFO"
    assert content["data"] == "info"


def test_log_warning_no_data(mocker):
    file_path = initiate_logging(mocker)

    logger.log_warning("warning")
    content = read_json_line(file_path)

    assert content.__contains__("asctime")
    assert content["levelname"] == "WARNING"
    assert content["message"] == "warning"


def test_log_warning_with_data(mocker):
    file_path = initiate_logging(mocker)

    logger.log_warning("warning", "extra")
    content = read_json_line(file_path)

    assert content.__contains__("asctime")
    assert content["levelname"] == "WARNING"
    assert content["message"] == "warning"
    assert content["extra"] == "extra"


def test_log_error_no_data(mocker):
    file_path = initiate_logging(mocker)

    logger.log_error("error")
    content = read_json_line(file_path)

    assert content.__contains__("asctime")
    assert content["levelname"] == "ERROR"
    assert content["message"] == "error"


def test_log_error_with_data(mocker):
    file_path = initiate_logging(mocker)

    logger.log_error("error", "extra")
    content = read_json_line(file_path)

    assert content.__contains__("asctime")
    assert content["levelname"] == "ERROR"
    assert content["message"] == "error"
    assert content["extra"] == "extra"
