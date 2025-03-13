"""creates an ASGI app for Uvicorn to run"""

import logging
from fastapi import FastAPI
from lib.spreadly_service import SpreadlyService

from schemas.carduploadrequest import CardUploadRequest
import config


logger = logging.getLogger(__name__)


def make_web_app():
    """creates an ASGI app for Uvicorn to run"""
    logging.basicConfig(level=logging.DEBUG)
    app = FastAPI()
    business_card_service = SpreadlyService(config.SPREADLY_API_KEY)

    @app.get("/")
    async def read_root():
        return {"Hello": "World"}

    @app.post("/api/cards")
    async def upload_card(request: CardUploadRequest):
        card_data = await business_card_service.upload_card(
            request.session_id, request.image_path
        )
        return card_data

    return app
