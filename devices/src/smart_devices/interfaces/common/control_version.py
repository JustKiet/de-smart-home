from abc import ABC, abstractmethod

class ControlVersion(ABC):
    """A common update service interface for all devices.

    Methods:
    - `update` -- A method that updates the device.
    - `get_info` -- A method that returns the device's information.
    """
    @abstractmethod
    def update(self):
        raise NotImplementedError
    
    @abstractmethod
    def get_info(self):
        raise NotImplementedError