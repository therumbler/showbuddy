import logging
import os
import time
from uuid import uuid4

from .uploader import Uploader
from lib.fireflies import Fireflies

logger = logging.getLogger(__name__)


class ShowBuddy:
    def __init__(self):
        self._uploader = Uploader()
        self._fireflies = Fireflies(os.environ["FIREFLIES_API_KEY"])
        logger.info(self._fireflies.fetch_user())

    def _process_business_card(self, business_card_filepath):
        pass

    def _process_business_cards(self, business_card_filepaths):
        return list(map(self._process_business_card, business_card_filepaths))

    def _upload_audio(self, audio_filepath):
        file_name = os.path.basename(audio_filepath)
        logger.info("Uploading %s ...", file_name)
        response = self._uploader.upload_file(audio_filepath)
        logger.info("uploader response: %r", response)
        return response

    def _process_audio(self, audio_filepath):
        s3_response = self._upload_audio(audio_filepath)
        logger.info("s3_response %r", s3_response)
        return s3_response

    def _fetch_transcripts(self):
        transcripts = []
        while not transcripts:
            resp = self._fireflies.fetch_transcripts()
            transcripts = resp["data"]["transcripts"]
            logger.info("transcripts %r", transcripts)
            time.sleep(5)
        return resp

    def _fetch_transcript(self, transcript_id):
        sentences = []
        while not sentences:
            transcript = self._fireflies.fetch_transcript(transcript_id)
            logger.info("transcript %r", transcript)
            sentences = transcript["data"]["transcript"]["sentences"]
        logger.info("sentences %r", sentences)
        return transcript

    def fetch_transcription_by_title(self, title):
        transcripts = self._fireflies.fetch_transcripts()
        for transcript in transcripts["data"]["transcripts"]:
            if transcript["title"] == title:
                return self._fetch_transcript(transcript["id"])

    def process(self, audio_filepath, business_card_filepaths, audio_title):
        audio_url = self._process_audio(audio_filepath)
        logger.info("got audo_url %s", audio_url)

        # call fireflies api with s3 url
        # audio_title = str(uuid4())
        resp = self._fireflies.upload_audio(audio_url, audio_title=audio_title)
        logger.info("fireflies response %r", resp)
        # get transcript
        transcripts = self._fetch_transcripts()
        transcript_id = transcripts["data"]["transcripts"][-1]["id"]
        transcript = self._fireflies.fetch_transcript(transcript_id)
        logger.info("transcript %r", transcript)
        return transcript

    def delete_file(self, audio_filepath):
        return self._uploader.delete_file(audio_filepath)

    def delete_transcript(self, transcript_id):
        return self._fireflies.delete_transcript(transcript_id)


def test():
    """test things"""
    showbuddy = ShowBuddy()
    assert showbuddy is not None
    print("All tests pass")
