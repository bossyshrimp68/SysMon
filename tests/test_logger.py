import logging
import sys_mon.logger as logger


def test_initiate_logging(mocker, tmp_path):
    log_file = tmp_path / "test.txt"
    mocker.patch("threading.Thread")  # don't start the thread

    logger.initiate_logging(str(log_file))

    assert logger.logger.hasHandlers()  # handler was added
    assert logger.logger.level == logging.INFO


def test_log_warning_no_data(mocker):
    mock_log = mocker.patch("logger.logger.log")
    logger.log_warning("warning")
    print(mock_log.assert_called_once_with(logging.WARNING, "warning"))


def test_log_warning_with_data(mocker):
    mock_log = mocker.patch("logger.logger.log")
    logger.log_warning("warning", "extra")
    mock_log.assert_called_once_with(logging.WARNING, "warning", extra={"data": "extra"})


def test_log_error_no_data(mocker):
    mock_log = mocker.patch("logger.logger.log")
    logger.log_error("error")
    mock_log.assert_called_once_with(logging.ERROR, "error")


def test_log_error_with_data(mocker):
    mock_log = mocker.patch("logger.logger.log")
    logger.log_error("error", "extra")
    mock_log.assert_called_once_with(logging.ERROR, "error", extra={"data": "extra"})
