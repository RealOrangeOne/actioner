from starlette.responses import JSONResponse

from actioner.clients import get_todoist_client, github


async def healthcheck(request):
    todoist = get_todoist_client()
    todoist.user.sync()
    return JSONResponse(
        {"github": github.get_user().login, "todoist": todoist.user.get_id()}
    )
