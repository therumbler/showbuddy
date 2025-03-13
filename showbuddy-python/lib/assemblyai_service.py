"""module to hit spreadly.app"""

import asyncio
import logging
import os
from datetime import datetime


import httpx

logger = logging.getLogger(__name__)


class AssemblyAIService:
    """service to hit https://assemblyai.com/api"""

    def __init__(self, api_key: str):
        self.api_key = api_key

    async def upload_audio(self, session_id: str, audio_data: bytes):
        """Upload a audio file"""

        transcript_data = await self._process_audio(session_id, audio_data)
        return transcript_data

    async def _process_audio(self, session_id: str, audio_data: bytes):
        """Process audiousing assemvly.io"""
        logger.info("Processing audio for session %s...", session_id)

        try:
            # Make API request to Spreadly.io
            # Set headers with Bearer token and Content-Type
            headers = {
                "Authorization": f"Bearer {self.api_key}",
            }
            logger.info("uploading a file of length %d", len(audio_data))
            files = {
                "front": ("audio.m4a", audio_data),
            }

            # Make the POST request with requests
            async with httpx.AsyncClient() as client:
                logger.info("Uploading audio data to AssemblyAI")
                response = await client.post(
                    "https://api.assemblyai.com/v2/transcript",
                    headers=headers,
                    files=files,
                    timeout=30.0,
                )

            if response.status_code != 200:
                logger.info("Audio processing failed: %d", response.status_code)
                return

            try:
                transcript_data = response.json()
            except ValueError:
                logger.error("Audio processing failed: Invalid JSON response")
                return

            transcript_data["response_type"] = "transcript_data"
            transcript_data["session_id"] = session_id

            logger.info("Audio processing completed for session %s", session_id)
            logger.info("Retrieved transcript data: %r", transcript_data)
            return transcript_data

        except Exception as e:
            logger.exception("Error processing audio: %s", e)


async def main():
    """transcribe 2 conversations asyncronously"""
    logging.basicConfig(level=logging.DEBUG)
    api_key = os.environ["SPREADLY_API_KEY"]
    session_id = "your_session_id_here"
    audio_path0 = "../tests/integration/files/oz-0.m4q"
    audio_path1 = "../tests/integration/files/oz-1.m4a"

    transcription_service = AssemblyAIService(api_key=api_key)

    with open(audio_path0, "rb") as audio0:
        with open(audio_path1, "rb") as audio1:

            results = await asyncio.gather(
                transcription_service.upload_audio(session_id, audio1.read()),
                # transcription_service.upload_audio(session_id, audio2.read()),
            )

    # print(results)


if __name__ == "__main__":

    asyncio.run(main())
