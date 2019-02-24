from aiohttp import web

from actioner.clients import get_todoist_client, github


async def healthcheck(request):
    todoist = get_todoist_client()
    todoist.user.sync()
    return web.json_response(
        {"github": github.get_user().login, "todoist": todoist.user.get_id()}
    )
