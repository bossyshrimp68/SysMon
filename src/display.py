from rich.live import Live
from rich.table import Table
import time

DELAY_SECONDS = 2
REFRESH_PER_SECOND = 1

with Live(refresh_per_second=REFRESH_PER_SECOND) as live:

    while True:

        table = Table(title="System Metrics")

        table.add_column("Metric")

        table.add_column("Value")

        # ... populate with data from collector ...

        live.update(table)

        time.sleep(DELAY_SECONDS)
