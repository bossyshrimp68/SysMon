import tempfile

import sys_mon.report as report

FILE_DATA = (r'{"asctime": "2026-03-25 15:31:02,200", "levelname": "INFO", "cpu": {"average": 11.51, "cores": [54.7, '
             r'46.1, 38.9, 36.7]}, "ram": {"total": "15.6G", "used": "13.7G", "available": "1.9G", "percent": 87.9}, '
             r'"partitions": {"C:\\": {"total": "930.6G", "used": "551.8G", "available": "378.8G", "percent": '
             r'59.3}}}\n{"asctime": "2026-03-26 15:31:07,200", "levelname": "INFO", "cpu": {"average": 26.77, '
             r'"cores": [75.8, 66.9, 59.8, 57.7]}, "ram": {"total": "15.6G", "used": "13.8G", "available": "1.8G", '
             r'"percent": 88.2}, "partitions": {"C:\\": {"total": "930.6G", "used": "551.8G", "available": "378.8G", '
             r'"percent": 59.3}}}\n{"asctime": "2026-03-26 15:31:12,208", "levelname": "INFO", "cpu": {"average": '
             r'12.47, "cores": [79.4, 42.3, 41.2, 34.8]}, "ram": {"total": "15.6G", "used": "13.7G", "available": '
             r'"1.9G", "percent": 87.9}, "partitions": {"C:\\": {"total": "930.6G", "used": "551.8G", "available": '
             r'"378.8G", "percent": 59.3}, "D:\\": {"total": "930.6G", "used": "551.8G", "available": "378.8G", '
             r'"percent": 59.3}}}\n{"asctime": "2026-03-27 15:31:17,208", "levelname": "INFO", "cpu": {"average": '
             r'12.81, "cores": [75.2, 47.3, 34.6]}, "ram": {"total": "15.6G", "used": "13.7G", "available": "1.9G", '
             r'"percent": 88.0}, "partitions": {"C:\\": {"total": "930.6G", "used": "551.8G", "available": "378.8G", '
             r'"percent": 59.3}}}')

CORRECT_DATA = []

CORRECT_DATE = "2026-03-26"
INCORRECT_DATE = "2026-04-29"


def test_correct_get_data_by_date(mocker):
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(b'FILE_DATA')
    temp_file.close()

    correct_date_data = report.get_data_by_date(CORRECT_DATE, temp_file.name)
    assert correct_date_data == CORRECT_DATA
