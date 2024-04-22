# Path: src/utilities/runtime.py

import time

from loguru import logger


def show_runtime(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        total_time = time.perf_counter() - start_time
        logger.info(f"{func.__module__}.{func.__qualname__} Took {total_time:.4f} seconds")
        return result

    return wrapper
