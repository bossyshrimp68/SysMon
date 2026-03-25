import logging
import os.path
import tempfile

import sys_mon.logger
import sys_mon.logger as logger


def test_initiate_logging(mocker, tmp_path):
    log_file = tmp_path / "test.txt"
    mocker.patch("threading.Thread")  # don't start the thread

    logger.initiate_logging(str(log_file))

    assert logger.logger.hasHandlers()  # handler was added
    assert logger.logger.level == logging.INFO


def initiate_logging(mocker):
    file = tempfile.NamedTemporaryFile(mode='w')

    mocker.patch("threading.Thread")  # don't start the thread

    logger.initiate_logging(file.name)
    return file


def test_log_info(mocker):
    temp_dir = tempfile.TemporaryDirectory()
    temp_file = os.path.join(temp_dir.name, "logging.log")


    mocker.patch("threading.Thread")  # don't start the thread

    logger.initiate_logging(temp_file)

    mocker.patch("sys_mon.logger.start_time", -5)
    mocker.patch("sys_mon.collector.get_all_data", return_value="data")
    logger.log_info()
    logger.flush()
    with open(temp_file, 'r') as file:
        content = file.readline()
    print(content)
    # assert content == {"asctime": "2026-03-25 18:11:20,380", "levelname": "INFO"}
    temp_dir.cleanup()



def test_log_warning_no_data(mocker):
    mock_log = mocker.patch("sys_mon.logger.logger.log")
    logger.log_warning("warning")
    mock_log.assert_called_once_with(logging.WARNING, "warning")


def test_log_warning_with_data(mocker):
    mock_log = mocker.patch("sys_mon.logger.logger.log")
    logger.log_warning("warning", "extra")
    mock_log.assert_called_once_with(logging.WARNING, "warning", extra={"data": "extra"})


def test_log_error_no_data(mocker):
    mock_log = mocker.patch("sys_mon.logger.logger.log")
    logger.log_error("error")
    mock_log.assert_called_once_with(logging.ERROR, "error")


def test_log_error_with_data(mocker):
    mock_log = mocker.patch("sys_mon.logger.logger.log")
    logger.log_error("error", "extra")
    mock_log.assert_called_once_with(logging.ERROR, "error", extra={"data": "extra"})
