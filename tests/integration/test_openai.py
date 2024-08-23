"""Async integration tests for the OpenAI API"""

import logging
import os
from unittest import IsolatedAsyncioTestCase

from lib.openai import OpenAI


class TestOpenAI(IsolatedAsyncioTestCase):
    """Async integration tests for the OpenAI API"""

    async def asyncSetUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self._openai = OpenAI(
            organization=os.environ["OPENAI_ORGANIZATION_ID"],
            project=os.environ["OPENAI_PROJECT_ID"],
            api_key=os.environ["OPENAI_API_KEY"],
        )

    async def test_openai(self):
        """test a simple completion"""
        content = """In the following text, return no text except for Speaker A's name:
        
Speaker A: Hello, my name is Frank
Speaker B: Hi Frank, I'm Bob
Speaker A: How are you today?
Speaker B: I'm good, how are you?"""
        expected_response = "Frank"
        resp = await self._openai.fetch_completions(content)
        assert resp["choices"][0]["message"]["content"] == expected_response
