from abc import ABC, abstractmethod
from devices.src.smart_devices.interfaces.common.control_power import ControlPower
from devices.src.smart_devices.interfaces.common.device_status import DeviceStatus

class ControlSpeaker(ControlPower,
                     DeviceStatus):
    """An interface for controlling speaker devices.
    
    Methods:
    - `set_volume` -- Set the volume of the speaker.
    - `control_bass` -- Control the bass of the speaker.
    - `control_treble` -- Control the treble of the speaker.
    - `mute` -- Mute the speaker.
    - `unmute` -- Unmute the speaker.
    - `play_audio` -- Play audio from the speaker.
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
    def play_audio(self):
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