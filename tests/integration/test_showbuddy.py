import logging
import unittest
from uuid import uuid4

from showbuddy import ShowBuddy


logger = logging.getLogger(__name__)

AUDIO_FILEPATH = "./tests/integration/files/test_audio_1a.m4a"


class TestShowBuddy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logging.basicConfig(level=logging.INFO)
        cls._showbuddy = ShowBuddy()

    def _check_for_text_in_sentences(self, text, sentences):
        return any([text in s["text"] for s in sentences])

    def test_showbuddy(self):
        TestShowBuddy._transcript_title = str(uuid4())
        resp = self._showbuddy.process(
            AUDIO_FILEPATH, [], TestShowBuddy._transcript_title
        )
        logger.info("process response: %r", resp)

        assert "errors" not in resp
        text = "Let's hope this file is larger than 500 kb"
        sentences = resp["data"]["transcript"]["sentences"]
        assert self._check_for_text_in_sentences(text, sentences)

    @classmethod
    def tearDownClass(cls):
        logger.info("Tear down! deleting file and transcript")
        cls._showbuddy.delete_file(AUDIO_FILEPATH)
        cls._showbuddy.delete_transcript_by_title(cls._transcript_title)
        logger.info(
            "Fireflies api requests count: %d",
            cls._showbuddy._fireflies.api_requests_count,
        )
