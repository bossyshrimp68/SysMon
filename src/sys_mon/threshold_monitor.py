import asyncio
import signal
import threading

from sys_mon import collector

from desktop_notifier import DesktopNotifier, Urgency, Button, ReplyField, DEFAULT_SOUND

cpu_threshold = 0
ram_threshold = 0


def initiate_monitor(thresholds):
    global cpu_threshold, ram_threshold
    cpu_threshold, ram_threshold = thresholds

    cpu_thread = threading.Thread(target=thread_func, daemon=True)
    cpu_thread.start()


def cpu_breached():
    cpu_average = collector.get_cpu_data()["average"]
    return cpu_average > cpu_threshold


def ram_breached():
    ram_percentage = collector.get_ram_data()["percent"]
    return ram_percentage > ram_threshold


# def notify():


async def main() -> None:
    notifier = DesktopNotifier(app_name="System monitor")

    await notifier.send(
        title="Threshold breach",
        message="Et tu, Brute?",
        urgency=Urgency.Critical,
        buttons=[
            Button(
                title="Mark as read",
                on_pressed=lambda: print("Marked as read"),
            )
        ],
        reply_field=ReplyField(
            on_replied=lambda text: print("Brutus replied:", text),
        ),
        on_dispatched=lambda: print("Notification showing"),
        on_clicked=lambda: print("Notification clicked"),
        on_dismissed=lambda: print("Notification dismissed"),
        sound=DEFAULT_SOUND,
    )

    # # Run the event loop forever to respond to user interactions with the notification.
    stop_event = asyncio.Event()
    # loop = asyncio.get_running_loop()
    #
    # loop.add_signal_handler(signal.SIGINT, stop_event.set)
    # loop.add_signal_handler(signal.SIGTERM, stop_event.set)
    #
    await stop_event.wait()


def thread_func():
    while True:
        if cpu_breached():
            asyncio.run(main())
        if ram_breached():
            asyncio.run(main())
