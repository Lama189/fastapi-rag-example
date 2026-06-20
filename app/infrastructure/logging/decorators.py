import time
import functools
import logging


logger = logging.getLogger("app_logger")


def log_duration(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.time()

        result = await func(*args, **kwargs)

        duration_ms = int((time.time() - start) * 1000)

        logger.info(
            f"{func.__name__}_finished",
            extra = { 
                "duration_ms": duration_ms,
            }
        )

        return result
    
    return wrapper