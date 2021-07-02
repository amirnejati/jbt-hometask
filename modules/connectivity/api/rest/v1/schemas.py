import re
from typing import List, Optional
import ujson

from pydantic import BaseModel


class OnlineAccount(str):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_twitter_username
        yield cls.validate_github_username

    @classmethod
    def validate_twitter_username(cls, v: str) -> str:
        """
        for more info about the rules & patterns used refer to:
        https://help.twitter.com/en/managing-your-account/twitter-username-rules
        """

        if not isinstance(v, str):
            raise TypeError('string required')
        twitter_username_regex = r'^[a-zA-Z0-9_]{1,15}$'
        if re.search(twitter_username_regex, v):
            return cls(v)
        raise ValueError(
            f'username "{v}" sounds to be an invalid account in Twitter. '
            f'Twitter regex pattern: {twitter_username_regex}'
        )

    @classmethod
    def validate_github_username(cls, v: str) -> str:
        """
        for more info about the rules & patterns used refer to:
        https://github.com/join
        """

        if not isinstance(v, str):
            raise TypeError('string required')
        github_username_regex = \
            r'^[a-zA-Z\d](?:[a-zA-Z\d]|-(?=[a-zA-Z\d])){0,38}$'
        if re.search(github_username_regex, v):
            return cls(v)
        raise ValueError(
            f'username "{v}" sounds to be an invalid account in Github. '
            f'Github regex pattern: {github_username_regex}'
        )


class RealtimeItem(BaseModel):
    connected: bool
    organisations: Optional[List[OnlineAccount]] = None

    class Config:
        json_loads = ujson.loads
        orm_mode = True


class RegisterItem(RealtimeItem):
    registered_at: str
