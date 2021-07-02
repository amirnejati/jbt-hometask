from typing import Any

from fastapi.responses import UJSONResponse


class CustomDataResponse(UJSONResponse):

    def render(self, content: Any) -> bytes:
        return super().render({'data': content})


class CustomErrResponse(UJSONResponse):

    def render(self, content: Any) -> bytes:
        return super().render({'error': content})
