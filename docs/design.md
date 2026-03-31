## SysMon - design
> A thread-based CLI tool.

---

## Data flow

```
main                            <- parses CLI args, initializes threads, combines the logic of it all
  |
  |-- report                    <- reads from log file, generates a daily report
  |
  |-- collector                 <- gets and stores the system data
        |
        |-- display             <- reads from collector (or report), creates and updates a live dashboard
        |
        |-- logger              <- reads from collector, writes the data to a log file
        |
        |-- threshold_monitor   <- reads from collector, checks and alert if there is a threshold breach

```

---

## Modules

### `collector`
Responsible for getting and storing the system metrics using `psutil`. Each metric (CPU, RAM, partitions and network speed) 
runs on a separate thread, so no slow read or long interval blocks the others.

Due to pythons global interpreter lock, only one thread can use the interpreter at a time. that means that they don't
truly run parallel, but they allow another thread to run while they wait for the `psutil` response, so it isn't nearly
as blocking.

To ensure the display always has data to show and doesn't need to wait for collector to finish retrieving it, each 
metric is stored in a variable that is updated with new data by its thread. when other classes retrieve that data they
get a copy of each variable, so data is always available for display, logging or monitoring.

### `display`
Responsible for a continuously updating dashboard, presenting the data from collector. using `rich` it creates a display
split to different layouts - one for each metric and a footer. It also has a function for displaying the report, reading 
from the report module. both are called by main, according to the user input.

Because collector always holds the latest value, display always has data to show, and doesn't concern itself with
collector's state.

before updating the CPU and RAM panels, it checks with the threshold_monitor module if the thresholds have been breached,
and if so it turns the corresponding panel red.

### `logger`
Responsible for logging data, warnings and errors in one-line JSON readings. It runs on its own thread, that logs all 
the metrics from collector every logging interval with time stamps. 

It also provides functions for logging errors and warning - they log a message and optional extra data. This is used
in collector for disk errors, and in threshold_monitoring for threshold breaches. 

If the user doesn't want to log - a null handler is passed into the logger, so the logging of errors and warnings in
other modules don't depend on actual logging.

Each JSON line is formatted as such:
```JSON
{
  "asctime": "2026-03-31 11:48:04,990", 
  "levelname": "INFO", 
  "cpu": {"average": 23.83, "cores": [45.7, 11.3, 14.5]}, 
  "ram": {"total": "15.6G", "used": "13.5G", "available": "2.1G", "percent": 86.3}, 
  "partitions": {"C:\\": {"total": "930.6G", "used": "553.5G", "available": "377.1G", "percent": 59.5}}, 
  "network": {"upload": "2.4 Bps", "download": "3.6 Bps"}
}
```

### `threshold_monitor`
Responsible for monitoring and handling threshold breached. It runs on its own thread, and gets the thresholds from main
when initiated.

It Provides functions for checking whether CPU or RAM threshold were breached, that way display doesn't need to have any
collector logic, and collector doesn't need to concern itself with user input.

If a threshold has been breached - it alerts it every 25 seconds using `plyer`, and logs it as a warning with a message 
and the threshold as the extra data. 

### `report`
Responsible for generating a daily report given a log file and a date. It is independent of collector. It reads a log 
file with JSON lines only.
The data flow:
```
filters the relevant data by date
            |
            |_ splits the readings into their metric (CPU, RAM..)
                                |
                                |_ calculates the min/avg/max for each one

```

### `main`
Responsible for parsing, and the logic of all the modules combined. It implements the `argparse` parser, validates each 
flag and passes them to the relevant module. It initializes all the modules and their threads, calls the appropriate 
function in display (dashboard or report), and handles closing of the program.

---

## Threads
| Thread               | Module            | Target                                                                   |
|----------------------|-------------------|--------------------------------------------------------------------------|
| CPU updating         | collector         | Updates CPU data by an interval                                          |
| RAM updating         | collector         | Updates RAM data                                                         |
| Partition updating   | collector         | Updates disk data for each partition                                     |
| Network updating     | collector         | Updates network upload and download speed                                |
| Logging              | logger            | Logs the data from collector every interval                              |
| Threshold monitoring | threshold_monitor | Checks if the CPU or RAM thresholds were breached, alerts and logs if so |

---

## Testing
All the test files are written with `pytest`. In collector_test the `psutil` functions are patched, and in test_logger
and test_report the tests use temporary named files to simulate the log file.
