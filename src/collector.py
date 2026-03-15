import os.path

import psutil
from psutil._common import bytes2human

SECONDS_BETWEEN_CALLS = 0.1  # so it doesn't measure in 0.0


def print_disk_stats(disk_stats):
    formatted_stats = convert_to_human_format(disk_stats)
    total, used, free, percent = formatted_stats

    print(f"Total disk memory: {total}")
    print(f"Used disk memory: {used}")
    print(f"Available disk memory: {free}")
    print(f"Disk memory usage percent: {percent}%")


def print_memory_stats(memory_stats):
    formatted_stats = convert_to_human_format(memory_stats[:4])
    total, available, percent, used = formatted_stats

    print(f"Total memory: {total}")  # total physical memory excluding swap
    print(f"Available memory: {available}")
    print(f"Memory usage percent: {percent}%")
    print(f"Used memory: {used}")

def print_partitions_stats(partitions_stats):
    for partition in partitions_stats:
        device, mountpoint, file_system, opts = partition
        print(f"Device path: {device}")
        print(f"Mount point: {mountpoint}")
        print(f"file system: {file_system}")
        print(f"Options: {opts}")
        print()


def convert_to_human_format(stats):
    """ bytes are written as int and percentage as floats. returns a new tuple with the bytes in human format"""
    formatted_stats = []
    for stat in stats:
        if type(stat) is int:
            stat = bytes2human(stat)
        formatted_stats.append(stat)
    return tuple(formatted_stats)


while True:
    cpu_percent = psutil.cpu_percent(interval=SECONDS_BETWEEN_CALLS)  # reruns cpu percentage since last call

    path = input("Enter path:\n")
    if not os.path.exists(path):
        print("\nGiven path doesn't exist")
        break

    disk_stats = psutil.disk_usage(path)  # disk usage statistics for the given path
    memory_stats = psutil.virtual_memory()
    partitions_stats = psutil.disk_partitions(all=True) # if all=False returns physical devices only


    print_disk_stats(disk_stats)
    print()
    print_memory_stats(memory_stats)
    print()
    print_partitions_stats(partitions_stats)
