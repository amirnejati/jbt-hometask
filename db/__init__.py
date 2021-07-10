from redis import Redis
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    scoped_session, sessionmaker
)
from sqlalchemy_utils import (
    create_database, database_exists
)

from config import Config


def init_db_connection():
    engine = create_engine(Config.SQLALCHEMY_DB_URL, pool_pre_ping=True)
    if not database_exists(Config.SQLALCHEMY_DB_URL):
        create_database(Config.SQLALCHEMY_DB_URL)
    session_factory = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=True,
        twophase=False)
    session = scoped_session(session_factory)
    return session


def init_redis_connection():
    return Redis.from_url(Config.REDIS_URL)


SessionLocal = init_db_connection()
Base = declarative_base()
SessionRedis = init_redis_connection()
