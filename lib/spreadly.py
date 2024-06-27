import logging
import os

from uuid import uuid4
import requests


# from requests_toolbelt.multipart.encoder import MultipartEncoder

logger = logging.getLogger(__name__)


class Spreadly:
    """Spreadly API
    https://spreadly.readme.io/reference/intro/getting-started
    """

    def __init__(self, api_key):
        self.api_requests_count = 0
        self._api_key = api_key

    def _fetch(self, endpoint, files):
        url = f"https://spreadly.app/api/v1/{endpoint}"

        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "accept": "application/json",
        }
        logger.debug("Fetching url: %s", url)
        resp = requests.post(url, files=files, headers=headers)
        self.api_requests_count += 1
        resp.raise_for_status()
        return resp.json()

    def scan_card(self, card_filepath):
        endpoint = "business-card-scans"
        with open(card_filepath, "rb") as f:
            filename = f"{str(uuid4())}.jpg"
            files = {
                "front": (
                    filename,
                    f,
                ),
            }

            return self._fetch(endpoint, files)

    def delete_scan(self, scan_id):
        logger.warning("delete_scan not yet implemented")


def main():
    """let's kick this off"""
    import os

    logging.basicConfig(level=logging.DEBUG)
    api_key = os.environ["SPREADLY_API_KEY"]
    spreadly = Spreadly(api_key)
    card_filepath = "../tests/integration/tsepo_montsi.zo.ca_business_card.HEIC"
    resp = spreadly.scan_card(card_filepath=card_filepath)
    logger.info("resp: %r", resp)


if __name__ == "__main__":
    main()
