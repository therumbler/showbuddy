"""Unit tests for ShowBuddy class"""

from io import BytesIO
import logging
import os
import json
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch, MagicMock, AsyncMock
from showbuddy import ShowBuddy


logger = logging.getLogger(__name__)
mocked_upload_file = MagicMock(return_value="http://example.com/file.mp3")
mocked_start_transcript = AsyncMock(return_value={"id": "fake", "status": "queued"})
mocked_fetch_transcript = AsyncMock(
    return_value={"id": "fake", "status": "completed", "utterances": []}
)
mocked_scan_card = AsyncMock(return_value={"status": "completed"})
mock_fetch_completions = AsyncMock(
    return_value={"choices": [{"message": {"content": "Summarized text"}}]}
)


class TestShowBuddy(IsolatedAsyncioTestCase):
    """Test the ShowBuddy class"""

    def setUp(self):
        os.environ["AWS_ENDPOINT_URL"] = "http://localhost:4566"
        os.environ["ASSEMBLYAI_API_KEY"] = "fake"
        os.environ["SPREADLY_API_KEY"] = "fake"
        os.environ["AWS_ACCESS_KEY_ID"] = "fake"
        os.environ["AWS_SECRET_ACCESS_KEY"] = "fake"
        os.environ["OPENAI_ORGANIZATION_ID"] = "fake"
        os.environ["OPENAI_PROJECT_ID"] = "fake"
        os.environ["OPENAI_API_KEY"] = "fake"
        self.showbuddy = ShowBuddy()

    async def test_showbuddy(self):
        """ensure the ShowBuddy instance is created"""
        assert self.showbuddy is not None

    @patch("showbuddy.showbuddy.Uploader.upload_fileobj", mocked_upload_file)
    @patch("showbuddy.showbuddy.AssemblyAI.start_transcript", mocked_start_transcript)
    @patch("showbuddy.showbuddy.AssemblyAI.fetch_transcript", mocked_fetch_transcript)
    @patch("showbuddy.showbuddy.OpenAI.fetch_completions", mock_fetch_completions)
    async def test_process_audio(self):
        """Test processing an audio file"""
        audio_fileobj = BytesIO(b"fake audio data")

        resp = await self.showbuddy.process_audio(audio_fileobj)
        assert resp is not None
        assert resp["text"] == "Summarized text"

    @patch("showbuddy.showbuddy.Spreadly.scan_card", mocked_scan_card)
    async def test_process_image(self):
        """Test processing an image file"""
        image_fileobj = BytesIO(b"fake image data")

        resp = await self.showbuddy.process_image(image_fileobj)

        assert resp is not None

    def test_extract_dialog_assemblyai(self):
        assembyai_response = {
            "utterances": [
                {"speaker": "B", "text": "Hello. My name is Tepo. What's your name?"},
                {"speaker": "A", "text": "Hey, I'm Benjamin. I work at Manatee."},
                {
                    "speaker": "B",
                    "text": "Hey, Benjamin. Great to meet you. I've heard great things about this Monati company.",
                },
                {
                    "speaker": "A",
                    "text": "Yeah, we make iced teas from basically out of paper.",
                },
                {
                    "speaker": "B",
                    "text": "Thank you. It's great doing business with you. All the best.",
                },
                {"speaker": "A", "text": "Yeah, you, too. Have a good day."},
                {"speaker": "B", "text": "Good day."},
            ]
        }

        expected = """Speaker B: Hello. My name is Tepo. What's your name?

Speaker A: Hey, I'm Benjamin. I work at Manatee.

Speaker B: Hey, Benjamin. Great to meet you. I've heard great things about this Monati company.

Speaker A: Yeah, we make iced teas from basically out of paper.

Speaker B: Thank you. It's great doing business with you. All the best.

Speaker A: Yeah, you, too. Have a good day.

Speaker B: Good day."""
        dialog = self.showbuddy.extract_dialog_assemblyai(assembyai_response)
        assert dialog == expected
