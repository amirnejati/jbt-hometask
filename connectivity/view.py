import asyncio

from fastapi import APIRouter

from services import GithubFactory, TwitterFactory


connectivity_router = APIRouter()


@connectivity_router.get("/realtime/{user1}/{user2}", tags=["users"])
async def read_users(user1, user2):
    results = await asyncio.gather(
        GithubFactory().get_organizations(user1),
        GithubFactory().get_organizations(user2),
        TwitterFactory().check_friendship(user1, user2),
    )
    print(results)

    return [{"username1": user1}, {"username2": user2}]


@connectivity_router.get("/register/{dev1}/{dev2}", tags=["users"])
async def read_user_me(dev1, dev2):
    return {"username": f"{dev1}\t{dev2}"}
