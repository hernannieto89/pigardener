import logging

import psutil
import RPi.GPIO as GPIO

from subprocess import Popen

logger = logging.getLogger(__name__)

SIMPLE_TIMER_PATH = "/home/pi/Desktop/pigardener/core/scripts/main_simple.py"

SIMPLE_TIMER_ARGS = "--pins {} --start_time {} --end_time {} --work_time {} --sleep_time {} --name {}"

SIMPLE_TIMER_EXC = "sudo python3 {} {} &".format(SIMPLE_TIMER_PATH, SIMPLE_TIMER_ARGS)


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
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()


def start_job(timer_instance):
    result = None
    try:
        process = Popen([SIMPLE_TIMER_EXC.format(timer_instance.data_pin,
                                                 timer_instance.start_time,
                                                 timer_instance.end_time,
                                                 timer_instance.work_time,
                                                 timer_instance.sleep_time,
                                                 timer_instance.name)], shell=True)
        result = process.pid + 1
        logger.info("Process {} started".format(result))
    except Exception as err:
        logger.info("Error starting job: {}".format(err))
    return result


def stop_job(timer_instance):
    try:
        kill(timer_instance.process_id)
        teardown([timer_instance.data_pin])
        logger.info("Process {} stopped".format(timer_instance.process_id))
    except Exception as err:
        logger.info("Error stopping job: {}".format(err))
