from abc import ABC, abstractmethod

class ControlPower(ABC):
    """A common power control interface for all devices.

    Methods:
    - `turn_on` -- Turn on the device.
    - `turn_off` -- Turn off the device
    """
    @abstractmethod
    def is_turned_on(self):
        raise NotImplementedError
    
    @abstractmethod
    def turn_on(self):
        raise NotImplementedError
    
    @abstractmethod
    def turn_off(self):
        raise NotImplementedError