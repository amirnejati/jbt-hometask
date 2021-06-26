import re
from typing import List, Optional

from pydantic import BaseModel, validator


class DeveloperAccount(BaseModel):
    username: str

    @validator('username')
    def username_validity(cls, v: str) -> str:
        """
        for more info about the rules & patterns used refer to:
            - https://help.twitter.com/en/managing-your-account/twitter-username-rules
            - https://github.com/join
        """

        twitter_username_regex = r'^[a-zA-Z0-9_]{1,15}$'
        github_username_regex = \
            r'^[a-zA-Z\d](?:[a-zA-Z\d]|-(?=[a-zA-Z\d])){0,38}$'

        if re.search(twitter_username_regex, v) and \
                re.search(github_username_regex, v):
            return v

        raise ValueError(
            f'username "{v}" sounds to be an invalid account in either '
            'Twitter or Github, or the both.\n'
            f'Twitter regex pattern: {twitter_username_regex}\n'
            f'Github regex pattern: {github_username_regex}'
        )


class RealtimeItem(BaseModel):
    connected: bool
    organisations: Optional[List[DeveloperAccount]] = None


class RegisterItem(RealtimeItem):
    registered_at: str
