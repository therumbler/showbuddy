"""creates an ASGI app for Uvicorn to run"""

import logging
from fastapi import FastAPI, UploadFile, File
from lib.spreadly_service import SpreadlyService
from lib.assemblyai_service import AssemblyAIService
from lib.claude_service import ClaudeService
from lib.db import ShowbuddyDB

import config


logger = logging.getLogger(__name__)
db = ShowbuddyDB(config.DB_PATH)

def make_web_app():
    """creates an ASGI app for Uvicorn to run"""
    logging.basicConfig(level=logging.DEBUG)
    app = FastAPI()
    business_card_service = SpreadlyService(config.SPREADLY_API_KEY)
    transcription_service = AssemblyAIService(config.ASSEMBLYAI_API_KEY)
    analytics_service = ClaudeService(config.ANTHROPIC_API_KEY)
    

    @app.get("/")
    async def read_root():
        return {"Hello": "World"}

    @app.post("/api/sessions/{session_id}/cards")
    async def upload_card(session_id: str, image_file: UploadFile = File(...)):
        image_data = await image_file.read()
        card_data = await business_card_service.process_card(session_id, image_data)
        db.card.add(session_id, card_data)
        print ("All Cards!\n\n\n************\n\n",db.card.get_all_cards(session_id))
        return card_data

    @app.post("/api/sessions/{session_id}/audio")
    async def process_audio(session_id: str, audio_file: UploadFile = File(...)):
        audio_data = await audio_file.read()
        transcription_data = await transcription_service.process(session_id, audio_data)
        db.transcript.add(session_id, transcription_data)
        return transcription_data
    
    @app.post("/api/sessions/{session_id}/analysis")
    async def analyse_transcript(session_id: str, transcript_file: UploadFile = File(...), card_file: UploadFile = File(...)):
        session_report = await analytics_service.generate_report(session_id, transcript_file, card_file)
        db.report.add(session_id, session_report)
        return session_report
    
    return app
