import threading

from rich.align import Align
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
import time
import collector

DELAY_SECONDS = 2
REFRESH_PER_SECOND = 1


def create_layout():
    layout = Layout(name="sysmon")

    layout.split(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
        Layout(name="footer", size=3)
    )
    layout["main"].split_row(
        Layout(name="left"),
        Layout(name="cpu"),
    )
    layout["left"].split(Layout(name="ram"), Layout(name="partitions"))
    return layout


def header():
    header_message = "System Monitoring CLI Tool"
    header_panel = Panel(
        Align.center(
            header_message
        ),
        border_style="bright_blue",
    )
    return header_panel


def footer():
    footer_message = "Press Ctrl + C to exit:)"
    footer_panel = Panel(
        footer_message,
        border_style="bright_blue",
    )
    return footer_panel


def update_cpu(cpu_data):
    while True:
        cpu_stats = collector.get_cpu_percentage()
        cpu_data.clear()
        for i, percent in enumerate(cpu_stats):
            cpu_data.append((f"Core{i}", f"{percent}%"))


def cpu_panel(cpu_data):
    cpu_table = Table(show_edge=False)
    cpu_table.add_column("CPU core")
    cpu_table.add_column("Usage")

    for data in cpu_data:
        core, usage = data
        cpu_table.add_row(core, usage)

    cpu_panel = Panel(
        Align.center(
            cpu_table
        ),
        title="CPU",
        border_style="bright_blue",
    )
    return cpu_panel


def update_ram(ram_data):
    while True:
        ram_stats = collector.get_ram_stats()
        ram_data.clear()
        ram_data.append(
            (ram_stats["total"],
             ram_stats["used"],
             ram_stats["available"],
             f"{ram_stats['percent']}%")
        )


def ram_panel(ram_data):
    ram_table = Table(show_edge=False, show_header=False)

    total, used, available, percent = ram_data[0]
    ram_table.add_row("Total memory", total)
    ram_table.add_row("Used memory", used)
    ram_table.add_row("Available memory", available)
    ram_table.add_row("Used percentage", percent)
    ram_panel = Panel(
        Align.center(
            ram_table
        ),
        title="RAM",
        border_style="bright_blue",
    )
    return ram_panel


def update_partitions(partitions_data):
    while True:
        partitions_stats = collector.get_partitions_stats()
        partitions_data.clear()
        for partition, stats in partitions_stats.items():
            partitions_data.append(
                (partition,
                 stats["total"],
                 stats["used"],
                 stats["available"],
                 f"{stats['percent']}%")
            )


def partitions_panel(partition_data):
    partitions_table = Table(show_edge=False)
    partitions_table.add_column("Path")
    partitions_table.add_column("Total memory")
    partitions_table.add_column("Used memory")
    partitions_table.add_column("Available memory")
    partitions_table.add_column("Used percentage")

    for data in partition_data:
        partition, total, used, available, percent = data
        partitions_table.add_row(partition, total, used, available, percent)

    partition_panel = Panel(
        Align.center(
            partitions_table
        ),
        title="Partitions",
        border_style="bright_blue",
    )
    return partition_panel


def initiate_threads(cpu_data, am_data, partition_data):
    cpu_thread = threading.Thread(target=update_cpu, args=(cpu_data,), daemon=True)
    cpu_thread.start()

    partition_thread = threading.Thread(target=update_partitions, args=(partition_data,), daemon=True)
    partition_thread.start()

    ram_thread = threading.Thread(target=update_ram, args=(ram_data,), daemon=True)
    ram_thread.start()


cpu_data = []
ram_data = []
partition_data = []

initiate_threads(cpu_data, ram_data, partition_data)

layout = create_layout()
layout["header"].update(header())
layout["footer"].update(footer())
layout["cpu"].update(cpu_panel(cpu_data))
layout["ram"].update(ram_panel(ram_data))
layout["partitions"].update(partitions_panel(partition_data))


def display():
    with Live(layout, refresh_per_second=REFRESH_PER_SECOND):
        while True:
            layout["cpu"].update(cpu_panel(cpu_data))
            layout["ram"].update(ram_panel(ram_data))
            layout["partitions"].update(partitions_panel(partition_data))
            time.sleep(DELAY_SECONDS)
