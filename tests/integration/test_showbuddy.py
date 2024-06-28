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

    def _check_for_text_in_sentences(self, text, sentences):
        return any([text in s["text"] for s in sentences])

    def _test_transcript_response(self, resp):
        assert resp is not None
        assert "errors" not in resp
        text = "Let's hope this file is larger than 500 kb"
        sentences = resp["data"]["transcript"]["sentences"]
        assert self._check_for_text_in_sentences(text, sentences)

    def _test_business_card_response(self, resp):
        card0 = resp[0]
        assert "errors" not in card0
        assert card0["given_name"] == "Tsepo"
        assert card0["family_name"] == "Montsi"
        assert "http://www.montsi.co.za" in card0["websites"]

    # @skip("Skipping test_showbuddy")
    def test_showbuddy(self):
        resp = None
        with open(BUSINESS_CARD_FILEPATH, "rb") as business_card_file:
            with open(AUDIO_FILEPATH, "rb") as audio_file:
                resp = self._showbuddy.process(
                    audio_file, [business_card_file], TestShowBuddy._transcript_title
                )
                logger.info("process response: %r", resp)

        self._test_business_card_response(resp["business_card_resp"])
        # self._test_transcript_response(resp["transcript"])

    @classmethod
    def tearDownClass(cls):
        logger.info("Tear down! deleting file and transcript")
        cls._showbuddy.delete_file(AUDIO_FILEPATH)
        # cls._showbuddy.delete_transcript_by_title(cls._transcript_title)
        logger.info(
            "Fireflies api requests count: %d",
            cls._showbuddy._fireflies.api_requests_count,
        )
