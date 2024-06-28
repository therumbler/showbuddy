import logging
import unittest

import os

from lib.spreadly import Spreadly

logger = logging.getLogger(__name__)

CARD_FILEPATH = "./tests/integration/files/tsepo_montsi.zo.ca_business_card.jpg"


class TestSpreadly(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logging.basicConfig(level=logging.DEBUG)

        cls._spreadly = Spreadly(os.environ["SPREADLY_API_KEY"])

    def test_spreadly(self):
        logger.info("starting test_spreadly with CARD_FILEPATH: %s", CARD_FILEPATH)
        resp = self._spreadly.scan_card(CARD_FILEPATH)
        logger.info("scan_card response: %r", resp)

        assert "errors" not in resp
        assert resp["given_name"] == "Tsepo"
        assert resp["family_name"] == "Montsi"
        assert "http://www.montsi.co.za" in resp["websites"]

    @classmethod
    def tearDownClass(cls):
        logger.info("Tear down! deleting file and transcript")
        cls._spreadly.delete_scan(CARD_FILEPATH)
        requests = cls._spreadly.api_requests_count
        logger.info("Spreadly API requests count: %d", requests)
