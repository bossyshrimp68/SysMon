import os.path

import psutil
from psutil._common import bytes2human

SECONDS_BETWEEN_CALLS = 0.1  # so it doesn't measure in 0.0
MEMORY_STATS_END_INDEX = 4


def get_disk_stats(path):
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


def get_memory_stats():
    memory_stats = psutil.virtual_memory()
    formatted_stats = convert_to_human_format(memory_stats[:MEMORY_STATS_END_INDEX])
    total, available, percent, used = formatted_stats

    return {
        "total": total,
        "available": available,
        "percent": percent,
        "used": used
    }


def get_partitions_stats():
    partitions_stats = psutil.disk_partitions(all=True)  # if all=False returns physical devices only
    partitions = []
    for partition in partitions_stats:
        device, mountpoint, file_system, opts = partition

        partitions.append({
            "path": device,
            "mountpoint": mountpoint,
            "file system": file_system,
            "options": opts
        })
    return partitions


def get_cpu_percent():
    return psutil.cpu_percent(interval=SECONDS_BETWEEN_CALLS)  # reruns cpu percentage since last call


def convert_to_human_format(stats):
    """ bytes are written as int and percentage as floats. returns a new tuple with the bytes in human format"""
    formatted_stats = []
    for stat in stats:
        if type(stat) is int:
            stat = bytes2human(stat)
        formatted_stats.append(stat)
    return tuple(formatted_stats)
