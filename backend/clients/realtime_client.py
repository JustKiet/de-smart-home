import asyncio
import websockets
from loguru import logger
from backend.devices.microphone_device import MicrophoneDevice
from config import MICROPHONE_SERVER_URL

async def websocket_client():
    """Client function to send microphone audio to the FastAPI WebSocket."""
    try:
        microphone = MicrophoneDevice("1")
        microphone.turn_on()
        
        async with websockets.connect(MICROPHONE_SERVER_URL) as websocket:
            logger.info("Connected to WebSocket Server at:", MICROPHONE_SERVER_URL)
            
            async for audio_data in microphone.stream_audio():  # ✅ Stream audio data
                await websocket.send(audio_data)
                await asyncio.sleep(0.02)

    except websockets.exceptions.ConnectionClosed:
        logger.warning("Connection closed by server")
    finally:
        logger.info("Closing WebSocket client connection")