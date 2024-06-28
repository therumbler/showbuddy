import logging
import os

import boto3

logger = logging.getLogger(__name__)


class Uploader:
    def __init__(self):
        self._s3 = boto3.client("s3")
        self._bucket_name = "showbuddy"
        self._s3_base_url = os.environ["AWS_ENDPOINT_URL"]

    def _get_full_url_for_file(self, file_name):
        base_url = self._s3_base_url.replace(
            "https://s3", f"https://{self._bucket_name}.s3"
        )
        return f"{base_url}/{file_name}"

    def upload_file(self, audio_fileobj, file_name) -> str:
        # file_name = audio_fileobj.filename
        logger.info("Uploading %s to s3", file_name)
        response = self._s3.upload_fileobj(audio_fileobj, self._bucket_name, file_name)

        return self._get_full_url_for_file(file_name)

    def delete_file(self, audio_fileobj) -> str:
        file_name = os.path.basename(audio_fileobj)
        logger.warning("⚠️ Deleting %s from s3", file_name)
        response = self._s3.delete_object(Bucket=self._bucket_name, Key=file_name)
        logger.debug("s3 response: %r", response)
        return response
