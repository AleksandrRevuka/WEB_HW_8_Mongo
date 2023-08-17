import asyncio

from functools import wraps
from datetime import datetime

from typing import Callable, Any


def async_timer():
    def wrapper(func: Callable) -> Callable:
        @wraps(func)
        async def wrapped(*args, **kwargs) -> Any:
            start = datetime.now()
            try:
                return await func(*args, **kwargs)
            finally:
                finish = datetime.now()
                print(f"statr: {start.time()} | finish: {finish.time()} | delta: {finish - start}")

        return wrapped

    return wrapper
