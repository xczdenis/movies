import time
from functools import wraps

from loguru import logger


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10, max_count=10):
    """
    Функция для повторного выполнения функции через некоторое время, если возникла ошибка.
    Использует наивный экспоненциальный рост времени повтора (factor) до граничного времени
    ожидания (border_sleep_time)

    Формула:
        t = start_sleep_time * 2^(n) if t < border_sleep_time
        t = border_sleep_time if t >= border_sleep_time
    :param start_sleep_time: начальное время повтора
    :param factor: во сколько раз нужно увеличить время ожидания
    :param border_sleep_time: граничное время ожидания
    :param max_count: максимальное количество попыток
    :return: результат выполнения функции
    """

    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            timeout = start_sleep_time
            count = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.error(e)
                    count += 1
                    if count == max_count:
                        break
                    time.sleep(timeout)
                    timeout = timeout * 2**factor
                    timeout = timeout if timeout < border_sleep_time else border_sleep_time
                    continue

        return inner

    return func_wrapper
