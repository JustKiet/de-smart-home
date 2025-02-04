from abc import ABC, abstractmethod

class BaseControl(ABC):
    """Abstract class for gateway devices"""

    @abstractmethod
    def turn_on(self):
        """Turn on the device"""
        pass
    
    @abstractmethod
    def turn_off(self):
        """Turn off the device"""
        pass
    

    @abstractmethod
    def connect(self):
        """Connect to the device"""
        pass

    @abstractmethod
    def disconnect(self):
        """Disconnect from the device"""
        pass

    @abstractmethod
    def send_data(self, data):
        """Send data to the device"""
        pass

    @abstractmethod
    def receive_data(self):
        """Receive data from the device"""
        pass
