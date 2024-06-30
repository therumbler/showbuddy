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
        """start a transcription job with AssemblyAI"""
        endpoint = "transcript"
        data = {"audio_url": audio_url, "speaker_labels": True}
        return await self._fetch(endpoint, data)

    async def fetch_transcript(self, transcript_id):
        """fetch a transcript by ID"""
        endpoint = f"transcript/{transcript_id}"
        return await self._fetch(endpoint, method="GET")

    async def delete_transcript(self, transcript_id):
        """delete a transcription by ID"""
        logger.warning("⚠️ deleting AssemblyAI transcript %s", transcript_id)
        endpoint = f"transcript/{transcript_id}"
        return await self._fetch(endpoint, data={}, method="DELETE")


async def main():
    """let's kick this off"""
    import os  # pylint: disable=import-outside-toplevel
    import json  # pylint: disable=import-outside-toplevel

    logging.basicConfig(level=logging.DEBUG)
    api_key = os.environ["ASSEMBLYAI_API_KEY"]
    assemblyai = AssemblyAI(api_key)

    # audio_url = "https://showbuddy.s3.us-west-002.backblazeb2.com/586cd004-2256-4975-89c1-ac287a44a741.webm"
    # resp = await assemblyai.start_transcript(audio_url)
    # transcript_id = resp["id"]
    # logger.info("transcript_id: %s", transcript_id)
    # await asyncio.sleep(10)
    transcript_id = "96f2ed0c-3a62-4c4b-89b0-646c83d15d4b"
    resp = await assemblyai.fetch_transcript(transcript_id)
    with open("transcript.json", "w", encoding="utf-8") as f:
        f.write(json.dumps(resp, indent=2))


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
