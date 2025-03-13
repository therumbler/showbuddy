import config
import logging
from fastapi import FastAPI
from lib.spreadly_service import SpreadlyService
import os



logger = logging.getLogger(__name__)    

def make_web_app():
    app = FastAPI()
    business_card_service = SpreadlyService(config.SPREADLY_API_KEY)

    @app.get("/")
    async def read_root():
        return {"Hello": "World"}


    @app.post("/api/sessions/{session_id}/cards")
    async def upload_card(session_id: str, image_path: str):
        print(f"Processing card for session {session_id}...")
        card_data = await business_card_service.upload_card(session_id, image_path)
        return card_data
    
    return app

