"""Async integration tests for the Open WebUI API"""

import logging
import os
from unittest import IsolatedAsyncioTestCase

from lib.openwebui import OpenWebUI


class TestOpenWebUI(IsolatedAsyncioTestCase):
    """Async integration tests for the OpenWebUI API"""

    async def asyncSetUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self._openwebui = OpenWebUI(
            url=os.environ["OPENWEBUI_URL"],
            api_key=os.environ["OPENWEBUI_API_KEY"],
        )

    async def test_openwebui(self):
        """test a simple completion"""
        content = """In the following text, return no text except for Speaker A's name:
        
Speaker A: Hello, my name is Frank
Speaker B: Hi Frank, I'm Bob
Speaker A: How are you today?
Speaker B: I'm good, how are you?"""
        expected_response = "Frank"
        resp = await self._openwebui.ollama_prompt(content)
        assert resp["response"] == expected_response
