from rich.live import Live

from rich.table import Table

import time

with Live(refresh_per_second=1) as live:

    while True:

        table = Table(title="System Metrics")

        table.add_column("Metric")

        table.add_column("Value")

        # ... populate with data from collector ...

        live.update(table)

        time.sleep(2)
