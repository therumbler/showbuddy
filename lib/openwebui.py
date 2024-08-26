"""Module for interacting with OpenAI API"""

import logging
import httpx


logger = logging.getLogger(__name__)


class OpenWebUI:
    """Use the OpenWebUI APT to do LLM things"""

    def __init__(self, url, api_key):
        self._url=url
        self._api_key = api_key
        self.api_requests_count = 0

    async def _fetch(self, endpoint, data=None, method="POST"):
        url = f"{self._url}/{endpoint}"
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "content-type": "application/json",
        }
        logger.debug("Fetching url: %s headers: %r", url, headers)
        req = httpx.Request(method, url, headers=headers, json=data)
        async with httpx.AsyncClient() as client:
            resp = await client.send(req)
            self.api_requests_count += 1
            data = resp.json()
            logger.info("data: %r", data)
            resp.raise_for_status()
            return data

    async def ollama_prompt(self, prompt):
        """Fetch the response to a prompt from Ollama"""
        endpoint = "ollama/api/generate"
        data = {
            "model": "llama3.1:8b",
            "prompt": prompt,
            "temperature": 0.3,
            "stream": "false",
        }
        resp = await self._fetch(endpoint, data)
        logger.info("resp: %r", resp)
        return resp




