"""Async integration tests for the OpenAI API"""

import os
from unittest import IsolatedAsyncioTestCase

from lib.openai import OpenAI


class TestOpenAI(IsolatedAsyncioTestCase):
    """Async integration tests for the OpenAI API"""

    async def asyncSetUp(self):
        self._openai = OpenAI(
            organization=os.environ["OPENAI_ORGANIZATION_ID"],
            project=os.environ["OPENAI_PROJECT_ID"],
            api_key=os.environ["OPENAI_API_KEY"],
        )

    async def test_openai(self):
        """test a simple completion"""
        content = "Hello, how are you?"
        expected_response = "I'm good, how are you?"
        resp = await self._openai.fetch_completions(content)
        assert resp == expected_response
