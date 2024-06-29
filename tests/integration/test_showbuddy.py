import asyncio
import logging
from unittest import TestCase, skip
from uuid import uuid4

from showbuddy import ShowBuddy


logger = logging.getLogger(__name__)

AUDIO_FILEPATH = "./tests/integration/files/test_audio_1a.m4a"
BUSINESS_CARD_FILEPATH = (
    "./tests/integration/files/tsepo_montsi.zo.ca_business_card.jpg"
)


class TestShowBuddy(TestCase):
    @classmethod
    def setUpClass(cls):
        logging.basicConfig(level=logging.INFO)
        cls._showbuddy = ShowBuddy()
        cls._transcript_title = str(uuid4())
        with open(BUSINESS_CARD_FILEPATH, "rb") as business_card_file:
            with open(AUDIO_FILEPATH, "rb") as audio_file:
                cls.resp = asyncio.run(
                    cls._showbuddy.process(
                        audio_file,
                        [business_card_file],
                        TestShowBuddy._transcript_title,
                    )
                )
                logger.info("process response: %r", cls.resp)

    def _check_for_text_in_sentences(self, text_to_check, text_resp):
        return text_to_check in text_resp

    def _test_transcript_response(self, resp):
        assert resp is not None
        assert "error" not in resp
        text_to_check = "Let's hope this file is larger than 500 kb"
        text_resp = resp["text"]
        assert self._check_for_text_in_sentences(text_to_check, text_resp)

    def _test_business_card_response(self, resp):
        card0 = resp[0]
        assert "errors" not in card0
        assert card0["given_name"] == "Tsepo"
        assert card0["family_name"] == "Montsi"
        assert "http://www.montsi.co.za" in card0["websites"]

    # @skip("Skipping test_showbuddy")
    def test_showbuddy(self):

        self._test_business_card_response(self.resp["business_card_resp"])
        self._test_transcript_response(self.resp["transcript"])

    @classmethod
    def tearDownClass(cls):
        logger.info("Tear down! deleting file and transcript")
        cls._showbuddy.delete_file(AUDIO_FILEPATH)
        asyncio.run(cls._showbuddy.delete_transcript(cls.resp["transcript"]["id"]))
        logger.info(
            "AssemblyAI API requests count: %d",
            cls._showbuddy._assemblyai.api_requests_count,
        )
