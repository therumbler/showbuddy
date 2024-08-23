from unittest import IsolatedAsyncioTestCase
from uuid import uuid4

from lib.openai import OpenAI


class TestOpenAI(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self._openai = OpenAI(
            organization="organization",
            project="project",
            api_key="api_key",
        )

    async def test_openai(self):
        content = "Hello, how are you?"
        expected_response = "I'm good, how are you?"
        resp = await self._openai.fetch_completions(content)
        assert resp == expected_response
