from abc import ABC, abstractmethod

class BaseDevice(ABC):
    """abstract class for smart devices"""

    @abstractmethod
    def power_on(self):
        """Power on the device"""
        pass

    @abstractmethod
    def power_off(self):
        """Power off the device"""
        pass

    @abstractmethod
    def get_status(self):
        """Get the status of the device"""
        pass
