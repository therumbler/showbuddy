import logging
import unittest

from showbuddy import ShowBuddy


logger = logging.getLogger(__name__)

AUDIO_FILEPATH = "./tests/integration/files/test_audio_1.m4a"


class TestShowBuddy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logging.basicConfig(level=logging.INFO)
        cls._showbuddy = ShowBuddy()

    def test_showbuddy(self):

        resp = self._showbuddy.process(AUDIO_FILEPATH, [])
        print(resp)
        # assert False  # TODO: implement your test here

    @classmethod
    def tearDownClass(cls):
        logger.info("Tear down! deleting file")
        cls._showbuddy.delete_file(AUDIO_FILEPATH)
