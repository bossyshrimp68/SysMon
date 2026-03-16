import threading

from rich.align import Align
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
import time

from rich.text import Text

import collector
from multiprocessing import Process

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
    layout["cpu"].split(
        Layout(name="cpu columns"),
        Layout(name="cpu data", ratio=3)
    )
    layout["left"].split(
        Layout(name="memory"),
        Layout(name="partitions")
    )
    return layout


def header():
    header_message = "System Monitoring CLI Tool"
    message_panel = Panel(
        Align.center(
            header_message
        ),
        border_style="bright_blue",
    )
    return message_panel


def footer():
    footer_message = "Press Ctrl + C to exit:)"
    message_panel = Panel(
        footer_message,
        border_style="bright_blue",
    )
    return message_panel


def cpu_panel():
    # left_column = "CPU core"
    # right_column = "usage"
    # columns = Text()

    grid = Table.grid(expand=True)
    grid.add_column("CPU core", justify="left")
    grid.add_column("Usage", justify="right")

    column_panel = Panel(
        grid,
        title="CPU",
        border_style="bright_blue",
    )

    return column_panel
    #
    # cpu_table = Table(show_edge=False, expand=True)
    # cpu_table.add_column("CPU core", justify="left")
    # cpu_table.add_column("Usage", justify="right")
    #
    # cpu_percentage = collector.get_cpu_percentage()
    # for i, percent in enumerate(cpu_percentage):
    #     cpu_table.add_row(f"Core{i}", f"{percent}%")
    #
    # message_panel = Panel(
    #     Align.center(
    #         cpu_table
    #     ),
    #     title="CPU",
    #     border_style="bright_blue",
    # )
    # return message_panel


def memory_panel():
    ram_table = Table(show_edge=False, show_header=False)

    memory_stats = collector.get_memory_stats()
    ram_table.add_row("Total memory", memory_stats["total"])
    ram_table.add_row("Used memory", memory_stats["used"])
    ram_table.add_row("Available memory", memory_stats["available"])
    ram_table.add_row("Used percentage", f"{memory_stats['percent']}%")
    message_panel = Panel(
        Align.center(
            ram_table
        ),
        title="RAM",
        border_style="bright_blue",
    )
    return message_panel


def partitions_panel():
    partitions_table = Table(show_edge=False)
    partitions_table.add_column("Path")
    partitions_table.add_column("Total memory")
    partitions_table.add_column("Used memory")
    partitions_table.add_column("Available memory")
    partitions_table.add_column("Used percentage")

    partitions_stats = collector.get_partitions_stats()
    for partition, stats in partitions_stats.items():
        partitions_table.add_row(
            partition,
            stats["total"],
            stats["used"],
            stats["available"],
            f"{stats['percent']}%")

    message_panel = Panel(
        Align.center(
            partitions_table
        ),
        title="Partitions",
        border_style="bright_blue",
    )
    return message_panel


layout = create_layout()
layout["header"].update(header())
layout["footer"].update(footer())
# layout["cpu"].update(cpu_panel())
layout["memory"].update(memory_panel())
layout["partitions"].update(partitions_panel())
layout["cpu"].update(Panel(cpu_panel(), title="CPU", border_style="bright_blue"))
layout["cpu columns"].update(cpu_panel())



def display():
    with Live(layout, refresh_per_second=REFRESH_PER_SECOND) as live:
        cpu_thread = threading.Thread(target=cpu_panel)
        cpu_thread.start()

        while True:
            # if not cpu_thread.is_alive():
            #     cpu_thread = threading.Thread(target=cpu_panel)
            #     layout["cpu"].update(cpu_panel())
            #     cpu_thread.start()

            layout["memory"].update(memory_panel())
            layout["partitions"].update(partitions_panel())
            time.sleep(DELAY_SECONDS)
