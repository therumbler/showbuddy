"""module to hit spreadly.app"""

import asyncio
import logging
import os
from datetime import datetime


import httpx

logger = logging.getLogger(__name__)


class SpreadlyService:
    """service to hit https://spreadly.app/api"""

    def __init__(self, api_key: str):
        self.api_key = api_key

    async def upload_card(self, session_id: str, image_data: bytes):
        """Upload a business card image"""

        card_data = await self._process_card(session_id, image_data)
        return card_data

    async def _process_card(self, session_id: str, image_data: bytes):
        """Process business card using Spreadly.io"""
        logger.info("Processing card for session %s...", session_id)

        try:
            # Make API request to Spreadly.io
            # Set headers with Bearer token and Content-Type
            headers = {
                "Authorization": f"Bearer {self.api_key}",
            }
            logger.info("uploading a file of length %d", len(image_data))
            files = {
                "front": ("image.png", image_data),
            }

            # Make the POST request with requests
            async with httpx.AsyncClient() as client:
                logger.info("Uploading card image to Spreadly.io")
                response = await client.post(
                    "https://spreadly.app/api/v1/business-card-scans",
                    headers=headers,
                    files=files,
                    timeout=30.0,
                )

            if response.status_code != 200:
                logger.info("Card processing failed: %d", response.status_code)
                return

            try:
                card_data = response.json()
            except ValueError:
                logger.error("Card processing failed: Invalid JSON response")
                return

            card_data["response_type"] = "card_data"
            card_data["session_id"] = session_id

            logger.info("Card processing completed for session %s", session_id)
            logger.info("Retrieved card data: %r", card_data)
            return card_data

        except Exception as e:
            logger.exception("Error processing card: %s", e)


async def main():
    """scan two cards asyncronously"""
    logging.basicConfig(level=logging.DEBUG)
    api_key = os.environ["SPREADLY_API_KEY"]
    session_id = "your_session_id_here"
    image_path0 = "../tests/integration/files/business_card_0.png"
    image_path1 = "../tests/integration/files/business_card_1.png"

    spreadly_service = SpreadlyService(api_key=api_key)

    with open(image_path0, "rb") as image1:
        with open(image_path1, "rb") as image2:

            results = await asyncio.gather(
                spreadly_service.upload_card(session_id, image1.read()),
                # spreadly_service.upload_card(session_id, image2.read()),
            )

    # print(results)


if __name__ == "__main__":

    asyncio.run(main())
