from backend.devices.interfaces.control_microphone import ControlMicrophone
from backend.devices.interfaces.control_speaker import ControlSpeaker

from typing import List
from fastapi import WebSocket
import websockets
from loguru import logger
from starlette.websockets import WebSocketDisconnect
import traceback
from openai import OpenAI
import io
import wave
import httpx
from fastapi import Response
import base64
class SpeechProcessor:
    """A Speech Processor class to handle speech processing related tasks."""
    def __init__(self,
                 client: OpenAI):
        self.client = client
        
    def validate_wav(self, wav_bytes):
        """
        Validate if the given BytesIO object contains a valid WAV file.
        """
        try:
            with wave.open(wav_bytes, 'rb') as wf:
                num_channels = wf.getnchannels()
                sample_width = wf.getsampwidth()
                frame_rate = wf.getframerate()
                num_frames = wf.getnframes()

                logger.info(f"Valid WAV File: {num_channels} channels, {sample_width*8}-bit, {frame_rate}Hz, {num_frames} frames")
                return True
        except wave.Error as e:
            logger.error(f"Valid WAV File: {e}")
            return False

    def raw_bytes_to_wav(self, raw_audio_bytes, sample_rate=16000, num_channels=1, sample_width=2):
        """
        Convert raw PCM audio bytes into a WAV file-like object.
        
        :param raw_audio_bytes: Raw PCM audio data (bytes)
        :param sample_rate: Sample rate in Hz (e.g., 44100)
        :param num_channels: Number of audio channels (1=mono, 2=stereo)
        :param sample_width: Sample width in bytes (2 for 16-bit audio)
        :return: A BytesIO object containing the WAV file
        """
        wav_file = io.BytesIO()
        
        with wave.open(wav_file, 'wb') as wf:
            wf.setnchannels(num_channels)      # Mono or Stereo
            wf.setsampwidth(sample_width)      # 2 bytes = 16-bit PCM
            wf.setframerate(sample_rate)       # Sample rate in Hz
            wf.writeframes(raw_audio_bytes)    # Write raw PCM audio data

        wav_file.seek(0)  # Move back to start for reading
        return wav_file
    
    def speech_to_text(self, audio_data) -> str:
        """Convert speech audio data to text using OpenAI's API."""
        response = self.client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_data,
        )
        return response.text

class NamedBytesIO(io.BytesIO):
    def __init__(self, *args, name="audio.wav", **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name

class AudioGateway(SpeechProcessor):
    def __init__(self,
                 client: OpenAI,
                 assistant_server_url: str = None,
                 speaker_server_url: str = None):
        super().__init__(client)
        self.microphones = {}
        self.speakers = {}
        self.assistant_server_url = assistant_server_url
        self.speaker_server_url = speaker_server_url
        self.websocket = None

    async def connect_speaker(self):
        """Establish a persistent WebSocket connection to the speaker."""
        try:
            self.websocket = await websockets.connect(self.speaker_server_url)
            logger.info(f"Connected to Speaker WebSocket at: {self.speaker_server_url}")
        except Exception as e:
            logger.error(f"Failed to connect to speaker: {e}")
            self.websocket = None
            
    def add_microphone(self, microphone: ControlMicrophone):
        self.microphones[microphone.device_id] = microphone
        self.microphones[microphone.device_id].turn_on()
        
    def get_microphone(self, device_id: str):
        return self.microphones.get(device_id, None)
    
    def add_speaker(self, speaker: ControlSpeaker):
        self.speakers[speaker.device_id] = speaker
        self.speakers[speaker.device_id].turn_on()
        
    def get_speaker(self, device_id: str):
        return self.speakers.get(device_id, None)
    
    async def send_audio(self, audio_data: bytes):
        """Send audio data to the Speaker WebSocket."""
        if not self.websocket or self.websocket.close_code is not None:
            await self.connect_speaker()
            
        # Write speech processing logic here
        # ==================================================================================
        # Transform raw PCM audio bytes into a WAV file-like object
        wav_bytes = self.raw_bytes_to_wav(audio_data)
        
        if self.validate_wav(wav_bytes):
            logger.debug(f"Converted {len(audio_data)} bytes to WAV")
        else:
            logger.error(f"Invalid audio data. Skipping...")
            return
        
        wav_file = NamedBytesIO(wav_bytes.getvalue(), name="audio.wav")
        
        transcript = self.speech_to_text(wav_file)
        logger.info(f"Transcript: {transcript}")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            assistant_response = await client.post(self.assistant_server_url, json={"message": transcript})
            assistant_response = assistant_response.json()
            logger.debug(f"Response Schema: {assistant_response.keys()}")
            logger.info(f"Assistant Response: {assistant_response['content']}")
            response_bytes = base64.b64decode(assistant_response["audio"])
        
        # ==================================================================================
        # Sends the audio data to the speaker through the WebSocket
        if self.websocket:
            try:
                await self.websocket.send(response_bytes)
                logger.info(f"Sent {len(response_bytes)} bytes to Speaker WebSocket")
            except websockets.exceptions.ConnectionClosed:
                logger.error(f"Speaker WebSocket closed unexpectedly. Reconnecting...")
                self.websocket = None
            except Exception as e:
                traceback.print_exc()
                logger.error(f"Error sending audio to speaker: {e}")
                
            return assistant_response["content"]
                
    def get_status(self):
        return {
            'device_id': self.device_id,
            'state': self._state,
        }