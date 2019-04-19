from multiprocessing import Process

from pigardener import TIMERS_DICT

from .main_simple import simple_timer


def start_job(timer_instance):
    process = Process(target=simple_timer, args=(timer_instance.data_pin, timer_instance.start_time, timer_instance.end_time,
                                                 timer_instance.work_time, timer_instance.sleep_time))
    process.start()
    print("START")
    print(process, process.is_alive())
    TIMERS_DICT[timer_instance.process_id] = process
    print("IM DONE")


def stop_job(timer_instance):
    print(TIMERS_DICT)
    print("STOP")
    process = TIMERS_DICT[timer_instance.process_id]
    process.terminate()
    TIMERS_DICT[timer_instance.process_id] = None
    print(process, process.is_alive())
    print("IM DONE")
