import logging
import os
import time
from uuid import uuid4

from .uploader import Uploader
from lib.fireflies import Fireflies
from lib.spreadly import Spreadly

logger = logging.getLogger(__name__)


class ShowBuddy:
    def __init__(self):
        self._uploader = Uploader()
        self._fireflies = Fireflies(os.environ["FIREFLIES_API_KEY"])
        self._spreadly = Spreadly(os.environ["SPREADLY_API_KEY"])
        logger.info("ShowBuddy initialized")

    def _process_business_card(self, business_card_filepath):
        pass

    def _process_business_cards(self, business_card_filepaths):
        return list(map(self._process_business_card, business_card_filepaths))

    def _upload_audio(self, audio_fileobj, file_name):
        response = self._uploader.upload_file(audio_fileobj, file_name)

        return response

    def _process_audio(self, audio_fileobj, file_name):
        s3_response = self._upload_audio(audio_fileobj, file_name)
        logger.debug("s3_response %r", s3_response)
        return s3_response

    def _fetch_transcripts(self):
        transcripts = []
        while not transcripts:
            resp = self._fireflies.fetch_transcripts()
            transcripts = resp["data"]["transcripts"]

            if not transcripts:
                time.sleep(12)
        return resp

    def _fetch_transcript(self, transcript_id):
        logger.info('fetching transcript "%s"', transcript_id)
        sentences = []
        attempts = 0
        while not sentences:
            attempts += 1
            if attempts > 5:
                logger.error("no sentences found")
                transcript = None
                break
            transcript = self._fireflies.fetch_transcript(transcript_id)
            logger.debug("transcript %r", transcript)
            sentences = transcript["data"]["transcript"]["sentences"]
        logger.debug("sentences %r", sentences)
        return transcript

    def fetch_transcription_by_title(self, title):
        logger.info('fetching transcript by title "%s"', title)
        transcript = None
        while not transcript:
            transcripts = self._fireflies.fetch_transcripts()
            logger.info("transcripts %r", transcripts)
            # if not transcripts["data"]["transcripts"]:
            #     logger.error("no transcripts found")
            #     break
            for t in transcripts["data"]["transcripts"]:
                if t["title"] == title:
                    transcript = self._fetch_transcript(t["id"])
            if not transcript:
                time.sleep(12)
        return transcript

    def process(self, audio_fileobj, business_card_filepaths, audio_title):
        audio_url = self._process_audio(audio_fileobj, audio_title)
        logger.info("got audio_url %s", audio_url)

        # call fireflies api with s3 url
        # audio_title = str(uuid4())
        resp = self._fireflies.upload_audio(audio_url, audio_title=audio_title)

        # get transcript
        # transcripts = self._fetch_transcripts()
        transcript = self.fetch_transcription_by_title(audio_title)
        transcript_id = transcript["data"]["transcript"]["id"]
        transcript = self._fireflies.fetch_transcript(transcript_id)
        logger.info("transcript %r", transcript)
        return transcript

    def delete_file(self, audio_fileobj):
        return self._uploader.delete_file(audio_fileobj)

    def delete_transcript_by_title(self, title):
        transcript = self.fetch_transcription_by_title(title)
        return self._fireflies.delete_transcript(transcript["data"]["transcript"]["id"])


def test():
    """test things"""
    showbuddy = ShowBuddy()
    assert showbuddy is not None
    print("All tests pass")
