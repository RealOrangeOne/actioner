from aiohttp.test_utils import AioHTTPTestCase

from actioner.web import get_server


class BaseWebTestCase(AioHTTPTestCase):
    async def get_application(self):
        return get_server()
