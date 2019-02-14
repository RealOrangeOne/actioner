from aiohttp import web


async def healthcheck(request):
    return web.json_response({})


def get_server():
    app = web.Application()
    app.router.add_get("/healthcheck", healthcheck)
    return app
