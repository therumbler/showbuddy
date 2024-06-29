"""Main module for ShowBuddy"""

import asyncio
import logging
import os

# from lib.fireflies import Fireflies
from lib.assemblyai import AssemblyAI
from lib.spreadly import Spreadly
from .uploader import Uploader


logger = logging.getLogger(__name__)


class ShowBuddy:
    """Class to pull it all together"""

    def __init__(self):
        self._uploader = Uploader()
        self._assemblyai = AssemblyAI(os.environ["ASSEMBLYAI_API_KEY"])
        self._spreadly = Spreadly(os.environ["SPREADLY_API_KEY"])
        logger.info("ShowBuddy initialized")

    async def _process_business_card(self, business_card_fileobj):
        return await self._spreadly.scan_card(business_card_fileobj)

    async def _process_business_cards(self, business_card_fileobjs):
        tasks = [self._process_business_card(bco) for bco in business_card_fileobjs]
        logger.debug("awaiting %d business card tasks", len(tasks))
        return await asyncio.gather(*tasks)

    async def _process_audio(self, audio_fileobj, audio_title):
        logger.warning('skipping audio processing "%s"', audio_title)

        audio_url = self._uploader.upload_file(audio_fileobj, audio_title)
        logger.debug("audio_url %s", audio_url)

        resp = await self._assemblyai.start_transcript(audio_url)
        transcript_id = resp["id"]
        attempts = 0
        while resp["status"] == "queued":
            attempts += 1
            if attempts > 5:
                logger.error('max attempts reached for "%s"', audio_title)
                break
            await asyncio.sleep(5)
            resp = await self._assemblyai.fetch_transcript(transcript_id)

        return resp

    async def process(self, audio_fileobj, business_card_fileobjs, audio_title):
        """Trigger the processing of an audio file and business cards"""

        business_card_resp = await self._process_business_cards(business_card_fileobjs)

        logger.info("got business card resp %s", business_card_resp)
        # return
        transcript = await self._process_audio(audio_fileobj, audio_title)
        logger.info("got transcript resp %r", transcript)

        return {"business_card_resp": business_card_resp, "transcript": transcript}

    def delete_file(self, audio_fileobj):
        """used by integration tests to clean up after themselves"""
        return self._uploader.delete_file(audio_fileobj)

    async def delete_transcript(self, transcript_id):
        """used by integration tests to clean up after themselves"""
        return await self._assemblyai.delete_transcript(transcript_id)
