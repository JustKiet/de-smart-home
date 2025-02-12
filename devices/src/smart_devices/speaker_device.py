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

class SpeakerDevice(ControlSpeaker):
    def __init__(self, device_id: str):
        super().__init__()
        self._state = 'off'
        self._volume = 0
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
        self._volume = value
        return self.get_status()
    
    def mute(self):
        self._muted = True
        return self.get_status()
    
    def unmute(self):
        self._muted = False
        return self.get_status()

    def play_audio(self, audio_data):
        """Play audio using PyAudio instead of SoundDevice."""
        logger.info(f"Playing {len(audio_data)} bytes")  # ✅ Debug output
        
        try:
            # Convert bytes to NumPy array (16-bit PCM)
            audio_array = np.frombuffer(audio_data, dtype=np.int16) # Convert to float32 for resampling
            
            # Write the audio to the stream
            self.stream.write(audio_array.tobytes())  # Ensure it's in byte format

            logger.debug("Playback finished.")  # ✅ Log success

        except Exception as e:
            logger.error(f"SpeakerDevice: Error playing audio: {e}")  # ✅ Log error
    
    def play_from_url(self, url: str):
        if self._state == 'off':
            return {
                'device_id': self.device_id,
                'error': 'Speaker is off. Please turn it on first.'
            }
        
        self._audio_status = 'playing'
        self._pause_event.set()
        
        def play():
            try:
                response = requests.get(url, stream=True)
                if not response.ok:
                    return {
                        'device_id': self.device_id,
                        'error': f"Error streaming audio: {response.reason}"
                    }
                p = pyaudio.PyAudio()
                stream = p.open(
                    format=pyaudio.paInt16, 
                    channels=1, 
                    rate=16000, 
                    output=True
                )
                
                for chunk in response.iter_content(chunk_size=1024):
                    if self._audio_status != 'playing' or self._state == 'off':
                        break
                    self._pause_event.wait()
                    if not self._muted:
                        stream.write(chunk)
                
                stream.stop_stream()
                stream.close()
                p.terminate()
                
            except Exception as e:
                print(f"Error streaming audio: {e}")
            
            finally:
                self._audio_status = 'stopped'
        
        self._thread = threading.Thread(target=play)
        self._thread.start()
        return {"status": "Playing from URL"}
            
    def stop_audio(self):
        """Stop audio from the speaker."""
        self._audio_status = 'stopped'
        self._pause_event.set()
        self._streaming = False
        return self.get_status()
    
    def pause_audio(self):
        if self._audio_status == 'playing':
            self._audio_status = 'paused'
            self._pause_event.clear()
        return self.get_status()
    
    def resume_audio(self):
        if self._audio_status == 'paused':
            self._audio_status = 'playing'
            self._pause_event.set()
        return self.get_status()
    
    def get_status(self):
        """Get the current status of the speaker."""
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