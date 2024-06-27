import logging
import os

from .uploader import Uploader
import boto3

logger = logging.getLogger(__name__)


class ShowBuddy:
    def __init__(self):
        self._uploader = Uploader()

    def _process_business_card(self, business_card_filepath):
        pass

    def _process_business_cards(self, business_card_filepaths):
        return list(map(self._process_business_card, business_card_filepaths))

    def _upload_audio_to_s3(self, audio_filepath):
        file_name = os.path.basename(audio_filepath)
        logger.info("Uploading %s to s3", file_name)
        response = self._uploader.upload_file(audio_filepath)
        logger.info("s3 response: %r", response)
        return response

    def _process_audio(self, audio_filepath):
        s3_response = self._upload_audio_to_s3(audio_filepath)
        logger.info("s3_response %r", s3_response)
        return s3_response

    def process(self, audio_filepath, business_card_filepaths):
        audio_resp = self._process_audio(audio_filepath)
        # upload audio data to s3
        # get s3 url
        # call fireflies api with s3 url
        # get transcript
        # tag timestamp
        #
        return audio_resp

    def delete_file(self, audio_filepath):
        return self._uploader.delete_file(audio_filepath)


def test():
    """test things"""
    showbuddy = ShowBuddy()
    assert showbuddy is not None
    print("All tests pass")
