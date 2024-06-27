import logging
import os

import boto3

logger = logging.getLogger(__name__)


class Uploader:
    def __init__(self):
        self._s3 = boto3.client("s3")
        self._s3_bucket_name = "showbuddy"
        self._s3_base_url = os.environ["AWS_ENDPOINT_URL"]

    def _get_full_url_for_file(self, file_name):
        base_url = self._s3_base_url.replace(
            "https://s3", f"https://{self._s3_bucket_name}.s3"
        )
        return f"{base_url}/{file_name}"

    def upload_file(self, audio_filepath) -> str:
        file_name = os.path.basename(audio_filepath)
        logger.debug("Uploading %s to s3", file_name)
        response = self._s3.upload_file(audio_filepath, self._s3_bucket_name, file_name)

        return self._get_full_url_for_file(file_name)

    def delete_file(self, audio_filepath) -> str:
        file_name = os.path.basename(audio_filepath)
        logger.warning("⚠️ Deleting %s from s3", file_name)
        response = self._s3.delete_object(Bucket=self._s3_bucket_name, Key=file_name)
        logger.debug("s3 response: %r", response)
        return response
