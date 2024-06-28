import logging
import sys

from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from showbuddy import ShowBuddy

logger = logging.getLogger(__name__)


def make_app():
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    showbuddy = ShowBuddy()
    app = FastAPI()
    app.mount("/static", StaticFiles(directory="static"), name="static")

    @app.get("/")
    async def index_static():
        return FileResponse("static/index.html")

    @app.get("/app")
    async def app_static():
        return FileResponse("static/app.html")
        # return FileResponse("static/dropover_tmp.html")

    @app.post("/api/process")
    async def process(image: UploadFile = File(...), audio: UploadFile = File(...)):
        logger.info("image: %s", image.filename)
        logger.info("audio: %s", audio.filename)
        resp = await showbuddy.process(audio, [image], audio.filename)
        return resp

    return app
