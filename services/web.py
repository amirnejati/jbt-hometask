import asyncio
from functools import reduce
from typing import Dict, List, Set, Tuple

from config import Config
from utility.github import Github
from utility.twitter import Twitter


class TwitterFactory(Twitter):
    def __init__(self) -> None:
        super().__init__(Config.TWITTER_ACCESS_TOKEN)


class GithubFactory(Github):
    def __init__(self) -> None:
        super().__init__(Config.GITHUB_ACCESS_TOKEN)

    async def organisations_in_common(self, *users: str) -> Tuple[Set[str], List[str]]:

        results = await asyncio.gather(
            *(self.get_organisations(u) for u in users),
        )

        common_orgs, errors = reduce(
            lambda a, b: (a[0] & b[0], a[1] + b[1]),
            results,
        )

        return common_orgs, errors


async def get_connectivity_relation(
    user1: str,
    user2: str,
) -> Tuple[Dict[str, object], List[str]]:
    orgs_and_errs, friendship_and_errs = await asyncio.gather(
        GithubFactory().organisations_in_common(user1, user2),
        TwitterFactory().check_friendship(user1, user2),
    )
    common_orgs, errs1 = orgs_and_errs
    have_friendship, errs2 = friendship_and_errs

    data = (
        {
            'connected': True,
            'organisations': common_orgs,
        }
        if common_orgs and have_friendship
        else {'connected': False}
    )
    errors = errs1 + errs2

    return data, errors
