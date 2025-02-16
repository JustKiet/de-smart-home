from abc import ABC, abstractmethod

from devices.src.smart_devices.interfaces.common.control_power import ControlPower
from devices.src.smart_devices.interfaces.common.device_status import DeviceStatus

class ControlSensor(ControlPower,
                    DeviceStatus):
    """Abtsract class for sensor devices"""
    
    @abstractmethod
    def connect(self):
        """Connect to the sensor"""
        pass
    
    @abstractmethod
    def disconnect(self):
        """Disconnect from the sensor"""
        pass
    
    @abstractmethod
    def send_sensor_data(self, data):
        """Send sensor data"""
        pass

    @abstractmethod
    def read_sensor_data(self):
        """Read sensor data"""
        pass
    
    @abstractmethod
    def get_sensor_data(self):
        """Get sensor data"""
        pass
    
    @abstractmethod
    def set_sensor_data(self, data):
        """Set sensor data"""
        pass
