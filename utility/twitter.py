from typing import AsyncGenerator, Dict, List, Optional, Tuple

import httpx


class Twitter:
    base_url = 'https://api.twitter.com'
    request_headers: Dict[str, str] = {}

    def __init__(self, token: str):
        self.request_headers.update({'Authorization': f'Bearer {token}'})

    async def _check_users(self, *users: str) \
            -> AsyncGenerator[Tuple[str, bool], None]:
        """
        Validates account handlers on Twitter.

        :return: a tuple of boolean and str which
            - the boolean value is True when there is any error
            - the str shows the corresponding username
        """

        url = (
            f'{self.base_url}/2/users/by'
            f'?usernames={",".join(users)}'
        )

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.request_headers)

        if response.status_code >= 400:
            raise Exception(response.text)

        for i in response.json().get('data', []):
            yield i['username'], False
        for i in response.json().get('errors', []):
            yield i['value'], True

    async def check_friendship(
            self, source_user: str, target_user: str,
    ) -> Tuple[Optional[bool], List[str]]:
        """
        Shows friendship between two accounts. Friendship means both users
        follow each other.

        :return: a tuple of a boolean and list of str which
            - the boolean value shows whether the given accounts have
              friendship relation or not. in case of errors this value is NULL!
            - the list returns errors if there are any, in str format
        """

        url = (
            f'{self.base_url}/1.1/friendships/show.json'
            f'?source_screen_name={source_user}'
            f'&target_screen_name={target_user}'
        )
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.request_headers)

        if response.status_code == 404:
            errors = []
            async for username, has_error in self._check_users(
                    source_user,
                    target_user,
            ):
                errors.append(f'"{username}" is not a valid user in twitter') \
                    if has_error else None
            if errors:
                return None, errors

        if response.status_code >= 400:
            raise Exception(response.text)

        relationship = response.json()['relationship']['source']

        if relationship['following'] and relationship['followed_by']:
            return True, []
        else:
            return False, []
