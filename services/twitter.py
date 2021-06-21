from typing import AsyncGenerator, List, Tuple

import httpx


class Twitter:
    base_url = 'https://api.twitter.com'
    headers = {}

    def __init__(self, token: str):
        self.headers.update({
            'Authorization': f'Bearer {token}',
        })

    async def _check_users(self, *users: str) \
            -> AsyncGenerator[Tuple[bool, str], None]:
        """
        validates account handlers on Twitter

        :return: a tuple of boolean and str which
            - the boolean value is True when there is any error
            - the str shows the corresponding username
        """

        url = (
            f'{self.base_url}/2/users/by'
            f'?usernames={",".join(users)}'
        )

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)

        if response.status_code != 200:
            raise ValueError

        for i in response.json().get('data', []):
            yield False, i['username']
        for i in response.json().get('errors', []):
            yield True, i['value']

    async def check_friendship(
            self, source_user: str, target_user: str,
    ) -> Tuple[bool, List[str]]:
        """
        shows friendship between two accounts.
        friendship means both users follow each other

        :return: a tuple of a boolean and list of str which
            - the boolean value shows whether the given accounts have
              friendship relation or not. in case of errors this value is
              always False!
            - the list returns errors if there are any, in str format
        """

        errors = []
        async for has_error, username in self._check_users(
                source_user,
                target_user,
        ):
            errors.append(f'{username} is not a valid user in twitter') \
                if has_error else None
        if errors:
            return False, errors

        url = (
            f'{self.base_url}/1.1/friendships/show.json'
            f'?source_screen_name={source_user}'
            f'&target_screen_name={target_user}'
        )
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
        relationship = response.json()['relationship']['source']
        return (True, []) \
            if relationship['following'] and relationship['followed_by'] \
            else (False, [])


# import asyncio
# t = Twitter('AAAAAAAAAAAAAAAAAAAAAM1dQwEAAAAAGu%2FQtXL0dKjgcGWqkls3lN1nA0A%3DyFC1vU8PwHFM6YegygqtJvrJgODMg6LpKYf59ZG3Fb5auT4sD9')
# x = asyncio.run(t.check_friendship('amirhnejatii', 'bitcodr'))
# print(x)
