from abc import ABC, abstractmethod

class ManageAirConditioner(ABC):
    """Abstract class for managing AC devices"""
    
    @abstractmethod
    def get_device(self):
        """Get the device"""
        raise NotImplementedError
    
    @abstractmethod
    def get_all_devices(self):
        """Get all devices"""
        raise NotImplementedError
    
    @abstractmethod
    def log_ac_status(self):
        """Log the status of the AC"""
        raise NotImplementedError
    
    @abstractmethod
    def log_ac_status_by_id(self):
        """Log the status of the AC by ID"""
        raise NotImplementedError
    
    @abstractmethod
    def turn_on_by_id(self):
        """Turn on the AC by ID"""
        raise NotImplementedError
    
    @abstractmethod
    def turn_off_by_id(self):
        """Turn off the AC by ID"""
        raise NotImplementedError
    
    @abstractmethod
    def set_temperature_by_id(self):
        """Set the temperature of the AC by ID"""
        raise NotImplementedError
    
    @abstractmethod
    def set_fan_speed_by_id(self):
        """Set the fan speed of the AC by ID"""
        raise NotImplementedError
    
    @abstractmethod
    def set_humidity_by_id(self):
        """Set the humidity of the AC by ID"""
        raise NotImplementedError
    
    @abstractmethod
    def set_mode_by_id(self):
        """Set the mode of the AC by ID"""
        raise NotImplementedError
    
    @abstractmethod
    def set_temperature_for_all(self):
        """Set the temperature for all ACs"""
        raise NotImplementedError
    
    @abstractmethod
    def set_fan_speed_for_all(self):
        """Set the fan speed for all ACs"""
        raise NotImplementedError
    
    @abstractmethod
    def set_humidity_for_all(self):
        """Set the humidity for all ACs"""
        raise NotImplementedError
    
    @abstractmethod
    def turn_on_all(self):
        """Turn on all ACs"""
        raise NotImplementedError
    
    @abstractmethod
    def turn_off_all(self):
        """Turn off all ACs"""
        raise NotImplementedError
        
    @abstractmethod
    def get_ac_status(self):
        """Get the status of all ACs"""
        raise NotImplementedError
    
    @abstractmethod
    def get_status_by_id(self):
        """Get the status of the AC by ID"""
        raise NotImplementedError
