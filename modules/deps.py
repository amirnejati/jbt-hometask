from typing import Generator

from db import DBSession


def get_db() -> Generator:
    try:
        db = DBSession()
        yield db
    finally:
        db.close()
