"""Module for interacting with OpenAI API"""

import logging
import httpx


logger = logging.getLogger(__name__)


class OpenAI:
    """Use the OpenAI APT to do LLM things"""

    def __init__(self, organization, project, api_key):
        self._organization = organization
        self._project = project
        self._api_key = api_key
        self.api_requests_count = 0

    async def _fetch(self, endpoint, data=None, method="POST"):
        url = f"https://api.openai.com/v1/{endpoint}"
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "accept": "application/json",
            "content-type": "application/json",
            "OpenAI-Organization": self._organization,
            "OpenAI-Project": self._project,
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

    async def fetch_completions(self, content):
        """fetch a completion from OpenAI"""
        endpoint = "chat/completions"
        data = {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": content}],
            "temperature": 0.3,
        }
        resp = await self._fetch(endpoint, data)
        logger.info("resp: %r", resp)
        return resp
