from typing import Tuple

from fastapi import status
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from ratelimit import RateLimitMiddleware, Rule
from ratelimit.auths import EmptyInformation
from ratelimit.backends.redis import RedisBackend
from ratelimit.types import Scope
from redis.connection import ConnectionPool

from config import Config


class CustomRedisBackend(RedisBackend):
    def __init__(self):
        connection_kwargs = \
            ConnectionPool.from_url(Config.REDIS_URL).connection_kwargs
        options = {
            i: connection_kwargs.get(i) for i in
            ('host', 'port', 'db', 'password')
        }
        super().__init__(**options)


async def client_ip(scope: Scope) -> Tuple[str, str]:
    """
    instead of default ratelimit.auths.ip.client_ip method

    """
    ip = None
    if scope["client"]:
        ip, _ = tuple(scope["client"])
    for name, value in scope["headers"]:  # type: bytes, bytes
        if name == b"x-real-ip":
            ip = value.decode("utf8")
    if ip is None:
        raise EmptyInformation(scope)
    return ip, 'default'


def throttling_exception_handler(exc: Exception):
    return PlainTextResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content="too many requests due to rate-limiting policy",
    )


middleware_list = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
    ),
    Middleware(
        RateLimitMiddleware,
        authenticate=client_ip,
        backend=CustomRedisBackend(),
        config={
            r"^/v1/connected/realtime": [Rule(minute=10, block_time=60)],
            r"^/v1/connected/register": [Rule(minute=100, block_time=60)],
        },
        on_blocked=throttling_exception_handler
    ),
]
