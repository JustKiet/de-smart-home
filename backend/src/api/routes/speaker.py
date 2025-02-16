from fastapi import APIRouter, WebSocket
import asyncio
from loguru import logger
from devices.src.smart_devices.speaker_device import SpeakerDevice
import traceback


router = APIRouter()
speaker = SpeakerDevice("1")
speaker.turn_on()

@router.websocket("/speaker_stream")
async def speaker_stream(websocket: WebSocket):
    """Handles WebSocket connections for the speaker."""
    await websocket.accept()
    logger.info("Speaker connected to WebSocket.")
    try:
        while True:
            data = await websocket.receive_bytes()
            #logger.info(f"Received {len(data)} bytes of audio data.")
            logger.debug(f"data type: {type(data)}")
            if isinstance(data, bytes):
                speaker.play_audio(data)
            else:
                logger.error(f"Data is not in bytes format: {type(data)}")
    except Exception as e:
        logger.error(f"Error streaming audio to speaker: {e}")
        traceback.print_exc()
    finally:
        logger.info("Speaker disconnected from WebSocket.")