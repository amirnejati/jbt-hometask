from typing import Tuple, List
import asyncio
from functools import reduce

from utility.github import Github
from utility.twitter import Twitter
from config import Config


class TwitterFactory(Twitter):

    def __init__(self):
        super(TwitterFactory, self).__init__(Config.TWITTER_ACCESS_TOKEN)


class GithubFactory(Github):

    def __init__(self):
        super(GithubFactory, self).__init__(Config.GITHUB_ACCESS_TOKEN)

    async def organizations_in_common(self, *users: str) \
            -> Tuple[List[str], List[str]]:

        results = await asyncio.gather(
            *(self.get_organizations(u) for u in users),
        )

        common_orgs, errors = reduce(
            lambda a, b: (a[0] & b[0], a[1] + b[1]),
            results,
        )

        return common_orgs, errors


if __name__ == '__main__':
    t = TwitterFactory()
    # x = asyncio.run(t.check_friendship('amirhnejatii', 'bitcodr'))
    # print(x)

    g = GithubFactory()
    # x = asyncio.run(g.get_organizations(username='mitsuhiko'))
    # x, y = asyncio.run(g.organizations_in_common('mitsuhiko', 'davidism'))
    # print(x, y)
