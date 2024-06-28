"""Main module for ShowBuddy"""

import logging
import os
import time

from lib.fireflies import Fireflies
from lib.spreadly import Spreadly
from .uploader import Uploader


logger = logging.getLogger(__name__)


class ShowBuddy:
    """Class to pull it all together"""

    def __init__(self):
        self._uploader = Uploader()
        self._fireflies = Fireflies(os.environ["FIREFLIES_API_KEY"])
        self._spreadly = Spreadly(os.environ["SPREADLY_API_KEY"])
        logger.info("ShowBuddy initialized")

    def _process_business_card(self, business_card_fileobj):
        return self._spreadly.scan_card(business_card_fileobj)

    def _process_business_cards(self, business_card_fileobjs):
        # return []
        return list(map(self._process_business_card, business_card_fileobjs))

    def _process_audio(self, audio_fileobj, audio_title):
        logger.warning('skipping audio processing "%s"', audio_title)
        return None
        audio_url = self._uploader.upload_file(audio_fileobj, audio_title)
        logger.debug("audio_url %s", audio_url)

        self._fireflies.upload_audio(audio_url, audio_title=audio_title)
        transcript = self._fetch_transcription_by_title(audio_title)
        transcript_id = transcript["data"]["transcript"]["id"]
        transcript = self._fireflies.fetch_transcript(transcript_id)
        logger.info("transcript %r", transcript)
        return transcript

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

    def _fetch_transcription_by_title(self, title):
        logger.info('fetching transcript by title "%s"', title)
        transcript = None
        attempts = 0
        while not transcript:
            attempts += 1
            if attempts > 5:
                logger.error("no transcript found")
                break
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

    def process(self, audio_fileobj, business_card_fileobjs, audio_title):
        """Trigger the processing of an audio file and business cards"""

        business_card_resp = self._process_business_cards(business_card_fileobjs)

        logger.info("got business card resp %s", business_card_resp)
        # return
        transcript = self._process_audio(audio_fileobj, audio_title)
        logger.info("got transcript resp %r", transcript)

        return {"business_card_resp": business_card_resp, "transcript": transcript}

    def delete_file(self, audio_fileobj):
        """used by integration tests to clean up after themselves"""
        return self._uploader.delete_file(audio_fileobj)

    def delete_transcript_by_title(self, title):
        """used by integration tests to clean up after themselves"""
        transcript = self._fetch_transcription_by_title(title)
        return self._fireflies.delete_transcript(transcript["data"]["transcript"]["id"])
