import asyncio
import websockets
from fastapi import FastAPI, WebSocket
from backend.devices.microphone_device import MicrophoneDevice
from backend.devices.speaker_device import SpeakerDevice
from backend.gateways.audio_gateway import AudioGateway
from fastapi.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocketDisconnect
from loguru import logger
import traceback
from openai import OpenAI
from dotenv import load_dotenv
import keyboard
import uvicorn
import sys

from backend.api.routes import microphone, speaker
from backend.api.routes.speaker import speaker as speaker_device

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change for security)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI()

audio_gateway = AudioGateway(client)
microphone_device = MicrophoneDevice("1")

audio_gateway.add_microphone(microphone=microphone_device)
audio_gateway.add_speaker(speaker=speaker_device)

app.include_router(microphone.router, prefix="/microphone", tags=["Microphone"])
app.include_router(speaker.router, prefix="/speaker", tags=["Speaker"])


if __name__ == "__main__":
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        log_config=None,
        log_level="info"
    )