# SysMon
System Monitoring CLI Tool

Reads system metrics — CPU usage (per-core and aggregate), memory (used/total/percent), and disk usage (per-partition) at a configurable polling interval.
Displays live stats — Renders a continuously-updating terminal dashboard with color-coded indicators (green/yellow/red based on thresholds).
Logs to file — Appends timestamped readings to a structured log file (CSV or JSON).
Generates reports (stretch goal) — Produces a daily summary with averages, peaks, and any threshold breaches.

how to use:
1. git clone https://github.com/bossyshrimp68/SysMon.git
2. cd SysMon
3. pip install sys-mon
4. sys-mon --interval [int] --log [log path] (both are optional, default interval is 2 seconds)