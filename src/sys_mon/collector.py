import os.path
import threading

import psutil
from psutil._common import bytes2human

from sys_mon import logger

"""
Using psutil, collector gets cpu usage, partitions data and ram stats. 
All three run on separate threads.
"""

MEMORY_STATS_END_INDEX = 4
ROUND_UP_TO = 2

cpu_update_interval = 0

cpu_data = {
    "average": 0.0,
    "cores": []
}

ram_data = {
    "total": '',
    "used": '',
    "available": '',
    "percent": 0
}

partitions_data = {}


def update_cpu_percentage():
    """ updates average cpu usage, and usage percentage for each core every interval """
    cores = psutil.cpu_percent(interval=cpu_update_interval, percpu=True)
    total = sum(cores)
    average_usage = (total / len(cores)).__round__(ROUND_UP_TO)
    cores.sort(reverse=True)
    cpu_data["average"] = average_usage
    cpu_data["cores"] = cores


def update_ram_stats():
    """ updates ram status in a dict """
    memory_stats = psutil.virtual_memory()[:MEMORY_STATS_END_INDEX]
    total, available, percent, used = memory_stats
    total, available, used = convert_to_human_format([total, available, used])

    ram_data["total"] = total
    ram_data["available"] = available
    ram_data["percent"] = percent
    ram_data["used"] = used


def update_partitions_stats():
    """ updates partition path and stats for every partition """
    partitions_stats = psutil.disk_partitions(all=True)  # if all=False returns physical devices only
    for partition in partitions_stats:
        path = partition.mountpoint
        disk_stats = get_disk_stats(path)
        if not disk_stats:
            partitions_data.pop(path, None)  # returns None in case path isn't in the data
        else:
            partitions_data[path] = get_disk_stats(path)


def get_disk_stats(path):
    """ given a partition, returns its total, used, available memory, and used memory percentage """
    if not os.path.exists(path):
        logger.log_error("Path doesn't exist", path)
        return None

    try:
        disk_stats = psutil.disk_usage(path)  # disk usage statistics for the given path
    except OSError:
        logger.log_error("Partition disconnected", path)
        return None

    total, used, available, percent = disk_stats
    total, used, available = convert_to_human_format([total, used, available])

    return {
        "total": total,
        "used": used,
        "available": available,
        "percent": percent
    }


def convert_to_human_format(stats):
    formatted_stats = [bytes2human(stat) for stat in stats]
    return tuple(formatted_stats)


def initiate_threads(interval):
    global cpu_update_interval

    cpu_update_interval = interval

    cpu_thread = threading.Thread(target=cpu_thread_function, daemon=True)
    cpu_thread.start()

    ram_thread = threading.Thread(target=ram_thread_function, daemon=True)
    ram_thread.start()

    partition_thread = threading.Thread(target=partitions_thread_function, daemon=True)
    partition_thread.start()


def cpu_thread_function():
    while True:
        update_cpu_percentage()


def ram_thread_function():
    while True:
        update_ram_stats()


def partitions_thread_function():
    while True:
        update_partitions_stats()


def get_all_data():
    """ returns all data as a dict, without cores with 0 usage """
    cpu_stats = get_cpu_data()
    cores_usage = cpu_stats["cores"].copy()
    no_zeros = [usage for usage in cores_usage if usage != 0.0]
    cpu_stats["cores"] = sorted(no_zeros, reverse=True)

    return {
        "cpu": cpu_stats,
        "ram": get_ram_data(),
        "partitions": get_partitions_data()
    }


def get_cpu_data():
    return cpu_data.copy()


def get_ram_data():
    return ram_data.copy()


def get_partitions_data():
    return partitions_data.copy()
