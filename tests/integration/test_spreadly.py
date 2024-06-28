"""Integration tests for the Spreadly API"""

import asyncio
import logging
from unittest import TestCase

import os

from lib.spreadly import Spreadly

logger = logging.getLogger(__name__)

CARD_FILEPATH = "./tests/integration/files/tsepo_montsi.zo.ca_business_card.jpg"


class TestSpreadly(TestCase):
    """Integration tests for the Spreadly API"""

    @classmethod
    def setUpClass(cls):
        logging.basicConfig(level=logging.DEBUG)

        cls._spreadly = Spreadly(os.environ["SPREADLY_API_KEY"])
        with open(CARD_FILEPATH, "rb") as f:
            logger.info("starting scan_card with CARD_FILEPATH: %s", CARD_FILEPATH)
            resp = asyncio.run(cls._spreadly.scan_card(f))
            cls._resp = resp
            logger.info("scan_card response: %r", resp)

    def test_spreadly(self):
        """simple test to check if the response is as expected"""
        assert "errors" not in self._resp
        assert self._resp["given_name"] == "Tsepo"
        assert self._resp["family_name"] == "Montsi"
        assert "http://www.montsi.co.za" in self._resp["websites"]

    @classmethod
    def tearDownClass(cls):
        logger.info("Tear down! deleting scan")
        cls._spreadly.delete_scan(CARD_FILEPATH)
        requests = cls._spreadly.api_requests_count
        logger.info("Spreadly API requests count: %d", requests)
