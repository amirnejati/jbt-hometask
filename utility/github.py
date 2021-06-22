import re
from typing import AsyncGenerator, Set, Tuple
from urllib.parse import urlencode

import httpx


class Github:
    base_url = 'https://api.github.com'
    request_headers = {
        'Accept': 'application/vnd.github.v3+json',
    }

    def __init__(self, token: str = None):
        if token:
            self.request_headers.update({'Authorization': f'token {token}'})
        self.pagination_params = {'page': 1, 'per_page': 100}
        self.response_headers = {}

    def _continue_pagination(self) -> bool:
        """
        This method enables paginating data returned from Github.
        Based on Github API docs, it uses 'Link' header to determine
        paginate status.

        for more details:
        https://docs.github.com/en/rest/guides/traversing-with-pagination

        :return:
            - a boolean value which specified continue or not
        """

        if 'Link' in self.response_headers \
                and self.response_headers['Link'].find('"next"') > -1:
            page = int(p[0]) if (
                p := re.findall(
                    r'\W+page=(\d+)[^<]+"next"',
                    self.response_headers['Link'],
                )
            ) else 1
            per_page = int(p[0]) if (
                p := re.findall(
                    r'\W+per_page=(\d+)[^<]+"next"',
                    self.response_headers['Link'],
                )
            ) else 100
            self.pagination_params = {'page': page, 'per_page': per_page}
            return True
        return False

    async def _get_organizations(self, username: str) \
            -> AsyncGenerator[Tuple[Set[str], bool], None]:
        """
        A private method which calls Github API to get organizations related
        to an account.

        :param
            - username: account handler to be searched for
        :return: a tuple of python-set of str and bool which
            - set of str including orgs related to the username
            - the boolean value is True when there is any error
        """

        url = f'{self.base_url}/users/{username}/orgs'
        url += f'?{urlencode(self.pagination_params)}'

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.request_headers)
            self.response_headers = response.headers

        if response.status_code >= 400:
            if response.status_code == 404:
                yield set(), True
            else:
                raise Exception(response.text)

        if response.status_code == 200:
            yield {item['login'] for item in response.json()}, False

            if self._continue_pagination():
                async for result in self._get_organizations(username=username):
                    yield result

    async def get_organizations(self, username: str) -> Tuple[Set[str], bool]:
        """
        A wrapper method for calling :py:meth:`Github._get_organizations`.
        For :param & :return values, please refer to the origin method.
        """

        func = self._get_organizations(username=username)
        data, has_errors = set(), False

        async for result, err in func:
            data = data.union(result)
            has_errors |= err

        return data, has_errors
