"""module to hit assemblyai transcription interface"""

import asyncio
import logging
import os
from datetime import datetime
import httpx

logger = logging.getLogger(__name__)


class AssemblyAIService:
    """service to hit https://assemblyai.com/api"""

    def __init__(self, api_key: str):
        self._api_key = api_key
        self._fetch_until_complete_sleep = 5
        self._fetch_until_complete_count = 5



    async def _upload_audio(self, session_id: str, audio_data: bytes):
        """Upload  Audio to assembly.io"""
        logger.info("Processing audio for session %s...", session_id)

        try:
            # Make API request to AssemblyAI
            # Set headers with Bearer token and Content-Type
            headers = {
                "Authorization": self._api_key,
                "Content-Type": "application/octet-stream",
            }
            logger.info("uploading a file of length %d", len(audio_data))
            files = {
                "file": ("audio.m4a", audio_data),
            }

            # Make the POST request with requests
            async with httpx.AsyncClient() as client:
                logger.info("Uploading audio data to AssemblyAI")
                response = await client.post(
                    "https://api.assemblyai.com/v2/upload",
                    headers=headers,
                    content=audio_data,
                    timeout=30.0,
                )

            if response.status_code != 200:
                logger.info("Audio processing failed: %d", response.status_code)
                return

            try:
                json_response = response.json()
            except ValueError:
                logger.error("Audio processing failed: Invalid JSON response")
                return

            json_response["response_type"] = "transcript_data"
            json_response["session_id"] = session_id

            logger.info("Audio processing completed for session %s", session_id)
            logger.info("Retrieved transcript data: %r", json_response)
            return json_response

        except Exception as e:
            logger.exception("Error processing audio: %s", e)

    async def _fetch_transcript_until_complete(self, start_transcript_response):
        """fetch until the job is complete"""
        transcript_id = start_transcript_response["id"]
        counter = 0
        while True:
            response = await self._fetch_transcript(transcript_id)
            if response["status"] == "completed":
                return response
            counter += 1
            if counter > self._fetch_until_complete_count:
                logger.error("fetch_until_complete failed")
                return 
            await asyncio.sleep(self._fetch_until_complete_sleep)


    async def _fetch(self, endpoint, data=None, method="POST"):
        """Generic HTTP request using httpx"""
        url = f"https://api.assemblyai.com/v2/{endpoint}"
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "accept": "application/json",
        }
        logger.debug("Fetching url: %s", url)
        req = httpx.Request(method, url, headers=headers, json=data)
        async with httpx.AsyncClient() as client:
            resp = await client.send(req)
            data = resp.json()
            logger.info("data: %r", data)
            resp.raise_for_status()
            return data

    async def _start_transcript(self, upload_audio_response):
        """start a transcription job with AssemblyAI"""
        audio_url = upload_audio_response["upload_url"]
        endpoint = "transcript"
        data = {"audio_url": audio_url, "speaker_labels": True}
        return await self._fetch(endpoint, data)

    async def _fetch_transcript(self, transcript_id):
        """fetch a transcript by ID"""
        endpoint = f"transcript/{transcript_id}"
        return await self._fetch(endpoint, method="GET")

    async def _delete_transcript(self, transcript_id):
        """delete a transcription by ID"""
        logger.warning("⚠️ deleting AssemblyAI transcript %s", transcript_id)
        endpoint = f"transcript/{transcript_id}"
        return await self._fetch(endpoint, data={}, method="DELETE")  

    async def process(self, session_id: str, audio: bytes): 
        """let's kick this off"""
        upload_audio_response = await self._upload_audio(session_id, audio)
        start_transcript_response = await self._start_transcript(upload_audio_response)
        fetch_trascript_response = await self._fetch_transcript_until_complete(start_transcript_response)
        return fetch_trascript_response

async def main():
    """transcribe 2 conversations asyncronously"""
    logging.basicConfig(level=logging.INFO)
    api_key = os.environ["ASSEMBLYAI_API_KEY"]
    session_id = "your_session_id_here"
    
    audio_path0 = "/Users/tsepomontsi/projects/showbuddy/tests/integration/files/oz-0.m4a"
    audio_path1 = "/Users/tsepomontsi/projects/showbuddy/tests/integration/files/oz-1.m4a"
    audio_path2 = "/Users/tsepomontsi/projects/showbuddy/tests/integration/files/dialog.m4a"

    transcription_service = AssemblyAIService(api_key=api_key)

    with open(audio_path2, "rb") as audio0:
        results = await transcription_service.process(session_id, audio0.read())
        print(results)

    # with open(audio_path0, "rb") as audio0:
    #     with open(audio_path1, "rb") as audio1:

    #         results = await asyncio.gather(
    #             transcription_service.upload_audio(session_id, audio0.read()),
    #             # transcription_service.upload_audio(session_id, audio2.read()),
    #         )

    # print(results)


if __name__ == "__main__":

    asyncio.run(main())
