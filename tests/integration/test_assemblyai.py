"""Integration tests for the AssemblyAI API"""

import asyncio
import os
from unittest import IsolatedAsyncioTestCase
from uuid import uuid4

from lib.assemblyai import AssemblyAI
from showbuddy.uploader import Uploader


AUDIO_FILEPATH = "./tests/integration/files/test_audio_1a.m4a"
AUDIO_FILENAME = f"{str(uuid4())}.m4a"


class TestAssemblyAI(IsolatedAsyncioTestCase):
    """Integration tests for the AssemblyAI API"""

    def setUp(self):
        self.assemblyai = AssemblyAI(os.environ["ASSEMBLYAI_API_KEY"])
        self.uploader = Uploader()
        self.audio_url = self.uploader.upload_file_by_filepath(
            AUDIO_FILEPATH, AUDIO_FILENAME
        )

    async def asyncSetUp(self):
        self.transcript = await self.assemblyai.start_transcript(self.audio_url)
        self.transcript_id = self.transcript["id"]
        attempts = 0
        while self.transcript["status"] != "completed":
            await asyncio.sleep(5)
            self.transcript = await self.assemblyai.fetch_transcript(self.transcript_id)
            attempts += 1
            if attempts > 5:
                raise OverflowError("max attempts reached")

    def test_assemblyai(self):
        """simple test to check if the response is as expected"""
        assert self.assemblyai is not None

    def test_transcript_status(self):
        """ensure the transcript status is completed"""
        assert self.transcript["status"] == "completed"

    def test_transcript_has_speaker(self):
        """make sure the transcript has speaker labels"""
        assert self.transcript["words"][0]["speaker"] is not None

    async def asyncTearDown(self):
        self.uploader.delete_file(AUDIO_FILENAME)
        await self.assemblyai.delete_transcript(self.transcript_id)
