import os.path
import threading
from heapq import merge

import psutil
from psutil._common import bytes2human

import main

SECONDS_BETWEEN_CALLS = main.get_interval()  # default is 2 seconds
MEMORY_STATS_END_INDEX = 4
ROUND_UP_TO = 2

cpu_data = {
    "average": 0,
    "cores": []
}

ram_data = {
    "total": 0,
    "used": 0,
    "available": 0,
    "percent": 0
}

partitions_data = {}


def get_cpu_percentage(cpu_data):
    """ updates average cpu usage, and usage percentage for each core every interval """
    cores = psutil.cpu_percent(interval=SECONDS_BETWEEN_CALLS, percpu=True)
    total = 0
    for percent in cores:
        total += percent
    average_usage = (total / len(cores)).__round__(ROUND_UP_TO)
    cores.sort(reverse=True)
    cpu_data["average"] = average_usage
    cpu_data["cores"] = cores


def get_ram_stats(ram_data):
    """ updates ram status in a dict """
    memory_stats = psutil.virtual_memory()
    formatted_stats = convert_to_human_format(memory_stats[:MEMORY_STATS_END_INDEX])
    total, available, percent, used = formatted_stats

    ram_data["total"] = total
    ram_data["available"] = available
    ram_data["percent"] = percent
    ram_data["used"] = used


def get_partitions_stats(partitions_data):
    """ updates partition path and stats for every partition """
    partitions_stats = psutil.disk_partitions(all=True)  # if all=False returns physical devices only
    for partition in partitions_stats:
        path = partition.mountpoint
        partitions_data[path] = get_disk_stats(path)


def get_disk_stats(path):
    """ given a partition, returns its total, used, free memory, and used memory percentage """
    if not os.path.exists(path):
        raise FileNotFoundError(f"The file '{path}' does not exist!")

    disk_stats = psutil.disk_usage(path)  # disk usage statistics for the given path
    formatted_stats = convert_to_human_format(disk_stats)
    total, used, free, percent = formatted_stats

    return {
        "total": total,
        "used": used,
        "available": free,
        "percent": percent
    }


def convert_to_human_format(stats):
    """ bytes are written as int and percentage as floats. returns a new tuple with the bytes in human format """
    formatted_stats = []
    for stat in stats:
        if type(stat) is int:
            stat = bytes2human(stat)
        formatted_stats.append(stat)
    return tuple(formatted_stats)


def initiate_threads():
    cpu_thread = threading.Thread(target=cpu_thread_function, daemon=True)
    cpu_thread.start()

    ram_thread = threading.Thread(target=ram_thread_function, daemon=True)
    ram_thread.start()

    partition_thread = threading.Thread(target=partitions_thread_function, daemon=True)
    partition_thread.start()


def cpu_thread_function():
    while True:
        get_cpu_percentage(cpu_data)


def ram_thread_function():
    while True:
        get_ram_stats(ram_data)


def partitions_thread_function():
    while True:
        get_partitions_stats(partitions_data)


def get_cpu_data():
    return cpu_data.copy()


def get_ram_data():
    return ram_data.copy()


def get_partitions_data():
    return partitions_data.copy()


def get_all_data():
    """ returns all data as a dict, without cores with 0 usage """
    cpu_stats = get_cpu_data()
    cores_list = cpu_stats["cores"].copy()
    cpu_stats["cores"] = [x for x in cores_list if x != 0.0]

    return {
        "cpu": cpu_stats,
        "ram": get_ram_data(),
        "partitions": get_partitions_data()
    }
