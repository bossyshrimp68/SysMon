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


def cpu_panel():
    cpu_table = Table(show_edge=False)

    cpu_table.add_column("CPU core")
    cpu_table.add_column("Usage")

    cpu_data = collector.get_cpu_data()
    cpu_table.add_row("Average CPU usage", f"{cpu_data['average']}%")
    for i, percent in enumerate(cpu_data["cores"]):
        cpu_table.add_row(f"Core{i}", f"{percent}%")

    cpu_panel = Panel(
        Align.center(
            cpu_table
        ),
        title="CPU",
        border_style="bright_blue",
    )
    return cpu_panel


def ram_panel():
    ram_table = Table(show_edge=False, show_header=False)

    ram_data = collector.get_ram_data()
    ram_table.add_row("Total memory", str(ram_data["total"]))
    ram_table.add_row("Used memory", str(ram_data["used"]))
    ram_table.add_row("Available memory", str(ram_data["available"]))
    ram_table.add_row("Used percentage", f"{ram_data['percent']}%")

    ram_panel = Panel(
        Align.center(
            ram_table
        ),
        title="RAM",
        border_style="bright_blue",
    )
    return ram_panel


def partitions_panel():
    partitions_table = Table(show_edge=False)

    partitions_table.add_column("Path")
    partitions_table.add_column("Total memory")
    partitions_table.add_column("Used memory")
    partitions_table.add_column("Available memory")
    partitions_table.add_column("Used percentage")

    partition_data = collector.get_partitions_data()

    for partition, data in partition_data.items():
        partitions_table.add_row(
            partition,
            str(data["total"]),
            str(data["used"]),
            str(data["available"]),
            str(data["percent"])
        )

    partition_panel = Panel(
        Align.center(
            partitions_table
        ),
        title="Partitions",
        border_style="bright_blue",
    )
    return partition_panel


layout = create_layout()
layout["header"].update(header())
layout["footer"].update(footer())
layout["cpu"].update(cpu_panel())
layout["ram"].update(ram_panel())
layout["partitions"].update(partitions_panel())


def display():
    with Live(layout, refresh_per_second=REFRESH_PER_SECOND):
        while True:
            layout["cpu"].update(cpu_panel())
            layout["ram"].update(ram_panel())
            layout["partitions"].update(partitions_panel())
            time.sleep(DELAY_SECONDS)
