import re
from typing import AsyncGenerator, Dict, List, Set, Tuple
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
        self.response_headers: Dict[str, str] = {}

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

    async def _get_organisations(self, username: str) \
            -> AsyncGenerator[Tuple[Set[str], bool], None]:
        """
        A private method which calls Github API to get organisations related
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

        if response.status_code == 404:
            yield set(), True
            return
        if response.status_code >= 400:
            raise Exception(response.text)

        yield {item['login'] for item in response.json()}, False

        if self._continue_pagination():
            async for result in self._get_organisations(username=username):
                yield result

    async def get_organisations(self, username: str) \
            -> Tuple[Set[str], List[str]]:
        """
        A wrapper method for calling :py:meth:`Github._get_organisations`.
        For :param & :return values, please refer to the origin method.
        """

        data: Set[str] = set()
        func = self._get_organisations(username=username)

        async for result, err in func:
            if err:
                return result, [f'"{username}" is not a valid user in github']
            data = data.union(result)

        return data, []
