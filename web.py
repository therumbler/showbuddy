"""FastAPI web server for ShowBuddy"""

import logging
import os
import sys

from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from showbuddy import ShowBuddy

logger = logging.getLogger(__name__)

APP_MODE = os.getenv("APP_MODE", "landing")


def make_app():
    """create a FastAPI ASGI app"""
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

    app = FastAPI()
    app.mount("/static", StaticFiles(directory="static"), name="static")

    if APP_MODE == "landing":
        logger.info("running in landing mode")

        @app.get("/")
        async def index_static():
            return FileResponse("static/landing.html")

    if APP_MODE == "app":
        logger.info("running in app mode")
        showbuddy = ShowBuddy()

        @app.get("/")
        async def app_static():
            return FileResponse("static/app.html")

        @app.post("/api/process")
        async def process(image: UploadFile = File(...), audio: UploadFile = File(...)):
            logger.info("image: %s", image.filename)
            logger.info("audio: %s", audio.filename)
            resp = await showbuddy.process(audio, [image.file])
            return resp

        @app.post("/api/audio")
        async def process_audio(audio: UploadFile = File(...)):
            logger.info("audio: %s", audio.filename)
            resp = await showbuddy.process_audio(audio.file)
            return resp

        @app.post("/api/image")
        async def process_image(image: UploadFile = File(...)):
            resp = await showbuddy.process_image(image.file)
            return resp

    return app
