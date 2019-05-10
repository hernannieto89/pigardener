import os
import signal
import psutil
import json
import RPi.GPIO as GPIO

from subprocess import Popen


SIMPLE_TIMER_TEMPLATE = "sudo python3 /home/pi/Desktop/pigardener/core/scripts/main_simple.py --pins {} --start_time {} --end_time {} --work_time {} --sleep_time {} &"


def teardown(pins):
    """
    Performs GPIO cleanup
    :return: None
    """
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    for i in pins:
        GPIO.setup(i, GPIO.OUT)
        GPIO.output(i, GPIO.HIGH)
        GPIO.cleanup(i)

def kill(proc_pid):
    #print(proc_pid)
    process = psutil.Process(proc_pid)
    #print(process)
    for proc in process.children(recursive=True):
        #print('children')
        #print(proc.pid)
        proc.kill()
    process.kill()

def start_job(timer_instance):
    process = Popen([SIMPLE_TIMER_TEMPLATE.format(timer_instance.data_pin,
                                                 timer_instance.start_time,
                                                 timer_instance.end_time,
                                                 timer_instance.work_time,
                                                 timer_instance.sleep_time)], shell=True)
    return process.pid + 1

def stop_job(timer_instance):
    try:
        kill(timer_instance.process_id)
        teardown([timer_instance.data_pin])
    except Exception as err:
        print(err)
