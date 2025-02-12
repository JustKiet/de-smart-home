import asyncio
import websockets
from fastapi import FastAPI, WebSocket
from devices.src.smart_devices.microphone_device import MicrophoneDevice
from devices.src.smart_devices.speaker_device import SpeakerDevice
from devices.src.gateways.audio_gateway import AudioGateway
from fastapi.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocketDisconnect
from loguru import logger
import traceback

# WebSocket server URL (ensure it matches your FastAPI server)
MICROPHONE_SERVER_URL = "ws://localhost:8001/microphone_stream"
SPEAKER_SERVER_URL = "ws://localhost:8001/speaker_stream"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change for security)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

microphone = MicrophoneDevice("1", MICROPHONE_SERVER_URL)
speaker = SpeakerDevice("1")
audio_gateway = AudioGateway(microphone, speaker, SPEAKER_SERVER_URL)

# ✅ FastAPI WebSocket Server Endpoints
@app.websocket("/microphone_stream")
async def microphone_stream(websocket: WebSocket):
    """Handles WebSocket connections from the microphone."""
    await websocket.accept()
    microphone.turn_on()
    
    try:
        while True:
            data = await websocket.receive_bytes()
            logger.info(f"Received {len(data)} bytes of audio data.")
            await asyncio.sleep(0.05)  # Simulate processing delay
            await audio_gateway.send_audio(data)
    except WebSocketDisconnect:
        logger.warning("Microphone WebSocket disconnected.")
    except Exception as e:
        logger.error(f"Error streaming audio from microphone: {e}")
        traceback.print_exc()
    finally:
        logger.info("Microphone WebSocket closed.")

@app.websocket("/speaker_stream")
async def speaker_stream(websocket: WebSocket):
    """Handles WebSocket connections for the speaker."""
    await websocket.accept()
    logger.info("Speaker connected to WebSocket.")
    try:
        while True:
            data = await websocket.receive_bytes()
            logger.info(f"Received {len(data)} bytes of audio data.")
            speaker.play_audio(data)
    except Exception as e:
        logger.error(f"Error streaming audio to speaker: {e}")
    finally:
        logger.info("Speaker disconnected from WebSocket.")

async def websocket_client():
    """Client function to send microphone audio to the FastAPI WebSocket."""
    microphone.turn_on()
    try:
        async with websockets.connect(MICROPHONE_SERVER_URL) as websocket:
            print("🎤 Connected to WebSocket Server at:", MICROPHONE_SERVER_URL)
            
            async for audio_data in microphone.record_audio():  # ✅ Stream audio data
                await websocket.send(audio_data)
                await asyncio.sleep(0.02)

    except websockets.exceptions.ConnectionClosed:
        print("❌ Connection closed by server")
    finally:
        print("🔴 Closing WebSocket client connection")
        microphone.turn_off()

if __name__ == "__main__":
    try:
        asyncio.run(websocket_client())
    except KeyboardInterrupt:
        print("\nStreaming stopped by user. Exiting gracefully.")