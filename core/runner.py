from multiprocessing import Process

from pigardener import TIMERS_DICT

from .main_simple import simple_timer


def start_job(timer_instance):
    process = Process(target=simple_timer, args=(timer_instance.pins, timer_instance.start_time, timer_instance.end_time,
                                                 timer_instance.work_time, timer_instance.sleep_time))
    process.start()
    TIMERS_DICT[timer_instance.process_id] = process


def stop_job(timer_instance):
    process = TIMERS_DICT[timer_instance.process_id]
    process.terminate()
    process.join()
    TIMERS_DICT[timer_instance.process_id] = None
