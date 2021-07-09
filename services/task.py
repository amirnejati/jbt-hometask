from typing import Callable, Any

from rq import Queue

from db import SessionRedis


def enqueue_task(func: Callable, *args, **kwargs):
    q = Queue(connection=SessionRedis)
    q.enqueue(func, *args, **kwargs)
    return