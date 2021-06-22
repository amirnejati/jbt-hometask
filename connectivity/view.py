import asyncio

from fastapi import APIRouter, Response, status

from services import GithubFactory, TwitterFactory


connectivity_router = APIRouter()


@connectivity_router.get(
    "/realtime/{user1}/{user2}",
    tags=["users"],
    status_code=200
)
async def read_users(user1: str, user2: str, response: Response):
    orgs_and_errs, friendship_and_errs = await asyncio.gather(
        GithubFactory().organizations_in_common(user1, user2),
        TwitterFactory().check_friendship(user1, user2),
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


@connectivity_router.get("/register/{dev1}/{dev2}", tags=["users"])
async def read_user_me(dev1, dev2):
    return {"username": f"{dev1}\t{dev2}"}
