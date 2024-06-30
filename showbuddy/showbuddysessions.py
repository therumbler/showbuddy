"""Module for ShowBuddySessions class."""

import asyncio
import json
import logging


logger = logging.getLogger(__name__)


class ShowBuddySessions:
    """used to track sessions and deal with websocket connections"""

    def __init__(self, showbuddy):
        self._showbuddy = showbuddy
        self._websockets = []

    async def add_websocket(self, websocket):
        """add a websocket to the session"""
        logger.info("ShowBuddySessions add_websocket")
        self._websockets.append(websocket)
        # asyncio.create_task(self._process_websocket(websocket))

    async def remove_websocket(self, websocket):
        """remove a websocket from the session"""
        logger.info("ShowBuddySessions remove_websocket")
        self._websockets.remove(websocket)

    async def _process_websocket(self, websocket):
        """process data from a websocket"""
        logger.info("_process_websocket")
        while True:
            data = await websocket.receive_text()
            logger.info("recevied text %s", data)

    async def process_callback(self, data):
        """process data from a callback"""
        logger.info(
            "processing Session callback %s to %d websockets",
            data,
            len(self._websockets),
        )
        for ws in self._websockets:
            await ws.send_text(json.dumps(data))
        return data

    async def process_websocket_data(self, data):
        return {"success": True}
