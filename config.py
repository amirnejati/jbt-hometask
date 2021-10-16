from enum import Enum
import os
import secrets
from typing import Any, Dict, Optional

from pydantic import BaseSettings, RedisDsn, PositiveInt, PostgresDsn, validator


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class EnvModeEnum(str, Enum):
    testing = 'test'
    development = 'dev'
    staging = 'stg'
    production = 'prod'


ENV_MODE: str = os.environ.get('ENV_MODE', 'dev')


class Settings(BaseSettings):
    DEBUG: bool
    SECRET_KEY: str = secrets.token_urlsafe(32)

    ALLOWED_REQUESTS_PER_MINUTE: PositiveInt = 60
    THROTTLING_DENY_SECONDS: PositiveInt = 60

    GITHUB_ACCESS_TOKEN: str
    TWITTER_ACCESS_TOKEN: str
    BASIC_AUTH_USER: str
    BASIC_AUTH_PASS: str

    REDIS_URL: RedisDsn

    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DB_URL: Optional[PostgresDsn] = None

    @validator('SQLALCHEMY_DB_URL', pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme='postgresql',
            user=values.get('POSTGRES_USER'),
            password=values.get('POSTGRES_PASSWORD'),
            host=values.get('POSTGRES_HOST'),
            path=f'/{values.get("POSTGRES_DB") or ""}',
        )

    class Config:
        case_sensitive = True
        env_file = f'.env.{EnvModeEnum(ENV_MODE).value}'
        env_file_encoding = 'utf-8'


Config = Settings()
