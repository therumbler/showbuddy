import logging
import sys

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


logger = logging.getLogger(__name__)


def make_app():
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    app = FastAPI()
    app.mount("/static", StaticFiles(directory="static"), name="static")

    @app.get("/")
    async def index():
        logger.debug("in index")
        return FileResponse("static/index.html")

    return app
