from aiohttp import web
from .healthcheck import healthcheck

def get_server():
    app = web.Application()
    app.router.add_get("/healthcheck", healthcheck)
    return app
