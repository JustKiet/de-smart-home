from abc import abstractmethod
from devices.src.gateways.interfaces.common.device_status import DeviceStatus
from devices.src.gateways.interfaces.common.control_power import ControlPower
class ControlSpeaker(ControlPower, DeviceStatus):
    """An interface for controlling speaker devices.
    
    Methods:
    - `turn_on` -- Turn on the speaker.
    - `turn_off` -- Turn off the speaker.
    - `get_status` -- Get the status of the speaker.
    - `set_volume` -- Set the volume of the speaker.
    - `mute` -- Mute the speaker.
    - `unmute` -- Unmute the speaker.
    - `play_from_file` -- Play audio from a file.
    - `play_from_url` -- Play audio from a URL.
    - `play_audio_bytes` -- Play audio bytes from the speaker.
    - `stop_audio` -- Stop audio from the speaker.
    - `pause_audio` -- Pause audio from the speaker.
    - `resume_audio` -- Resume audio from the speaker.
    - `get_audio` -- Get the audio from the speaker.
    """
    @abstractmethod
    def set_volume(self):
        raise NotImplementedError
    
    @abstractmethod
    def mute(self):
        raise NotImplementedError
    
    @abstractmethod
    def unmute(self):
        raise NotImplementedError
    
    @abstractmethod
    async def play_audio(self):
        raise NotImplementedError
    
    @abstractmethod
    def stop_audio(self):
        raise NotImplementedError
    
    @abstractmethod
    def pause_audio(self):
        raise NotImplementedError
    
    @abstractmethod
    def resume_audio(self):
        raise NotImplementedError