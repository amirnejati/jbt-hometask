import logging
from typing import Any

from fastapi import Request, status
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import PlainTextResponse

from common.helper.custom_renderer import CustomErrResponse
from config import Config


logger = logging.getLogger('basic')


class OnlineAccountException(Exception):
    __slots__ = 'msg'

    def __init__(self, msg: Any):
        self.msg = msg


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> CustomErrResponse:
    return CustomErrResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=exc.errors(),
    )


async def online_account_exception_handler(
    request: Request,
    exc: OnlineAccountException,
) -> CustomErrResponse:
    return CustomErrResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=exc.msg,
    )


async def server_error(request: Request, exc: Any) -> PlainTextResponse:
    if Config.DEBUG and str(exc):
        msg = str(exc)
    else:
        msg = 'Internal Server Error.'
    return PlainTextResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=msg,
    )


async def auth_error(request: Request, exc: HTTPException) -> PlainTextResponse:
    logger.info(f'http-status-code: 401 , ip: {request.client.host} , {exc.detail}')
    return PlainTextResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content='not authenticated',
        headers={'WWW-Authenticate': 'Basic'},
    )


exc_handlers = {
    RequestValidationError: validation_exception_handler,
    OnlineAccountException: online_account_exception_handler,
    500: server_error,
    401: auth_error,
}
