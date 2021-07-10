from typing import List

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Session

from modules.connectivity import models
from modules.connectivity.api.rest.v1 import schemas
from modules.deps import get_db


def add_connectivity_invocation(
        db: Session,
        user1: schemas.OnlineAccount, user2: schemas.OnlineAccount,
        connected: bool, organisations: List[str] = None,
):
    if not db:  # in case of background-task call
        db = next(get_db())

    invocation = {'connected': connected, 'organisations': organisations}
    invocation = schemas.RegisterItem(**invocation).dict(exclude_none=True)

    user1, user2 = sorted((user1, user2))
    db_item = models.Connectivity(
        username1=user1, username2=user2, invocation=invocation,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_connectivity_invocations_history(
        db: Session,
        user1: schemas.OnlineAccount, user2: schemas.OnlineAccount,
) -> List[schemas.RegisterItem]:

    user1, user2 = sorted((user1, user2))
    connectivity_history = db.query(
        func.array_agg(
            models.Connectivity.invocation,
            type_=JSON(),
        ).label('invocations'),
    ).filter(
        models.Connectivity.username1 == user1,
        models.Connectivity.username2 == user2,
    ).group_by(
        models.Connectivity.username1,
        models.Connectivity.username2,
    ).first()

    return connectivity_history['invocations'] if connectivity_history else []
