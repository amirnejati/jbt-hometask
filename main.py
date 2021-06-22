# import uvicorn
from fastapi import FastAPI

from config import Config
from connectivity.view import connectivity_router

app = FastAPI(
    title="LBS api",
    description="""location base services""",
    version="0.0.1",
    # docs_url="/docsss",#setting.DOC_URL,
    # servers=[{"url": f"http://{setting.HOST}:{setting.GENERAL_URL_PORT}"}, {"url": ""}]
)


app.include_router(router=connectivity_router, prefix='/connected')


# asgi_app = SentryAsgiMiddleware(app)
# if __name__ == "__main__":
#     uvicorn.run(app, port="8/080")
