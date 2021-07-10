from typing import Any

from fastapi import (
    Request, status
)
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse

from config import Config
from helper.custom_renderer import CustomErrResponse


class OnlineAccountException(Exception):
    def __init__(self, msg: Any):
        self.msg = msg


async def validation_exception_handler(
        request: Request, exc: RequestValidationError,
):
    return CustomErrResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=exc.errors(),
    )


async def online_account_exception_handler(
        request: Request, exc: OnlineAccountException,
):
    return CustomErrResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=exc.msg,
    )


async def server_error(request: Request, exc):
    if Config.DEBUG and str(exc):
        msg = str(exc)
    else:
        msg = 'Internal Server Error.'
    return PlainTextResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=msg,
    )


exc_handlers = {
    RequestValidationError: validation_exception_handler,
    OnlineAccountException: online_account_exception_handler,
    500: server_error,
}
