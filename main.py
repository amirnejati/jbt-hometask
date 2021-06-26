# import uvicorn
from fastapi import FastAPI

import modules.connectivity.api.rest.v1.view as connectivity_view_v1

app = FastAPI(
    title="JobAndTalent Coding Test",
    description="""job position: \"senior software developer \"""",
    version="0.0.1",
    # docs_url="/docsss",#setting.DOC_URL,
)


app.include_router(router=connectivity_view_v1.router, prefix='/v1/connected')


# asgi_app = SentryAsgiMiddleware(app)
# if __name__ == "__main__":
#     uvicorn.run(app, port="8/080")
