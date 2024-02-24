from server.api_base import app

from router import router

app.include_router(router)