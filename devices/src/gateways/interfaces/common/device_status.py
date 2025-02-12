from abc import ABC, abstractmethod

class DeviceStatus(ABC):
    """A common device status interface for all devices.

    Methods:
    - `get_status` -- Get the status of the device.
    """
    @abstractmethod
    def get_status(self):
        raise NotImplementedError