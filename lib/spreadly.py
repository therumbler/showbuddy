"""Module for interacting with Spreadly API"""

import logging

from uuid import uuid4
import requests
import httpx

logger = logging.getLogger(__name__)


class Spreadly:
    """Spreadly API
    https://spreadly.readme.io/reference/intro/getting-started
    """

    def __init__(self, api_key):
        self.api_requests_count = 0
        self._api_key = api_key

    async def _fetch(self, endpoint, files):
        url = f"https://spreadly.app/api/v1/{endpoint}"

        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "accept": "application/json",
        }
        logger.debug("Fetching url: %s", url)
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, files=files, headers=headers, timeout=30)
            self.api_requests_count += 1
            resp.raise_for_status()
            return resp.json()

    async def scan_card(self, card_file):
        """scan a business card image file and return the data"""
        endpoint = "business-card-scans"

        filename = f"{str(uuid4())}.jpg"
        files = {
            "front": (
                filename,
                card_file,
            ),
        }

        return await self._fetch(endpoint, files)

    def delete_scan(self, _):
        """delete a scan by ID"""
        logger.warning("delete_scan not yet implemented")


async def main():
    """let's kick this off"""
    import os  # pylint: disable=import-outside-toplevel

    logging.basicConfig(level=logging.DEBUG)
    api_key = os.environ["SPREADLY_API_KEY"]
    spreadly = Spreadly(api_key)
    card_filepath = "./tests/integration/files/tsepo_montsi.zo.ca_business_card.jpg"
    with open(card_filepath, "rb") as f:
        resp = await spreadly.scan_card(f)
    logger.info("resp: %r", resp)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
