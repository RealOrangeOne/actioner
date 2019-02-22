from aiohttp import BasicAuth
from aiohttp.test_utils import unittest_run_loop

from actioner.settings import BASIC_AUTH
from tests.test_web import BaseWebTestCase


class HealthcheckTestCase(BaseWebTestCase):
    @unittest_run_loop
    async def test_heartbeat_requires_auth(self):
        response = await self.client.get("/healthcheck")
        self.assertEqual(response.status, 401)
        response = await self.client.get(
            "/healthcheck", headers={"Authorization": BasicAuth(*BASIC_AUTH).encode()}
        )
        self.assertEqual(response.status, 200)

    @unittest_run_loop
    async def test_heartbeat_response(self):
        response = await self.client.get(
            "/healthcheck", headers={"Authorization": BasicAuth(*BASIC_AUTH).encode()}
        )
        self.assertEqual(response.status, 200)
        self.assertEqual(
            await response.json(), {"github": "RealOrangeOne", "todoist": 7471233}
        )
