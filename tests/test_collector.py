# from src_.collector import *
#
# EXISTING_PATH = r"C:\Networks\work\python_practice\images\planes"
# NON_EXISTING_PATH = r"C:\Networks\work\python_practice\imagessssss\planes"
#
#
# partitions = get_partitions_stats()
# memory = get_ram_stats()
# disk = get_disk_stats(EXISTING_PATH)
# average_cpu, cpu_percent = get_cpu_percentage()
#
# print("Partitions:\n", partitions, end="\n\n")
#
# print("Memory:\n", memory, end="\n\n")
#
# print("Disk:\n", disk, end="\n\n")
#
# print("Average CPU usage:", average_cpu)
# print("CPU percentage per CPU:\n", cpu_percent, end="\n\n")
#
# try:
#     disk = get_disk_stats(NON_EXISTING_PATH)
# except FileNotFoundError as e:
#     print(e)
