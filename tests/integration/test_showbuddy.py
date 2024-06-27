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

    def test_showbuddy(self):
        TestShowBuddy._uuid = str(uuid4())
        resp = self._showbuddy.process(AUDIO_FILEPATH, [], TestShowBuddy._uuid)
        logger.info("process response: %r", resp)

        assert "errors" not in resp

    @classmethod
    def tearDownClass(cls):
        logger.info("Tear down! deleting file and transcript")
        cls._showbuddy.delete_file(AUDIO_FILEPATH)
        cls._showbuddy.delete_transcript(cls._uuid)
