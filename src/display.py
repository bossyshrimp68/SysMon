from rich.align import Align
from rich.console import Group
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
import time
import collector

from rich.text import Text

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
    layout["left"].split(Layout(name="memory"), Layout(name="partitions"))
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


def cpu_panel():
    """Some example content."""
    cpu_stats = Table(show_edge=False)
    cpu_stats.add_column("CPU core")
    cpu_stats.add_column("Usage")

    cpu_percentage = collector.get_cpu_percentage()
    for i, percent in enumerate(cpu_percentage):
        cpu_stats.add_row(f"Core{i}", f"{percent}%")

    message_panel = Panel(
        Align.center(
            cpu_stats
        ),
        title="CPU",
        border_style="bright_blue",
    )
    return message_panel


def memory_panel():
    ram_stats = Table(show_edge=False, show_header=False)
    ram_stats.add_row("Total memory", "1")
    ram_stats.add_row("Used memory", "1")
    ram_stats.add_row("Used percentage", "%")
    message_panel = Panel(
        Align.center(
            ram_stats
        ),
        title="RAM",
        border_style="bright_blue",
    )
    return message_panel


def partitions_panel():
    partitions_stats = Table(show_edge=False)
    partitions_stats.add_column("Path")
    partitions_stats.add_column("Total memory")
    partitions_stats.add_column("Used memory")
    partitions_stats.add_column("Available memory")
    partitions_stats.add_column("Used percentage")
    partitions_stats.add_row("/", "1", "1", "1", "%")
    partitions_stats.add_row("/", "1", "1", "1", "%")
    message_panel = Panel(
        Align.center(
            partitions_stats
        ),
        title="Partitions",
        border_style="bright_blue",
    )
    return message_panel


layout = create_layout()
layout["header"].update(header())
layout["cpu"].update(cpu_panel())
layout["memory"].update(memory_panel())
layout["partitions"].update(partitions_panel())

with Live(layout, refresh_per_second=REFRESH_PER_SECOND) as live:
    while True:
        layout["cpu"].update(cpu_panel())
        time.sleep(DELAY_SECONDS)
