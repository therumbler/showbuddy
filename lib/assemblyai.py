"""Module for interacting with AssemblyAI API"""

import logging

import httpx

logger = logging.getLogger(__name__)


class AssemblyAI:
    """AssemblyAI API
    https://spreadly.readme.io/reference/intro/getting-started
    """

    def __init__(self, api_key):
        self.api_requests_count = 0
        self._api_key = api_key

    async def _fetch(self, endpoint, data=None, method="POST"):
        url = f"https://api.assemblyai.com/v2/{endpoint}"

        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "accept": "application/json",
        }
        logger.debug("Fetching url: %s", url)
        req = httpx.Request(method, url, headers=headers, json=data)
        async with httpx.AsyncClient() as client:
            resp = await client.send(req)
            self.api_requests_count += 1
            data = resp.json()
            logger.info("data: %r", data)
            resp.raise_for_status()
            return data

    async def start_transcript(self, audio_url):
        """scan a business card image file and return the data"""
        endpoint = "transcript"

        data = {"audio_url": audio_url}

        return await self._fetch(endpoint, data)

    async def fetch_transcript(self, transcript_id):
        """fetch a transcript by ID"""
        endpoint = f"transcript/{transcript_id}"
        return await self._fetch(endpoint, method="GET")

    async def delete_transcript(self, transcript_id):
        """delete a scan by ID"""
        logger.warning("delete_scan not yet implemented")
        endpoint = f"transcript/{transcript_id}"
        return await self._fetch(endpoint, data={}, method="DELETE")


async def main():
    """let's kick this off"""
    import os  # pylint: disable=import-outside-toplevel

    logging.basicConfig(level=logging.DEBUG)
    api_key = os.environ["ASSEMBLYAI_API_KEY"]
    assemblyai = AssemblyAI(api_key)
    # card_filepath = "./tests/integration/files/tsepo_montsi.zo.ca_business_card.jpg"
    audio_filepath = "./tests/integration/files/test_audio_1a.m4a"
    resp = await assemblyai.fetch_transcript(audio_filepath)
    logger.info("resp: %r", resp)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
