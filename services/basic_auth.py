import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from config import Config


security = HTTPBasic()


def apply_basic_auth(credentials: HTTPBasicCredentials = Depends(security)) -> None:
    is_username_correct = secrets.compare_digest(
        credentials.username, Config.BASIC_AUTH_USER
    )
    is_password_correct = secrets.compare_digest(
        credentials.password, Config.BASIC_AUTH_PASS
    )
    if not (is_username_correct and is_password_correct):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='incorrect username or password',
            headers={'WWW-Authenticate': 'Basic'},
        )
