# Path: src/utilities/runtime.py

import time

from loguru import logger


def show_runtime(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        logger.info(f"{func.__name__} executed in {time.time() - start_time} seconds")
        return result

    return wrapper
