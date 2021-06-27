import asyncio
from typing import List, Any

from fastapi import APIRouter, Response, status, Path, BackgroundTasks, Depends

from services import GithubFactory, TwitterFactory
from modules.connectivity.api.rest.v1 import schemas


router = APIRouter()


@router.get(
    '/realtime/{dev1}/{dev2}',
    tags=['➼ realtime endpoint'],
    status_code=200,
    description=(
        'For a given pair of developers checks whether they are connected or '
        'not. They are considered connected if they follow each other on '
        'Twitter, and they have at least one Github organization in common.'
    ),
    response_model=schemas.RealtimeItem,
)
async def realtime(
        dev1: schemas.OnlineAccount,
        dev2: schemas.OnlineAccount,
        background_tasks: BackgroundTasks,
        response: Response,
) -> Any:
    orgs_and_errs, friendship_and_errs = await asyncio.gather(
        GithubFactory().organizations_in_common(dev1, dev2),
        TwitterFactory().check_friendship(dev1, dev2),
    )
    common_orgs, errs1 = orgs_and_errs
    have_friendship, errs2 = friendship_and_errs

    data = {
        'connected': True, 'organizations': common_orgs,
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
)
async def register(
        dev1: schemas.OnlineAccount,
        dev2: schemas.OnlineAccount,
) -> Any:
    return [{
        'connected': 'True',
        'registered_at': '2019-09-27T12:34:00Z',
        'path-parameters': [dev1, dev2]
    }]
