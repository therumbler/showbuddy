import json
import logging
import os
from urllib.error import HTTPError
from urllib.request import Request, urlopen

logger = logging.getLogger(__name__)


class Fireflies:
    """Fireflies class"""

    def __init__(self, api_key):
        self._api_key = api_key
        self._user = self.fetch_user()
        logger.info("_user: %r", self._user)

    def _fetch(self, data):
        url = "https://api.fireflies.ai/graphql"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._api_key}",
        }
        req = Request(url, data=json.dumps(data).encode(), headers=headers)
        logger.info("Fetching %s data: %s", url, json.dumps(data, indent=2))
        try:
            with urlopen(req) as response:
                return json.load(response)
        except HTTPError as ex:
            logger.error("HTTPError: %s", ex.code)
            return json.load(ex)

    def fetch_user(self):
        query = "{ users { name user_id } }"
        data = {"query": query}
        return self._fetch(data)

    def upload_audio(self, audio_url):
        logger.info('fireflies.upload_audio("%s")', audio_url)
        file_name = os.path.basename(audio_url)
        input = {
            # "webhook": "https://your_webhook_url",
            "url": audio_url,
            "title": file_name,
            "attendees": [
                {
                    "displayName": "attendee_name",
                    "email": "attendee_email",
                    "phoneNumber": "attendee_phone",
                },
            ],
        }
        data = {
            "query": """mutation($input: AudioUploadInput) {
                uploadAudio(input: $input) {
                success
                title
                message
                }
            }
            """,
            "variables": input,
        }

        return self._fetch(data)


def main():
    """let's kick this off"""
    import os

    api_key = os.environ["FIREFLIES_API_KEY"]
    fireflies = Fireflies(api_key)
    print(fireflies.fetch_user())


if __name__ == "__main__":
    main()
