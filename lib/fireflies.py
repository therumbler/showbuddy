"""Module for interacting with Fireflies API"""

import json
import logging
from urllib.error import HTTPError
from urllib.request import Request, urlopen

logger = logging.getLogger(__name__)


class Fireflies:
    """Fireflies class
    https://docs.fireflies.ai/examples/overview
    """

    def __init__(self, api_key):
        self.api_requests_count = 0
        self._api_key = api_key
        self._user = self.fetch_user()
        self._user_id = self._user["data"]["users"][0]["user_id"]

    def _fetch(self, data):
        url = "https://api.fireflies.ai/graphql"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._api_key}",
        }
        req = Request(url, data=json.dumps(data).encode(), headers=headers)
        logger.debug("Fetching %s data: %s", url, json.dumps(data, indent=2))
        try:
            self.api_requests_count += 1
            with urlopen(req) as response:
                return json.load(response)
        except HTTPError as ex:
            logger.error("HTTPError: %s", ex.code)
            return json.load(ex)

    def fetch_user(self):
        """Fetch the user from the Fireflies API for the current API key"""
        query = "{ users { name user_id } }"
        data = {"query": query}
        return self._fetch(data)

    def fetch_transcript(self, transcript_id):
        """fetch a Fireflies transcript by ID"""
        data = {
            "query": """query Transcript($transcriptId: String!) { 
                transcript(id: $transcriptId) 
                { 
                    title 
                    id 
                    sentences { 
                        text speaker_name start_time end_time 
                    }
                }
                }""",
            "variables": {"transcriptId": transcript_id},
        }
        return self._fetch(data)

    def fetch_transcripts(self):
        """Fetch all transcripts for the current user"""
        data = {
            "query": """query Transcripts($userId: String) { 
                transcripts(user_id: $userId) { title id } 
            }""",
            "variables": {"userId": self._user_id},
        }
        return self._fetch(data)

    def upload_audio(self, audio_url, audio_title):
        """Upload an audio file to Fireflies for transcription"""
        logger.info('fireflies.upload_audio("%s")', audio_url)

        variables = {
            "input": {
                # "webhook": "https://your_webhook_url",
                "url": audio_url,
                "title": audio_title,
                "attendees": [
                    {
                        "displayName": "Attendee One",
                        "email": "attendee1@example.com",
                        "phoneNumber": "attendee_phone",
                    },
                    {
                        "displayName": "Attendee Two",
                        "email": "attendee2@example.com",
                        "phoneNumber": "attendee_phone",
                    },
                ],
            }
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
            "variables": variables,
        }

        return self._fetch(data)

    def delete_transcript(self, transcript_id):
        """Delete a Fireflies transcript by ID"""
        data = {
            "query": """
        mutation($transcriptId: String!) {
          deleteTranscript(id: $transcriptId) {
            title
            date
            duration
            organizer_email
          }
        }
    """,
            "variables": {"transcriptId": transcript_id},
        }
        logger.warning("⚠️ deleting transcript_id %s", transcript_id)
        return self._fetch(data)


def main():
    """let's kick this off"""
    import os  # pylint: disable=import-outside-toplevel

    logging.basicConfig(level=logging.DEBUG)
    api_key = os.environ["FIREFLIES_API_KEY"]

    audio_url = "https://showbuddy.s3.us-west-002.backblazeb2.com/586cd004-2256-4975-89c1-ac287a44a741.webm"
    audio_filename = "586cd004-2256-4975-89c1-ac287a44a741a.webm"
    fireflies = Fireflies(api_key)
    # resp = fireflies.upload_audio(audio_url, audio_filename)
    # logger.info("fireflies.upload_audio resp: %r", resp)
    # transcripts = fireflies.fetch_transcripts()
    # logger.info("transcripts: %r", transcripts)
    # transcript_id = "gGemAwnYU3VEthM1"
    transcript_id = "v0KZ7JbCapvDL63A"
    transcript = fireflies.fetch_transcript(transcript_id)
    with open("fireflies_transcript2.json", "w") as f:
        json.dump(transcript, f, indent=2)
    # logger.info("count of transcripts: %d", len(transcripts["data"]["transcripts"]))


if __name__ == "__main__":
    main()
