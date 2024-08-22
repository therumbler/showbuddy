"""Main module for ShowBuddy"""

import asyncio
import logging
import os
from uuid import uuid4

# from lib.fireflies import Fireflies
from lib.assemblyai import AssemblyAI
from lib.spreadly import Spreadly
from .uploader import Uploader
from .showbuddysessions import ShowBuddySessions

logger = logging.getLogger(__name__)


class ShowBuddy:
    """Class to pull it all together"""

    def __init__(self):
        self._uploader = Uploader()
        self._assemblyai = AssemblyAI(os.environ["ASSEMBLYAI_API_KEY"])
        self._spreadly = Spreadly(os.environ["SPREADLY_API_KEY"])
        self._sessions = ShowBuddySessions(showbuddy=self)

    async def _process_business_card(self, business_card_fileobj):
        return await self._spreadly.scan_card(business_card_fileobj)

    async def _process_business_cards(self, business_card_fileobjs):
        tasks = [self._process_business_card(bco) for bco in business_card_fileobjs]
        logger.debug("awaiting %d business card tasks", len(tasks))
        return await asyncio.gather(*tasks)

    async def process_audio(self, audio_fileobj):
        """Trigger the processing of an audio file"""
        audio_title = f"{str(uuid4())}.webm"

        audio_url = self._uploader.upload_fileobj(audio_fileobj, audio_title)
        logger.debug("audio_url %s", audio_url)

        resp = await self._assemblyai.start_transcript(audio_url)
        transcript_id = resp["id"]
        attempts = 0
        while resp["status"] != "completed":
            resp = await self._assemblyai.fetch_transcript(transcript_id)
            if resp["status"] == "completed":
                break
            attempts += 1
            if attempts > 5:
                logger.error('max attempts reached for "%s"', audio_title)
                break

            await asyncio.sleep(5)
        return resp

    async def process(self, audio_fileobj, business_card_fileobjs):
        """Trigger the processing of an audio file and business cards"""
        business_card_resp = await self._process_business_cards(business_card_fileobjs)
        logger.info("got business card resp %s", business_card_resp)

        transcript = await self.process_audio(audio_fileobj)
        logger.info("got transcript resp %r", transcript)

        return {"business_card_resp": business_card_resp, "transcript": transcript}

    async def process_image(self, image_fileobj):
        """Trigger the processing of an image file"""

        return await self._spreadly.scan_card(image_fileobj)

    def delete_file(self, filename):
        """used by integration tests to clean up after themselves"""
        return self._uploader.delete_file(filename)

    async def delete_transcript(self, transcript_id):
        """used by integration tests to clean up after themselves"""
        return await self._assemblyai.delete_transcript(transcript_id)

    async def add_websocket(self, websocket):
        """process data from a websocket connection"""
        logger.info("ShowBuddy add_websocket")
        await self._sessions.add_websocket(websocket)

    async def remove_websocket(self, websocket):
        """remove a websocket connection"""
        logger.info("ShowBuddy remove_websocket")
        await self._sessions.remove_websocket(websocket)

    async def process_websocket_data(self, data):
        await self._sessions.process_websocket_data(data)

    async def process_callback(self, data):
        """process a callback from a webhook"""
        logger.info("got callback data %s", data)
        await self._sessions.process_callback(data)
        return {"status": "ok"}
