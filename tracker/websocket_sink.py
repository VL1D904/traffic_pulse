from sink import Sink
from frame_result_contract import FrameResultContract
from dotenv import load_dotenv
import os
import websockets
import json
import cv2
import base64
import numpy as np


class WebSocketSink(Sink):
    def __init__(self) -> None:
        self.websocket_url = os.getenv("WEBSOCKET_URL")
        self.websocket = None

    async def connect(self):
        self.websocket = await websockets.connect(
            self.websocket_url,
            ping_timeout=10,
            ping_interval=10
        )

    def process_frame(self, frame: np.ndarray) -> str:
        _, frame_bytes = cv2.imencode('.jpg', frame)
        frame_bytes = frame_bytes.tobytes()
        frame_bytes = base64.b64encode(frame_bytes).decode('utf-8')
        return frame_bytes 

    async def send_plot(self, frame_result: FrameResultContract, video_id: int) -> None:
        frame_bytes = self.process_frame(frame_result.processed_frame)
        frame_data = {video_id: frame_bytes}
        
        if self.websocket:
            try:
                await self.websocket.send(json.dumps(frame_data))
            except websockets.exceptions.ConnectionClosedError:
                print("Соединение закрылось")
                raise

    async def close(self) -> None:
        if self.websocket:
            await self.websocket.close()