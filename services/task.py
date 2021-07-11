from typing import Callable, Any

from rq import Queue

from db import SessionRedis


def enqueue_task(func: Callable, *args: Any, **kwargs: Any) -> None:
    q = Queue(connection=SessionRedis)
    q.enqueue(func, *args, **kwargs)
    return
