import json
import sys

"""
Receives a log file with json logs and a date. from the data in the file on that date returns:
- min, avg, max average cpu usage percentages
- min, avg, max used ram percentage
- min, avg, max used percentage for each partition
- min, avg, max network speed for upload and download
"""

DIGITS_TO_ROUND = 3


def generate_report(date: str, log_path: str):
    """ Returns a dict with the min, avg, max values percentages for cpu, ram and partitions in a given log file """
    data_list = get_data_by_date(date, log_path)
    cpu_usages, ram_usages, partitions_usages, network_speed = split_data(data_list)

    partition_min_avg_max = {}
    for partition, stats in partitions_usages.items():
        partition_min_avg_max[partition] = min_avg_max(stats, '%')
    print(network_speed["upload"])
    upload_speed = [float(s.split()[0]) for s in network_speed["upload"]]  # to get rid of ' Bps'
    download_speed = [float(s.split()[0]) for s in network_speed["download"]]  # to get rid of ' Bps'

    return {
        "cpu": min_avg_max(cpu_usages, '%'),
        "ram": min_avg_max(ram_usages, '%'),
        "partitions": partition_min_avg_max,
        "upload speed": min_avg_max(upload_speed, ' Bps'),
        "download speed": min_avg_max(download_speed, ' Bps')
    }


def get_data_by_date(date: str, log_path: str):
    """ Gets a file with json lines. returns the lines that match the given date """
    content_in_date = []
    with open(log_path, 'r') as log_file:
        for line in log_file:
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
    network_speed = {"upload": [], "download": []}

    for data in data_list:
        if data["levelname"] == "INFO":
            cpu_usages.append(data["cpu"]["average"])
            ram_usages.append(data["ram"]["percent"])
            if data["network"]["upload"]:  # initially they are both ""
                network_speed["upload"].append(data["network"]["upload"])
                network_speed["download"].append(data["network"]["download"])

            for partition, stats in data["partitions"].items():
                if partitions_usages.__contains__(partition):
                    partitions_usages[partition].append(stats["percent"])
                else:
                    partitions_usages[partition] = [stats["percent"]]

    return cpu_usages, ram_usages, partitions_usages, network_speed


def min_avg_max(data, unit):
    data.sort()

    minimum = data[0]
    average = (sum(data) / len(data)).__round__(DIGITS_TO_ROUND)
    maximum = data[-1]

    return (
        str(minimum) + unit,
        str(average) + unit,
        str(maximum) + unit
    )
