from aiohttp import web


def get_server():
    app = web.Application()
    return app
