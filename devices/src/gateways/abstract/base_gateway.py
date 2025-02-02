from abc import ABC, abstractmethod

class BaseGateway(ABC):
    """Abstract class for gateway devices"""

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
