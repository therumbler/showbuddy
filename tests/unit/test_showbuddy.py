"""Unit tests for ShowBuddy class"""

from io import BytesIO
import logging
import os
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch, MagicMock, AsyncMock
from showbuddy import ShowBuddy


logger = logging.getLogger(__name__)
mocked_upload_file = MagicMock(return_value="http://example.com/file.mp3")
mocked_start_transcript = AsyncMock(return_value={"id": "fake", "status": "queued"})
mocked_fetch_transcript = AsyncMock(return_value={"id": "fake", "status": "completed"})
mocked_scan_card = AsyncMock(return_value={"status": "completed"})


class TestShowBuddy(IsolatedAsyncioTestCase):
    """Test the ShowBuddy class"""

    def setUp(self):
        os.environ["AWS_ENDPOINT_URL"] = "http://localhost:4566"
        os.environ["ASSEMBLYAI_API_KEY"] = "fake"
        os.environ["SPREADLY_API_KEY"] = "fake"
        os.environ["AWS_ACCESS_KEY_ID"] = "fake"
        os.environ["AWS_SECRET_ACCESS_KEY"] = "fake"
        self.showbuddy = ShowBuddy()

    async def test_showbuddy(self):
        """ensure the ShowBuddy instance is created"""
        assert self.showbuddy is not None

    @patch("showbuddy.showbuddy.Uploader.upload_fileobj", mocked_upload_file)
    @patch("showbuddy.showbuddy.AssemblyAI.start_transcript", mocked_start_transcript)
    @patch("showbuddy.showbuddy.AssemblyAI.fetch_transcript", mocked_fetch_transcript)
    async def test_process_audio(self):
        """Test processing an audio file"""
        audio_fileobj = BytesIO(b"fake audio data")

        resp = await self.showbuddy.process_audio(audio_fileobj)
        assert resp is not None
        assert resp["status"] == "completed"

    @patch("showbuddy.showbuddy.Spreadly.scan_card", mocked_scan_card)
    async def test_process_image(self):
        """Test processing an image file"""
        image_fileobj = BytesIO(b"fake image data")

        resp = await self.showbuddy.process_image(image_fileobj)

        assert resp is not None
