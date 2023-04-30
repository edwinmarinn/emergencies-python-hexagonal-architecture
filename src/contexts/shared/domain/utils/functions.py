import asyncio
import logging
from typing import Type

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
logger.addHandler(console_handler)


def retry_on_error(
    function=None,
    retries: int = 5,
    interval: int = 5,
    exception_class: Type[Exception] = Exception,
):
    def decorator(_function):
        async def wrapper(*args, **kwargs):
            retries_remaining = retries
            while retries_remaining:
                retries_remaining -= 1
                try:
                    return await _function(*args, **kwargs)
                except exception_class as e:
                    logger.info(
                        f"INFO: \t An {exception_class.__name__} exception has occurred, we are going to retry on {interval} seconds"
                    )
                    await asyncio.sleep(interval)
                    if retries_remaining == 0:
                        raise e

        return wrapper

    if function is not None:
        return decorator(function)

    return decorator
