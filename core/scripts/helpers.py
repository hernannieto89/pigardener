#!/usr/bin/python
"""
Simple timer - Helpers module.
"""
import os
import sys
import datetime
import time
import RPi.GPIO as GPIO

import Adafruit_DHT


DELAY_INTERVAL = 5
MAX_RETRIES = 5
FILE_NAME = '/home/pi/stadistics.txt'


def setup(pins):
    """
    GPIO setup.
    :param pins:
    :return: None
    """
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    for i in pins:
        GPIO.cleanup(i)
        GPIO.setup(i, GPIO.OUT)
        GPIO.output(i, GPIO.HIGH)


def teardown(pins):
    """
    Performs GPIO cleanup
    :return: None
    """
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    for i in pins:
        GPIO.output(i, GPIO.HIGH)
        GPIO.cleanup(i)


def got_to_work(start, end):
    """
    Ask if actual hour is within start - end range.
    :param start:
    :param end:
    :return: Boolean
    """
    now = datetime.datetime.now()
    now_time = now.time()
    start_time = datetime.time(start)
    end_time = datetime.time(end)

    if start_time < end_time:
        return now_time >= start_time and now_time <= end_time
    # Over midnight
    return now_time >= start_time or now_time <= end_time


def work(work_time, sleep_time, pins):
    """
    Performs job for work_time, sleeps for sleep_time.
    :param work_time:
    :param sleep_time:
    :param pins:
    :return: None
    """
    for i in pins:
        GPIO.setup(i, GPIO.IN)
        if GPIO.input(i) != GPIO.LOW:
            GPIO.setup(i, GPIO.OUT)
            GPIO.output(i, GPIO.LOW)
    time.sleep(work_time)
    for i in pins:
        GPIO.setup(i, GPIO.IN)
        if GPIO.input(i) != GPIO.HIGH:
            GPIO.setup(i, GPIO.OUT)
            GPIO.output(i, GPIO.HIGH)
    time.sleep(sleep_time)


def continuous_work(remaining_time, pins, on_time):
    """
    Performs job if needed and waits for remaining time.
    :param remaining_time:
    :param on_time:
    :param pins:
    :return: None
    """
    if on_time:
        for i in pins:
            GPIO.setup(i, GPIO.IN)
            if GPIO.input(i) != GPIO.LOW:
                GPIO.setup(i, GPIO.OUT)
                GPIO.output(i, GPIO.LOW)
    else:
        for i in pins:
            GPIO.setup(i, GPIO.IN)
            if GPIO.input(i) != GPIO.HIGH:
                GPIO.setup(i, GPIO.OUT)
                GPIO.output(i, GPIO.HIGH)
    #time.sleep(remaining_time)

def get_remaining_time(time_goal):
    """
    Returns remaining time in seconds between current time and specified goal.
    :param time_goal:
    :return: remaining_time
    """
    now = datetime.datetime.now()
    return (datetime.timedelta(hours=24) - (now - now.replace(hour=time_goal,
                                                              minute=0,
                                                              second=0,
                                                              microsecond=0)
                                            )
            ).total_seconds() % (24 * 3600)


def get_time_goal(start, end, on_time):
    """
    Gets current time goal.
    :param start:
    :param end:
    :param on_time:
    :return time_goal:
    """
    if on_time:
        time_goal = end
    else:
        time_goal = start

    return time_goal


def sanitize(args):
    """
    Sanitizes start_time and end_time parameters.
    :param args
    :return: None
    """
    datetime.time(args.start_time)
    datetime.time(args.end_time)


def check_sudo():
    """
    Checks for superuser privileges.
    :return: None
    """
    if os.getuid() != 0:
        print(sys.stderr, "You need to have root privileges to run this script.")
        sys.exit(1)


def setup_sensor(pin):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    sensor = Adafruit_DHT.DHT22
    return sensor


def setup_controller(pin):
    GPIO.cleanup(pin)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)


def get_ht(sensor, pin, log_level):
    tries = 0
    try:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        while out_of_range(humidity) or out_of_range(temperature):
            register_to_disk(temperature, humidity, "Out of Range - Beginning try {0}".format(tries), log_level)
            tries += 1
            time.sleep(DELAY_INTERVAL)
            humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
            if tries > MAX_RETRIES:
                raise Exception
    except Exception:
        humidity = 51.
        temperature = 101.
        register_to_disk(temperature, humidity, "Exception reading.", log_level)
    return humidity, temperature


def out_of_range(value):
    return value is None or value > 100


def heater_work(pin_heater, work_time, sleep_time, sensor, pin_dht, log_level, temperature_limit=None, humidity_limit=None):
    counter = 0

    GPIO.setup(pin_heater, GPIO.IN)
    if GPIO.input(pin_heater) != GPIO.LOW:
        GPIO.setup(pin_heater, GPIO.OUT)
        GPIO.output(pin_heater, GPIO.LOW)

    humidity, temperature = get_ht(sensor, pin_dht, log_level)
    register_to_disk(temperature, humidity, "Beginning to work.", log_level)
    while counter < work_time:
        if temperature_limit and temperature > temperature_limit:
            break
        elif humidity_limit and humidity > humidity_limit:
            break
        humidity, temperature = get_ht(sensor, pin_dht, log_level)
        counter += 30
        register_to_disk(temperature, humidity, "Working... Elapsed time: {0} seconds".format(counter), log_level)
        time.sleep(30)

    register_to_disk(temperature, humidity, "Work finished. Beginning to rest. {}".format(datetime.datetime.now()),
                     log_level)
    GPIO.setup(pin_heater, GPIO.IN)
    if GPIO.input(pin_heater) != GPIO.HIGH:
        GPIO.setup(pin_heater, GPIO.OUT)
        GPIO.output(pin_heater, GPIO.HIGH)

    counter = 0
    while counter < sleep_time:
        counter += 150
        time.sleep(150)
        humidity, temperature = get_ht(sensor, pin_dht, log_level)
        register_to_disk(temperature, humidity,
                         "Resting... Elapsed time: {0} seconds. {1}".format(counter, datetime.datetime.now()), log_level)


def register_to_disk(temperature, humidity, message, log_level):
    if log_level == 'INFO':
        with open(FILE_NAME, 'a') as the_file:
            the_file.write(message + '\n')
            the_file.write('Temp={0:0.1f}*  Humidity={1:0.1f}%\n'.format(temperature, humidity))
