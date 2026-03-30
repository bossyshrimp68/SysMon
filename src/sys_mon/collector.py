import os.path
import threading
import time
import psutil
from psutil._common import bytes2human
from sys_mon import logger

"""
Using psutil, collector gets cpu usage, partitions data, ram stats and network upload/download speed. 
All run on separate threads.
"""

MEMORY_STATS_END_INDEX = 4
ROUND_UP_TO_DIGITS = 2
NETWORK_SPEED_INTERVAL = 5

cpu_update_interval = 0
cpu_data = {
    "average": 0.0,
    "cores": [],
}
ram_data = {
    "total": '',
    "used": '',
    "available": '',
    "percent": 0,
}
partitions_data = {}
network_data = {
    "upload": '',
    "download": ''
}


def update_cpu_data():
    """ Every interval - updates average cpu usage, and usage percentage for each core """
    cores = psutil.cpu_percent(interval=cpu_update_interval, percpu=True)
    total = sum(cores)
    average_usage = (total / len(cores)).__round__(ROUND_UP_TO_DIGITS)
    cores.sort(reverse=True)
    cpu_data["average"] = average_usage
    cpu_data["cores"] = cores


def update_ram_data():
    """ Updates ram statistics """
    memory_stats = psutil.virtual_memory()[:MEMORY_STATS_END_INDEX]
    total, available, percent, used = memory_stats
    total, available, used = convert_to_human_format([total, available, used])

    ram_data["total"] = total
    ram_data["available"] = available
    ram_data["percent"] = percent
    ram_data["used"] = used


def update_partitions_data():
    """ For each partition, updates path and statistics """
    partitions_stats = psutil.disk_partitions(all=True)  # if all=False returns physical devices only
    for partition in partitions_stats:
        path = partition.mountpoint
        disk_stats = get_disk_stats(path)
        if not disk_stats:
            partitions_data.pop(path, None)  # returns None in case path isn't in the data
        else:
            partitions_data[path] = get_disk_stats(path)


def get_disk_stats(path):
    """ Given a partition, returns its total, used, available memory, and used memory percentage """
    if not os.path.exists(path):
        logger.log_warning("Path doesn't exist", path)
        return None

    try:
        disk_stats = psutil.disk_usage(path)
    except OSError:
        logger.log_error("Partition disconnected", path)
        return None

    total, used, available, percent = disk_stats
    total, used, available = convert_to_human_format([total, used, available])

    return {
        "total": total,
        "used": used,
        "available": available,
        "percent": percent,
    }


def update_network_data():
    """ Updates delta bytes / delta seconds for upload and download speed, across all the interfaces combined """
    start_time = time.time()
    counter = psutil.net_io_counters(pernic=True)
    start_upload_bytes = sum(s.bytes_sent for s in counter.values())
    start_download_bytes = sum(s.bytes_recv for s in counter.values())

    time.sleep(NETWORK_SPEED_INTERVAL)

    end_time = time.time()
    counter = psutil.net_io_counters(pernic=True)
    end_upload_bytes = sum(s.bytes_sent for s in counter.values())
    end_download_bytes = sum(s.bytes_recv for s in counter.values())

    delta_time = end_time - start_time
    upload_speed = ((end_upload_bytes - start_upload_bytes) / delta_time).__round__(ROUND_UP_TO_DIGITS)
    download_speed = ((end_download_bytes - start_download_bytes) / delta_time).__round__(ROUND_UP_TO_DIGITS)

    network_data["upload"] = f"{upload_speed} Bps"
    network_data["download"] = f"{download_speed} Bps"


def convert_to_human_format(stats):
    formatted_stats = [bytes2human(stat) for stat in stats]
    return tuple(formatted_stats)


def initiate_collector(cpu_interval):
    global cpu_update_interval

    cpu_update_interval = cpu_interval

    cpu_thread = threading.Thread(target=cpu_thread_function, daemon=True)
    cpu_thread.start()

    ram_thread = threading.Thread(target=ram_thread_function, daemon=True)
    ram_thread.start()

    partition_thread = threading.Thread(target=partitions_thread_function, daemon=True)
    partition_thread.start()

    network_thread = threading.Thread(target=network_thread_function, daemon=True)
    network_thread.start()


def cpu_thread_function():
    while True:
        update_cpu_data()


def ram_thread_function():
    while True:
        update_ram_data()


def partitions_thread_function():
    while True:
        update_partitions_data()


def network_thread_function():
    while True:
        update_network_data()


def get_all_data():
    """ Returns all data as a dict, without cores with 0 usage """
    cpu_stats = get_cpu_data()
    cores_usage = cpu_stats["cores"].copy()
    no_zeros = [usage for usage in cores_usage if usage != 0.0]
    cpu_stats["cores"] = sorted(no_zeros, reverse=True)

    return {
        "cpu": cpu_stats,
        "ram": get_ram_data(),

        "partitions": get_partitions_data(),
        "network": get_network_data()
    }


def get_cpu_data():
    return cpu_data.copy()


def get_ram_data():
    return ram_data.copy()


def get_partitions_data():
    return partitions_data.copy()


def get_network_data():
    return network_data.copy()
