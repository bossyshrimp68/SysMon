from rich.align import Align
from rich.console import Group
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
import time
import collector
from rich.progress_bar import ProgressBar

"""
Creates a live layout to display the data from collector.
"""

DELAY_SECONDS = 2
REFRESH_PER_SECOND = 1
DEFAULT_COLOR = "#FF5ED6"  # pink
CPU_COLOR = "#A87EF7"  # purple
RAM_COLOR = "#81E3F7"  # blue
PARTITIONS_COLOR = "#C2F268"  # green
FINISHED_BAR_COLOR = "#FF213A"  # red


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
        border_style=DEFAULT_COLOR,
    )
    return header_panel


def footer():
    footer_message = "Press Ctrl + C to exit:)"
    footer_panel = Panel(
        footer_message,
        border_style=DEFAULT_COLOR,
    )
    return footer_panel


def cpu_panel():
    cpu_data = collector.get_cpu_data()

    cpu_table = Table(show_edge=False, border_style=CPU_COLOR)

    average_cpu_bar = ProgressBar(completed=cpu_data["average"], complete_style=DEFAULT_COLOR)
    cpu_table.add_column("Average", width=7)  # name
    cpu_table.add_column(average_cpu_bar, width=25)  # bar
    cpu_table.add_column(f"{cpu_data['average']}%", width=7)  # percentage

    for i, percent in enumerate(cpu_data["cores"]):
        cpu_table.add_row(
            f"Core{i}",
            ProgressBar(completed=percent, complete_style=DEFAULT_COLOR, finished_style=FINISHED_BAR_COLOR),
            f"{percent}%"
        )

    cpu_panel = Panel(
        Align.center(
            cpu_table
        ),
        title="CPU",
        border_style=CPU_COLOR,
    )
    return cpu_panel


def ram_panel():
    ram_table = Table(show_edge=False, show_header=False, border_style=RAM_COLOR)

    ram_data = collector.get_ram_data()

    ram_table.add_row("Total memory", str(ram_data["total"]))
    ram_table.add_row("Used memory", str(ram_data["used"]))
    ram_table.add_row("Available memory", str(ram_data["available"]))
    ram_table.add_row("Used percentage", f"{ram_data['percent']}%")

    bar = ProgressBar(
        total=100,
        completed=ram_data['percent'],
        complete_style=DEFAULT_COLOR,
        finished_style=FINISHED_BAR_COLOR
    )

    ram_panel = Panel(
        Group(
            Align.center(
                ram_table
            ),
            bar
        ),
        title="RAM",
        border_style=RAM_COLOR,
    )
    return ram_panel


def partitions_panel():
    partitions_table = Table(show_edge=False, border_style=PARTITIONS_COLOR)

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
            f"{data['percent']}%"
        )

    partition_panel = Panel(
        Align.center(
            partitions_table
        ),
        title="Partitions",
        border_style=PARTITIONS_COLOR,
    )
    return partition_panel


layout = create_layout()
layout["header"].update(header())
layout["footer"].update(footer())
layout["cpu"].update(cpu_panel())
layout["ram"].update(ram_panel())
layout["partitions"].update(partitions_panel())


def display():
    with Live(layout, refresh_per_second=REFRESH_PER_SECOND, screen=True):
        while True:
            layout["cpu"].update(cpu_panel())
            layout["ram"].update(ram_panel())
            layout["partitions"].update(partitions_panel())
            time.sleep(DELAY_SECONDS)
