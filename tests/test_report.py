import tempfile

import sys_mon.report as report

"""
This class tests the functions in report.py. 
NOTICE!!! the constants rely on each other. if you change one, modify the rest accordingly.
"""

DATE = "2026-03-26"

FILE_DATA = (r'{"asctime": "2026-03-25 15:31:02,200", "levelname": "INFO", "cpu": {"average": 11.51, "cores": [54.7, '
             r'46.1, 38.9, 36.7]}, "ram": {"total": "15.6G", "used": "13.7G", "available": "1.9G", "percent": 87.9}, '
             r'"partitions": {"C:\\": {"total": "930.6G", "used": "551.8G", "available": "378.8G", "percent": '
             '59.3}}, "network": {"upload": "", "download": ""}}\n'
             r'{"asctime": "2026-03-26 15:31:07,200", "levelname": "INFO", "cpu": {"average": 26.77, "cores": [75.8, '
             r'66.9, 59.8, 57.7]}, "ram": {"total": "15.6G", "used": "13.8G", "available": "1.8G", "percent": 88.2}, '
             r'"partitions": {"C:\\": {"total": "930.6G", "used": "551.8G", "available": "378.8G", "percent": 59.3}}, '
             '"network": {"upload": "191.7 Bps", "download": "234.11 Bps"}}\n'
             r'{"asctime": "2026-03-26 15:31:12,208", "levelname": "INFO", "cpu": {"average": 12.47, "cores": [79.4, '
             r'42.3, 41.2, 34.8]}, "ram": {"total": "15.6G", "used": "13.7G", "available": "1.9G", "percent": 87.9}, '
             r'"partitions": {"C:\\": {"total": "930.6G", "used": "551.8G", "available": "378.8G", "percent": 59.3}, '
             r'"D:\\": {"total": "930.6G", "used": "551.8G", "available": "378.8G", "percent": 59.3}}, "network": {'
             '"upload": "150.61 Bps", "download": "223.45 Bps"}}\n'
             r'{"asctime": "2026-03-27 15:31:17,208", "levelname": "INFO", "cpu": {"average": 12.81, "cores": [75.2, '
             r'47.3, 34.6]}, "ram": {"total": "15.6G", "used": "13.7G", "available": "1.9G", "percent": 88.0}, '
             r'"partitions": {"C:\\": {"total": "930.6G", "used": "551.8G", "available": "378.8G", "percent": 59.3}}, '
             r'"network": {"upload": "191.7 Bps", "download": "234.11 Bps"}}')

DATA_BY_DATE = [
    {
        "asctime": "2026-03-26 15:31:07,200", "levelname": "INFO",
        "cpu": {"average": 26.77, "cores": [75.8, 66.9, 59.8, 57.7]},
        "ram": {"total": "15.6G", "used": "13.8G", "available": "1.8G", "percent": 88.2},
        "partitions": {
            "C:\\": {"total": "930.6G", "used": "551.8G", "available": "378.8G", "percent": 59.3}
        },
        "network": {"upload": "191.7 Bps", "download": "234.11 Bps"}
    },
    {
        "asctime": "2026-03-26 15:31:12,208", "levelname": "INFO",
        "cpu": {"average": 12.47, "cores": [79.4, 42.3, 41.2, 34.8]},
        "ram": {"total": "15.6G", "used": "13.7G", "available": "1.9G", "percent": 87.9},
        "partitions": {
            "C:\\": {"total": "930.6G", "used": "551.8G", "available": "378.8G", "percent": 59.3},
            "D:\\": {"total": "930.6G", "used": "551.8G", "available": "378.8G", "percent": 59.3}
        },
        "network": {"upload": "150.61 Bps", "download": "223.45 Bps"}
    }
]

SLICED_DATA = (
    [26.77, 12.47], [88.2, 87.9], {'C:\\': [59.3, 59.3], 'D:\\': [59.3]}, {'download': ['234.11 Bps', '223.45 Bps'],
                                                                           'upload': ['191.7 Bps', '150.61 Bps']}
)

FINAL_REPORT = {
    'cpu': ('12.47%', '19.62%', '26.77%'),
    'ram': ('87.9%', '88.05%', '88.2%'),
    'partitions': {
        'C:\\': ('59.3%', '59.3%', '59.3%'),
        'D:\\': ('59.3%', '59.3%', '59.3%')
    },
    'upload speed': ('150.61 Bps', '171.155 Bps', '191.7 Bps'),
    'download speed': ('223.45 Bps', '228.78 Bps', '234.11 Bps')
}


def test_generate_report():  # test all together
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    with open(temp_file.name, 'w') as log_file:
        log_file.write(FILE_DATA)

    final_report = report.generate_report(DATE, temp_file.name)
    assert final_report == FINAL_REPORT


def test_get_data_by_date():
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    with open(temp_file.name, 'w') as log_file:
        log_file.write(FILE_DATA)

    data = report.get_data_by_date(DATE, temp_file.name)

    assert data == DATA_BY_DATE


def test_split_data():
    sliced_data = report.split_data(DATA_BY_DATE)
    assert sliced_data == SLICED_DATA


def test_min_avg_max():
    stats = report.min_avg_max([1, 1, 2, 2], '%')
    assert stats == ('1%', '1.5%', '2%')
