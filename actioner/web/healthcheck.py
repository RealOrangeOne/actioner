from aiohttp import web

from actioner.clients import github, todoist


async def healthcheck(request):
    todoist.user.sync()
    return web.json_response({
        'github': github.get_user().login,
        'todoist': todoist.user.get_id()
    })
