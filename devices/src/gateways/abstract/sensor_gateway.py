from abc import ABC, abstractmethod

from .base_gateway import BaseGateway 

class SensorGateway(BaseGateway):
    """Abtsract class for sensor devices"""

    @abstractmethod
    def read_sensor_data(self):
        """Read sensor data"""
        pass
