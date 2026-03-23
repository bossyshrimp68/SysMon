import logging
import sys

sys.path.insert(0, "../src")  # so it will recognise src.collector

import src.logger as logger


def test_initiate_logging(mocker, tmp_path):
    log_file = tmp_path / "test.txt"
    mocker.patch("threading.Thread")  # don't start the thread

    logger.initiate_logging(str(log_file))

    assert logger.logger.hasHandlers()  # handler was added
    assert logger.logger.level == logging.INFO


def test_log_warning_no_data(mocker):
    mock_warning = mocker.patch.object(logger.logger, "warning")  # patch logger.warning
    logger.log_warning("warning")
    mock_warning.assert_called_once_with("warning", extra={})


def test_log_warning_with_data(mocker):
    mock_warning = mocker.patch.object(logger.logger, "warning")  # patch logger.warning
    logger.log_warning("warning", "extra")
    mock_warning.assert_called_once_with("warning", extra="extra")


def test_log_error_no_data(mocker):
    mock_warning = mocker.patch.object(logger.logger, "error")  # patch logger.error
    logger.log_error("error")
    mock_warning.assert_called_once_with("error", extra={})


def test_log_error_with_data(mocker):
    mock_warning = mocker.patch.object(logger.logger, "error")  # patch logger.error
    logger.log_error("error", "extra")
    mock_warning.assert_called_once_with("error", extra="extra")
