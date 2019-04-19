from multiprocessing import Process

from pigardener import TIMERS_DICT

from .main_simple import simple_timer


def start_job(timer_instance):
    process = Process(target=simple_timer)
    process.start()
    TIMERS_DICT[timer_instance.process_id] = process


def stop_job(timer_instance):
    process = TIMERS_DICT[timer_instance.process_id]
    process.stop()
    TIMERS_DICT[timer_instance.process_id] = None
