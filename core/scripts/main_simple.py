#!/usr/bin/python
"""
Simple timer - Main module.
"""
import click
from helpers import got_to_work, setup, work, check_sudo,\
    continuous_work, get_remaining_time, get_time_goal

@click.command()
@click.option('--pins', type=click.INT, help='GPIO pins.')
@click.option('--start_time', type=click.INT, help='Start time.')
@click.option('--end_time', type=click.INT, help='End time.')
@click.option('--work_time', type=click.INT, help='Work time.')
@click.option('--sleep_time', type=click.INT, help='Sleep time.')
def simple_timer(pins, start_time, end_time, work_time, sleep_time):
    """
    Simple timer.
    """
    check_sudo()

    start = start_time
    end = end_time
    pins = [pins]
    work_time = work_time
    sleep_time = sleep_time
    continuous = sleep_time <= 0
    # setup GPIO
    setup(pins)
    while True:
        on_time = got_to_work(start, end)
        if not continuous:
            if on_time:
                work(work_time, sleep_time, pins)
        else:
            time_goal = get_time_goal(start, end, on_time)
            remaining_time = get_remaining_time(time_goal)
            continuous_work(remaining_time, pins, on_time)


if __name__ == '__main__':
    simple_timer()
