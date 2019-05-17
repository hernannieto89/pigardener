#!/usr/bin/python
"""
Simple timer - Main module.
"""
import logging
import click
from helpers import got_to_work, setup, work, check_sudo,\
    continuous_work, get_remaining_time, get_time_goal


@click.command()
@click.option('--pins', type=click.INT, help='GPIO pins.')
@click.option('--start_time', type=click.INT, help='Start time.')
@click.option('--end_time', type=click.INT, help='End time.')
@click.option('--work_time', type=click.INT, help='Work time.')
@click.option('--sleep_time', type=click.INT, help='Sleep time.')
@click.option('--name', type=click.STRING, help='Sleep time.')
def simple_timer(pins, start_time, end_time, work_time, sleep_time, name):
    """
    Simple timer.
    """
    check_sudo()
    logging.basicConfig(filename='/home/pi/Desktop/pigardener/core/logs/{}.log'.format(name), level=logging.DEBUG)
    logger = logging.getLogger(name)
    logger.info('Starting Simple Timer for {}'.format(name))
    start = start_time
    end = end_time
    pins = [pins]
    work_time = work_time
    sleep_time = sleep_time
    continuous = sleep_time <= 0
    # setup GPIO
    setup(pins)
    while True:
        on_time = got_to_work(start, end, logger=logger)
        if not continuous:
            logger.info('Cyclic work mode')
            if on_time:
                work(work_time, sleep_time, pins, logger=logger)
        else:
            logger.info('Continuous work mode')
            time_goal = get_time_goal(start, end, on_time)
            remaining_time = get_remaining_time(time_goal)
            logger.info('Working until: {}'.format(time_goal))
            continuous_work(remaining_time, pins, on_time, logger=logger)


if __name__ == '__main__':
    simple_timer()
