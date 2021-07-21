from fastapi import FastAPI

import modules.connectivity.api.rest.v1.view as connectivity_view_v1
from common.helper.custom_exc_handlers import exc_handlers
from common.helper.custom_renderer import CustomDataResponse
from common.log_setter import load_logging_configuration
from common.middlewares import middleware_list


load_logging_configuration()

app = FastAPI(
    title='JobAndTalent Coding Test',
    description='job position: "senior software developer"',
    version='0.0.1',
    default_response_class=CustomDataResponse,
    exception_handlers=exc_handlers,
    middleware=middleware_list,
)

app.include_router(router=connectivity_view_v1.router, prefix='/v1/connected')


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        'main:app',
        host='127.0.0.1',
        port=8000,
        log_level='debug',
        reload=True,
        debug=True,
    )
