from aiohttp import web
from aiohttp_basicauth import BasicAuthMiddleware

from actioner.settings import BASIC_AUTH

from .healthcheck import healthcheck


def get_server():
    auth = BasicAuthMiddleware(username=BASIC_AUTH[0], password=BASIC_AUTH[1], force=False)
    app = web.Application()
    app.router.add_get("/healthcheck", auth.required(healthcheck))
    return app
