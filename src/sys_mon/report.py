import json
import sys

"""
Receives a json log file and a date, and from the data in the file on that date returns:
- min, avg, max average cpu usage percentages
- min, avg, max used ram percentage
- min, avg, max used percentage for each partition
"""

DIGITS_TO_ROUND = 3


def generate_report(date: str, log_path: str):
    """ Returns a dict with the min, avg, max values percentages for cpu, ram and partitions in a given log file """
    data_list = get_data_by_date(date, log_path)
    cpu_usages, ram_usages, partitions_usages = split_data(data_list)

    partition_min_avg_max = {}
    for partition, stats in partitions_usages.items():
        partition_min_avg_max[partition] = min_avg_max(stats)

    return {
        "cpu": min_avg_max(cpu_usages),
        "ram": min_avg_max(ram_usages),
        "partitions": partition_min_avg_max
    }


def get_data_by_date(date: str, log_path: str):
    """ Gets a file with json lines. returns the lines that match the given date """
    content_in_date = []
    with open(log_path, 'r') as log_file:
        for line in log_file:
            print(line)
            try:
                log = json.loads(line)
                log_date = log["asctime"].split()[0]  # to get rid of the time
                if log_date == date:
                    content_in_date.append(log)
                if log_date > date:
                    break

            except Exception as e:
                print("Not a valid file. must contain only json lines")
                sys.exit(-1)

    if not content_in_date:
        print("Date isn't in log file")
        sys.exit(-1)
    return content_in_date


def split_data(data_list):
    """ returns a tuple with all cpu averages, all ram percentages, a dict with all percentages for each partition """
    cpu_usages = []
    ram_usages = []
    partitions_usages = {}

    for data in data_list:
        if data["levelname"] == "INFO":
            cpu_usages.append(data["cpu"]["average"])
            ram_usages.append(data["ram"]["percent"])
            for partition, stats in data["partitions"].items():
                if partitions_usages.__contains__(partition):
                    partitions_usages[partition].append(stats["percent"])
                else:
                    partitions_usages[partition] = [stats["percent"]]

    return cpu_usages, ram_usages, partitions_usages


def min_avg_max(data):
    data.sort()

    min = data[0]
    max = data[-1]
    avg = (sum(data) / len(data)).__round__(DIGITS_TO_ROUND)

    return f'{min}%', f'{avg}%', f'{max}%'
