"""creates an ASGI app for Uvicorn to run"""

import logging
from fastapi import FastAPI, UploadFile, File
from lib.spreadly_service import SpreadlyService
from lib.assemblyai_service import AssemblyAIService

import config


logger = logging.getLogger(__name__)


def make_web_app():
    """creates an ASGI app for Uvicorn to run"""
    logging.basicConfig(level=logging.DEBUG)
    app = FastAPI()
    business_card_service = SpreadlyService(config.SPREADLY_API_KEY)
    transcription_service = AssemblyAIService(config.ASSEMBLYAI_API_KEY)

    @app.get("/")
    async def read_root():
        return {"Hello": "World"}

    @app.post("/api/sessions/{session_id}/cards")
    async def upload_card(session_id: str, image_file: UploadFile = File(...)):
        image_data = await image_file.read()
        card_data = await business_card_service.process_card(session_id, image_data)
        return card_data

    @app.post("/api/sessions/{session_id}/audio")
    async def process_audio(session_id: str, audio_file: UploadFile = File(...)):
        audio_data = await audio_file.read()
        transcription_data = await transcription_service.process(session_id, audio_data)
        return transcription_data
    
    return app
