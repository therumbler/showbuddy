"""Module for uploading files to S3 using Boto3"""

import logging
import os

import boto3

logger = logging.getLogger(__name__)


class Uploader:
    """Class for interacting with S3 (Boto3)"""

    def __init__(self):
        self._s3 = boto3.client("s3")
        self._bucket_name = "showbuddy"
        self._s3_base_url = os.environ["AWS_ENDPOINT_URL"]

    def _get_full_url_for_file(self, file_name):
        base_url = self._s3_base_url.replace(
            "https://s3", f"https://{self._bucket_name}.s3"
        )
        return f"{base_url}/{file_name}"

    def upload_file_by_filepath(self, file_path, file_name) -> str:
        """upload a file using S3 (Boto3) and return the URL"""
        with open(file_path, "rb") as f:
            return self.upload_fileobj(f, file_name)

    def upload_fileobj(self, audio_fileobj, file_name) -> str:
        """upload a file using S3 (Boto3) and return the URL"""
        logger.info("Uploading %s to s3", file_name)
        self._s3.upload_fileobj(audio_fileobj, self._bucket_name, file_name)

        return self._get_full_url_for_file(file_name)

    def delete_file(self, file_name) -> str:
        """Delete a file from S3 (for itegration test cleanup)"""
        logger.warning("⚠️ Deleting %s from s3", file_name)
        response = self._s3.delete_object(Bucket=self._bucket_name, Key=file_name)
        logger.debug("s3 response: %r", response)
        return response
