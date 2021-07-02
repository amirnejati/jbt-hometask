from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import modules.connectivity.api.rest.v1.view as connectivity_view_v1
from helper.custom_renderer import CustomDataResponse
from helper.custom_exc_handlers import exc_handlers


app = FastAPI(
    title="JobAndTalent Coding Test",
    description="""job position: \"senior software developer \"""",
    version="0.0.1",
    default_response_class=CustomDataResponse,
    exception_handlers=exc_handlers,
)

app.include_router(router=connectivity_view_v1.router, prefix='/v1/connected')
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])


if __name__ == '__main__':
    import uvicorn
    # asgi_app = SentryAsgiMiddleware(app)
    uvicorn.run(
        "main:app", host="127.0.0.1", port=8000,
        log_level="debug", reload=True, debug=True
    )
