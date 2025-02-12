from devices.src.gateways.interfaces.common.authenticate import Authenticate
from devices.src.smart_devices.interfaces.control_speaker import ControlSpeaker
from fastapi import WebSocket
import websockets
from loguru import logger
from starlette.websockets import WebSocketDisconnect
import webrtcvad
import traceback

class AudioGateway:
    def __init__(self, microphone, speaker, speaker_server_url):
        self.microphone = microphone
        self.speaker = speaker
        self.speaker_server_url = speaker_server_url
        self.websocket = None

    async def stream_audio(self, websocket: WebSocket):
        """Receives audio from WebSocket and plays it on the speaker."""
        await websocket.accept()
        print("🔊 AudioGateway: WebSocket Connection Accepted")  # ✅ Debug connection
        
        try:
            while True:
                audio_data = await websocket.receive_bytes()
                logger.info(f"Received {len(audio_data)} bytes from WebSocket")  # ✅ Log received data
                
                if self.speaker:
                    logger.info(f"Sending {len(audio_data)} bytes to SpeakerDevice")  # ✅ Confirm forwarding
                    self.speaker.play_audio(audio_data)  # 🔥 Send to speaker
                else:
                    print("⚠️ No SpeakerDevice attached!")
        except WebSocketDisconnect:
            logger.warning("WebSocket Disconnected.")
        except Exception as e:
            logger.error(f"⚠️ AudioGateway Error: {e}")
        finally:
            logger.info("Connection Closed.")

    async def connect_speaker(self):
        """Establish a persistent WebSocket connection to the speaker."""
        try:
            self.websocket = await websockets.connect(self.speaker_server_url)
            print("🔗 Connected to Speaker WebSocket.")
        except Exception as e:
            print(f"⚠️ Failed to connect to speaker: {e}")
            self.websocket = None
            
    async def send_audio(self, audio_data: bytes):
        """Send audio data to the Speaker WebSocket."""
        if not self.websocket or self.websocket.close_code is not None:
            await self.connect_speaker()

        if self.websocket:
            try:
                await self.websocket.send(audio_data)
                print(f"📢 Sent {len(audio_data)} bytes to Speaker WebSocket")
            except websockets.exceptions.ConnectionClosed:
                print("⚠️ Speaker WebSocket closed unexpectedly. Reconnecting...")
                self.websocket = None
            except Exception as e:
                traceback.print_exc()
                logger.error(f"⚠️ Error sending audio to speaker: {e}")