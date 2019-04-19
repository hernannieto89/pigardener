#!/usr/bin/python
"""
Simple timer - Main module.
"""
from .graceful_killer import GracefulKiller
from .helpers import teardown, got_to_work, setup, work, check_sudo,\
    continuous_work, get_remaining_time, get_time_goal


def simple_timer(timer_instance):
    """
    Simple timer.
    """
    check_sudo()

    start = timer_instance.start_time
    end = timer_instance.end_time
    pins = list(timer_instance.pins)
    work_time = timer_instance.work_time
    sleep_time = timer_instance.sleep_time
    continuous = sleep_time <= 0
    # setup GPIO
    setup(pins)
    try:
        killer = GracefulKiller()
        while True:
            on_time = got_to_work(start, end)
            if killer.kill_now:
                break
            if not continuous:
                if on_time:
                    work(work_time, sleep_time, pins)
            else:
                time_goal = get_time_goal(start, end, on_time)
                remaining_time = get_remaining_time(time_goal)
                continuous_work(remaining_time, pins, on_time)

        print("Program killed gracefully. Cleaning and exiting...")
    except KeyboardInterrupt:
        # End program cleanly with keyboard
        print("KeyboardInterrupt captured. Cleaning and exiting...")
    # Reset GPIO settings
    teardown(pins)
