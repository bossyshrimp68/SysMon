Collector - using the psutil library, this module is responsible for collecting the data. the collection of the CPU data is by an interval, 
so to not block the rest of the data collection all parts run on separate threads. so even though in python only one 
thread can use the interpreter at a time, while it's waiting for the interval to pass or for data to be retrieved from
psutil, another thread can run. in order to always have data to display,  