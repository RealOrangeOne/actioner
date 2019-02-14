from aiohttp import web
from actioner.clients import github


async def healthcheck(request):
    return web.json_response({
        'github': github.get_user().login
    })
