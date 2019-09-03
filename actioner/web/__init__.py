import os

import uvicorn
from sentry_asgi import SentryMiddleware
from starlette.applications import Starlette
from starlette.authentication import SimpleUser, requires  # or a custom user model
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.routing import Route
from starlette_auth_toolkit.base.backends import BaseBasicAuth

from actioner.settings import BASIC_AUTH

from .healthcheck import healthcheck


class BasicAuth(BaseBasicAuth):
    async def verify(self, username: str, password: str):
        if [username, password] != BASIC_AUTH:
            return None
        return SimpleUser(username)


def get_server():
    requires_authentication = requires("authenticated")
    app = Starlette(
        routes=[
            Route(
                "/healthcheck/", requires_authentication(healthcheck), methods=["GET"]
            )
        ]
    )
    app.add_middleware(AuthenticationMiddleware, backend=BasicAuth())
    app.add_middleware(SentryMiddleware)

    return app


def run_server(server):
    uvicorn.run(server, host="0.0.0.0", port=os.environ.get("PORT", 8000))
