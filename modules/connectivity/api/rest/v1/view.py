from typing import Any, List

from fastapi import APIRouter, BackgroundTasks, Depends, Response, status
from sqlalchemy.orm import Session

from helper.custom_exc_handlers import OnlineAccountException
from modules import deps
from modules.connectivity import crud
from modules.connectivity.api.rest.v1 import schemas
from services.task import enqueue_task
from services.web import get_connectivity_relation


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
) -> Any:

    data, errors = await get_connectivity_relation(dev1, dev2)
    if errors:
        response.status_code = status.HTTP_404_NOT_FOUND
        raise OnlineAccountException(msg=errors)

    background_tasks.add_task(
        enqueue_task,
        crud.add_connectivity_invocation, None, dev1, dev2, **data
    )

    return data


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

    return crud.get_connectivity_invocations_history(db, dev1, dev2)
