import threading
import time
import tkinter as tk
from tkinter import simpledialog

from sys_mon import collector

CPU_INTERVAL = 15
RAM_INTERVAL = 15

cpu_threshold = 0
ram_threshold = 0


def initiate_monitor(thresholds):
    global cpu_threshold, ram_threshold
    cpu_threshold, ram_threshold = thresholds

    cpu_thread = threading.Thread(target=thread_func, daemon=True)
    cpu_thread.start()


def cpu_breached():
    cpu_average = collector.get_cpu_data()["average"]
    return cpu_average > cpu_threshold


def ram_breached():
    ram_percentage = collector.get_ram_data()["percent"]
    return ram_percentage > ram_threshold


def get_user_input(response):
    if (response == "") or (response == None):  # None means user pressed cancel or dismiss
        return 0

    try:
        user_input = int(response)
        if 0 < user_input < 100:
            return user_input
        return None
    except ValueError:
        return None


def notify(message):
    root = tk.Tk()
    root.withdraw()  # hide the main window
    response = simpledialog.askstring(
        "Threshold breach",
        f"{message}. enter a new threshold if you wish",
    )
    user_input = get_user_input(response)
    if user_input is None:
        notify("Invalid input")

    root.destroy()
    return user_input


def thread_func():
    global cpu_threshold, ram_threshold

    cpu_timer = -CPU_INTERVAL
    ram_timer = -RAM_INTERVAL
    while True:
        if cpu_breached() and (time.time() - cpu_timer >= CPU_INTERVAL):
            response = notify(f"cpu threshold {cpu_threshold}% breached")
            cpu_timer = time.time()
            if response != 0:
                cpu_threshold = response

        if ram_breached() and (time.time() - ram_timer >= RAM_INTERVAL):
            response = notify(f"ram threshold {ram_threshold}% breached")
            ram_timer = time.time()
            if response != 0:
                ram_threshold = response
