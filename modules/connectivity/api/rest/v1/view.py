import asyncio
from typing import Any, List

from fastapi import APIRouter, Response, status, BackgroundTasks, Depends
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Session


from modules import deps
from services import GithubFactory, TwitterFactory
from modules.connectivity.api.rest.v1 import schemas
from modules.connectivity.models import Connectivity


router = APIRouter()


@router.get(
    '/realtime/{dev1}/{dev2}',
    tags=['➼ realtime endpoint'],
    status_code=200,
    description=(
        'For a given pair of developers checks whether they are connected or '
        'not. They are considered connected if they follow each other on '
        'Twitter, and they have at least one Github organisation in common.'
    ),
    response_model=schemas.RealtimeItem,
    response_model_exclude_unset=True,
)
async def realtime(
        dev1: schemas.OnlineAccount,
        dev2: schemas.OnlineAccount,
        response: Response,
        background_tasks: BackgroundTasks,
        db: Session = Depends(deps.get_db),
) -> Any:
    orgs_and_errs, friendship_and_errs = await asyncio.gather(
        GithubFactory().organisations_in_common(dev1, dev2),
        TwitterFactory().check_friendship(dev1, dev2),
    )
    common_orgs, errs1 = orgs_and_errs
    have_friendship, errs2 = friendship_and_errs

    data = {
        'connected': True, 'organisations': common_orgs,
    } if common_orgs and have_friendship else \
        {'connected': False}
    errors = errs1 + errs2

    if errors:
        response.status_code = status.HTTP_404_NOT_FOUND

    return {'data': data, 'errors': errors}


@router.get(
    '/register/{dev1}/{dev2}',
    tags=['➼ register endpoint'],
    status_code=200,
    description=(
        'Returns a history of all previous invocations of the '
        '"realtime endpoint" for a given pair of developers.'
    ),
    response_model=List[schemas.RegisterItem],
    response_model_exclude_unset=True,
)
async def register(
        dev1: schemas.OnlineAccount,
        dev2: schemas.OnlineAccount,
        db: Session = Depends(deps.get_db),
) -> Any:

    user1, user2 = sorted((dev1, dev2))
    connectivity_history = db.query(
        func.array_agg(
            Connectivity.invocation,
            type_=JSON(),
        ).label('invocations'),
    ).filter(
        Connectivity.username1 == user1,
        Connectivity.username2 == user2,
    ).group_by(
        Connectivity.username1,
        Connectivity.username2,
    ).first()

    return connectivity_history['invocations']
