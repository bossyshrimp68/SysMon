import threading
import time
from plyer import notification

from sys_mon import collector

CPU_INTERVAL_SECONDS = 25
RAM_INTERVAL_SECONDS = 25
NOTIFICATION_TIMEOUT = 5
THREAD_SLEEP = 1

cpu_threshold = 0
ram_threshold = 0


def initiate_monitor(thresholds):
    global cpu_threshold, ram_threshold
    cpu_threshold, ram_threshold = thresholds

    monitoring_thread = threading.Thread(target=thread_func, daemon=True)
    monitoring_thread.start()


def cpu_breached():
    cpu_average = collector.get_cpu_data()["average"]
    return cpu_average > cpu_threshold


def ram_breached():
    ram_percentage = collector.get_ram_data()["percent"]
    return ram_percentage > ram_threshold


def notify(message):
    notification.notify(
        title="Threshold breach",
        message=message,
        timeout=NOTIFICATION_TIMEOUT
    )


def thread_func():
    cpu_timer = -CPU_INTERVAL_SECONDS
    ram_timer = -RAM_INTERVAL_SECONDS

    while True:
        if cpu_breached() and (time.time() - cpu_timer >= CPU_INTERVAL_SECONDS):
            notify(f"cpu percentage breached the threshold: {cpu_threshold}%")
            cpu_timer = time.time()

        if ram_breached() and (time.time() - ram_timer >= RAM_INTERVAL_SECONDS):
            notify(f"memory percentage breached the threshold: {ram_threshold}%")
            ram_timer = time.time()

        time.sleep(THREAD_SLEEP)
