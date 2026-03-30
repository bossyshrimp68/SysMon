# SysMon
> A CLI tool for monitoring system performance in real time.

SysMon tracks CPU, memory, disk and network metrics from your terminal, and presents the data on a live dashboard with
threshold, alerts, logging and daily reports.

---

![img](sys-mon-recording.gif)

---

## Features

- **Live dashboard** - continuously updating terminal display with color coded panels that turn red when thresholds 
are breached
- **Data tracking** - cpu tracking for each core alone and combined, memory and disk tracking (of every partition)
for total, used, available, percentage memory, plus upload and download network speed.
- **Threshold alerts** - desktop notifications every 25 seconds if CPU or RAM percentage exceed your desired threshold.
- **Logging** - appends timestamped readings to a file as json lines, logs errors and warnings as well.
- **Daily reports** - presents a min/avg/max analysis of every metric for a given log file and date.

---

## Installation

```bash
git clone https://github.com/bossyshrimp68/SysMon.git
cd SysMon
pip install sys-mon
```

---

## Usage

### Basic monitoring
```bash
sys-mon
```

### With logging
```bash
sys-mon --log /path/example.txt
```

### With a custom CPU updating interval (in seconds, default is 2)
```bash
sys-mon --interval 5
```

### With thresholds for CPU average usage or used RAM, represents a percentage 0-100
```bash
sys-mon --cpu-warn 50 --mem-warn 80
```

when a threshold is breached:
- its corresponding display panel will turn red
- an alert will appear every 25 seconds
- it will be logged as a warning

---

## Daily reports

Generate a min/avg/max analysis for a specific date in a log file:

```bash
sys-mon report --rlog log/file/path.txt --date 2026-3-30
```

- --rlog - path of the log file from witch to generate the report.
- --date - the date to report on, must be in the format y-m-d.

## All flags
| Flag         | Description                    | Default |
|--------------|--------------------------------|---------|
| `--log`      | Path to write the log file     | None    |
| `--interval` | CPU update interval in seconds | 2       |
| `--cpu-warn` | CPU usage threshold (0–100)    | 100     |
| `--mem-warn` | RAM usage threshold (0–100)    | 100     |
| `--rlog`     | Log path for the report        | None    |
| `--date`     | Date to report on in the rlog  | None    |
