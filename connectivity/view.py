import asyncio

from fastapi import APIRouter

from services.github import Github
from services.twitter import Twitter

connectivity_router = APIRouter()


@connectivity_router.get("/realtime/{dev1}/{dev2}", tags=["users"])
async def read_users(dev1, dev2):
    results = await asyncio.gather(
        Github.get_organizations(dev1),
        Github.get_organizations(dev2),
        Twitter.get_organizations(dev1),
        Twitter.get_organizations(dev2),
    )
    print(results)

    return [{"username": dev1}, {"username": dev2}]


@connectivity_router.get("/register/{dev1}/{dev2}", tags=["users"])
async def read_user_me(dev1, dev2):
    return {"username": f"{dev1}\t{dev2}"}
