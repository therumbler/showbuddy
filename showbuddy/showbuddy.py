import logging
import os

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

    def process(self, audio_filepath, business_card_filepaths):
        audio_url = self._process_audio(audio_filepath)
        logger.info("got audo_url %s", audio_url)

        # call fireflies api with s3 url
        resp = self._fireflies.upload_audio(audio_url)
        logger.info("fireflies response %r", resp)
        # get transcript
        # tag timestamp
        #
        return resp

    def delete_file(self, audio_filepath):
        return self._uploader.delete_file(audio_filepath)


def test():
    """test things"""
    showbuddy = ShowBuddy()
    assert showbuddy is not None
    print("All tests pass")
