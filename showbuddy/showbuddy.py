"""Main module for ShowBuddy"""

import asyncio
import logging
import os
from uuid import uuid4

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

    async def _process_business_card(self, business_card_fileobj):
        return await self._spreadly.scan_card(business_card_fileobj)

    async def _process_business_cards(self, business_card_fileobjs):
        tasks = [self._process_business_card(bco) for bco in business_card_fileobjs]
        logger.debug("awaiting %d business card tasks", len(tasks))
        return await asyncio.gather(*tasks)

    def extract_dialog_assemblyai(self, transcript):
        """Extract the transcript from the response"""
        paragraphs = []
        for utterance in transcript["utterances"]:
            speaker_label = utterance["speaker"]
            text = utterance["text"]
            paragraphs.append(f"Speaker {speaker_label}: {text}")

        # Join paragraphs into the final formatted text
        formatted_text = "\n\n".join(paragraphs)

        # Output the formatted text
        logger.info("formatted_text %s", formatted_text)
        return formatted_text

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
                dialog = self.extract_dialog_assemblyai(resp)
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
