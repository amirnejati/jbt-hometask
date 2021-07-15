from typing import Any, Callable

from rq import Queue

from db import SessionRedis


def enqueue_task(func: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
    q = Queue(connection=SessionRedis)
    q.enqueue(func, *args, **kwargs)
    return
