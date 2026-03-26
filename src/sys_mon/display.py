from rich import box
from rich.align import Align
from rich.console import Group, Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
import time
from sys_mon import collector, report
from rich.progress_bar import ProgressBar

"""
Creates a live layout to display the data from collector.
"""

DELAY_SECONDS = 2
REFRESH_PER_SECOND = 1
DEFAULT_COLOR = "#33C6D7"  # blue
CPU_COLOR = "#FF70C3"  # pink
RAM_COLOR = "#90EB5C"  # green
PARTITIONS_COLOR = "#B86FD8"  # purple
FINISHED_BAR_COLOR = "#EF4854"  # red
DEFAULT_BOX_TYPE = box.DOUBLE_EDGE


def create_layout():
    layout = Layout(name="sysmon")
    layout.split_row(
        Layout(name="panels"),
        Layout(name="cpu", size=75),
    )
    layout["panels"].split(
        Layout(name="ram", ratio=1),
        Layout(name="partitions"),
        Layout(name="footer", size=5),
    )
    return layout


def footer():
    footer_message = "Press Ctrl + C to exit:)"
    footer_panel = Panel(
        footer_message,
        box=DEFAULT_BOX_TYPE,
        border_style=DEFAULT_COLOR,
        width=100,
        padding=(1, 2)
    )
    return footer_panel


def cpu_panel():
    cpu_table = Table(show_edge=False, border_style=CPU_COLOR, expand=True, leading=1)

    cpu_data = collector.get_cpu_data()

    average_cpu_bar = ProgressBar(completed=cpu_data["average"], complete_style=DEFAULT_COLOR)
    cpu_table.add_column("Average", width=7)  # core
    cpu_table.add_column(average_cpu_bar, width=25)  # bar
    cpu_table.add_column(f"{cpu_data['average']}%", width=7)  # percentage

    for i, percent in enumerate(cpu_data["cores"]):
        cpu_table.add_row(
            f"Core{i}",
            ProgressBar(completed=percent, complete_style=DEFAULT_COLOR, finished_style=FINISHED_BAR_COLOR),
            f"{percent}%",
        )

    cpu_panel = Panel(
        Align.center(cpu_table),
        padding=(2, 0),
        title="CPU",
        box=DEFAULT_BOX_TYPE,
        border_style=CPU_COLOR
    )
    return cpu_panel


def ram_panel():
    ram_table = Table(
        show_edge=False,
        show_header=False,
        border_style=RAM_COLOR,
        width=30,
        padding=(1, 1),
        expand=True
    )

    ram_data = collector.get_ram_data()

    ram_table.add_row("Total memory", str(ram_data["total"]))
    ram_table.add_row("Used memory", str(ram_data["used"]))
    ram_table.add_row("Available memory", str(ram_data["available"]))
    ram_table.add_row("Used percentage", f"{ram_data['percent']}%")

    bar = ProgressBar(
        total=100,
        completed=ram_data['percent'],
        complete_style=DEFAULT_COLOR,
        finished_style=FINISHED_BAR_COLOR,
        width=60,
    )

    ram_panel = Panel(
        Group(
            Align.center(ram_table),
            Align.center(bar)  # doesn't work if I align the group
        ),
        padding=(2, 0),
        expand=True,
        title="RAM",
        box=DEFAULT_BOX_TYPE,
        border_style=RAM_COLOR,
        width=100,
        height=20
    )
    return ram_panel


def partitions_panel():
    partitions_table = Table(show_edge=False, border_style=PARTITIONS_COLOR, expand=True, padding=(1, 2))

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
            f"{data['percent']}%",
        )

    partition_panel = Panel(
        Align.center(partitions_table),
        padding=(2, 0),
        title="Partitions",
        box=DEFAULT_BOX_TYPE,
        border_style=PARTITIONS_COLOR,
        width=100,
        height=20
    )
    return partition_panel


def report_display(report_data: dict):
    console = Console()
    report_table = Table(show_edge=False, border_style=CPU_COLOR, expand=True, padding=(1, 2))

    report_table.add_column()
    report_table.add_column("Minimum")
    report_table.add_column("Average")
    report_table.add_column("Maximum")

    for sector, stats in report_data.items():
        if sector == "partitions":
            for partition, values in stats.items():
                min, avg, max = values
                report_table.add_row(partition, min, avg, max)
        else:
            min, avg, max = stats
            report_table.add_row(sector, min, avg, max)

    report_panel = Panel(
        Align.center(report_table),
        expand=True,
        padding=(2, 0),
        title="Report",
        box=DEFAULT_BOX_TYPE,
        border_style=CPU_COLOR,
    )
    console.print(report_panel)


def display():
    layout = create_layout()
    layout["cpu"].update(cpu_panel())
    layout["ram"].update(ram_panel())
    layout["partitions"].update(partitions_panel())
    layout["footer"].update(footer())
    with Live(layout, refresh_per_second=REFRESH_PER_SECOND, screen=True):
        while True:
            layout["cpu"].update(cpu_panel())
            layout["ram"].update(ram_panel())
            layout["partitions"].update(partitions_panel())
            time.sleep(DELAY_SECONDS)
