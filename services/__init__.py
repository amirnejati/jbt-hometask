from utility.github import Github
from utility.twitter import Twitter
from config import Config


class TwitterFactory(Twitter):

    def __init__(self):
        super(TwitterFactory, self).__init__(Config.TWITTER_ACCESS_TOKEN)


class GithubFactory(Github):

    def __init__(self):
        super(GithubFactory, self).__init__(Config.GITHUB_ACCESS_TOKEN)



if __name__ == '__main__':
    import asyncio
    # t = TwitterFactory()
    # x = asyncio.run(t.check_friendship('amirhnejatii', 'bitcodr'))
    # print(x)
    g = GithubFactory()
    x = asyncio.run(g.get_organizations(username='mitsuhiko'))
    print(x)
