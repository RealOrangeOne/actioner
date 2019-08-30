import os

import uvicorn
from starlette.applications import Starlette
from starlette.authentication import SimpleUser, requires  # or a custom user model
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.responses import PlainTextResponse
from starlette.routing import Route, Router
from starlette_auth_toolkit.base.backends import BaseBasicAuth

from actioner.settings import BASIC_AUTH

from .healthcheck import healthcheck


class BasicAuth(BaseBasicAuth):
    async def verify(self, username: str, password: str):
        print(username, password)
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

    return app


def run_server(server):
    uvicorn.run(server, host="0.0.0.0", port=os.environ.get("PORT", 8000))
