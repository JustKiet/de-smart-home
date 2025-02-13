from devices.src.smart_devices.interfaces.control_speaker import ControlSpeaker
import pyaudio
import wave
import requests
import threading
from fastapi import FastAPI, WebSocket
from typing import Literal
import sounddevice as sd
import numpy as np
from loguru import logger
import librosa
import time
class SpeakerDevice(ControlSpeaker):
    def __init__(self, device_id: str):
        super().__init__()
        self._state = 'off'
        self._volume = 1.0
        self._muted = False
        self.device_id = f"speaker_{device_id}"
        self._audio_status: Literal['playing', 'paused', 'stopped'] = 'stopped'
        self._pause_event = threading.Event()
        self._pause_event.set()
        self._thread = None
        self._streaming = False
        
        self._chunk_size = 4096
        self.sample_rate = 16000
        self._channels = 1
        self._format = pyaudio.paInt16
        
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=self._format,
            channels=self._channels,
            rate=self.sample_rate,
            output=True,
            frames_per_buffer=self._chunk_size
        )
        
    def is_turned_on(self):
        if self._state == 'on':
            return True
        else:
            raise Exception(f"{self.device_id} | Speaker is turned off. Please turn the device on first.")
        
    def turn_on(self):
        self._state = 'on'
        return self.get_status()
        
    def turn_off(self):
        self._state = 'off'
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        return self.get_status()
    
    def set_volume(self, value: int):
        self.is_turned_on()
        self._volume = value
        return self.get_status()
    
    def mute(self):
        self.is_turned_on()
        self._muted = True
        return self.get_status()
    
    def unmute(self):
        self.is_turned_on()
        self._muted = False
        return self.get_status()

    def play_audio(self, audio_data):
        """Play audio using PyAudio with support for pause and mute."""
        self.is_turned_on()
        
        if self._audio_status == 'playing':
            logger.warning("Already playing audio.")
            return

        self._audio_status = 'playing'
        self._pause_event.set()

        def playback():
            logger.info(f"Playing {len(audio_data)} bytes")  # ✅ Debug output
            
            try:
                # Convert bytes to NumPy array (16-bit PCM)
                audio_array = np.frombuffer(audio_data, dtype=np.int16)

                # Apply volume scaling (if volume is between 0-1)
                if not self._muted:
                    scaled_audio = (audio_array * self._volume).astype(np.int16)
                else:
                    scaled_audio = np.zeros_like(audio_array)  # Mute by setting all samples to 0

                # Split the audio into chunks
                for i in range(0, len(scaled_audio), self._chunk_size):
                    while self._audio_status == 'paused':
                        self._pause_event.wait()  # Wait until resumed
                    
                    if self._audio_status == 'stopped':
                        logger.info("Audio playback stopped.")
                        return

                    chunk = scaled_audio[i:i + self._chunk_size].tobytes()
                    self.stream.write(chunk)  # Play the audio chunk

                logger.debug("Playback finished.")  # ✅ Log success
                self._audio_status = 'stopped'

            except Exception as e:
                logger.error(f"SpeakerDevice: Error playing audio: {e}")

        self._thread = threading.Thread(target=playback)
        self._thread.start()

            
    def stop_audio(self):
        """Stop audio from the speaker."""
        self.is_turned_on()
        
        self._audio_status = 'stopped'
        self._pause_event.set()
        self._streaming = False
        return self.get_status()
    
    def pause_audio(self):
        self.is_turned_on()
        
        if self._audio_status == 'playing':
            self._audio_status = 'paused'
            self._pause_event.clear()
        return self.get_status()
    
    def resume_audio(self):
        self.is_turned_on()
        
        if self._audio_status == 'paused':
            self._audio_status = 'playing'
            self._pause_event.set()
        return self.get_status()
    
    def get_status(self):
        """Get the current status of the speaker."""
        self.is_turned_on()
        
        return {
            'device_id': self.device_id,
            'device_power': self._state,
            'muted': self._muted,
            'volume': self._volume,
            'audio_status': self._audio_status,
            'streaming': self._streaming
        }
        
if __name__ == "__main__":
    from openai import OpenAI
    from dotenv import load_dotenv
    
    load_dotenv()
    
    client = OpenAI()
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input="Today is a wonderful day to build something people love!",
        response_format="wav"
    )
    
    print(type(response.content))
    
    speaker = SpeakerDevice("1")
    speaker.play_audio(response.content)