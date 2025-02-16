from abc import ABC, abstractmethod
from typing import List, Union

# Kiet: Remember to only import the interface, not the implementation.
from devices.src.smart_devices.interfaces.control_ac import ControlAirConditioner
from devices.src.gateways.interfaces.manage_ac import ManageAirConditioner
from devices.src.gateways.interfaces.common.control_gateway import ControlGateway

# TODO: Rework this class.
class ACGateway(ControlGateway,
                ManageAirConditioner):
    def __init__(self, ac_devices: List[ControlAirConditioner]):
        self.ac_devices = {ac_devices.device_id: ac_devices for ac_devices in ac_devices} 
        
    def get_device(self, device_id: str) -> Union[ControlAirConditioner, None]:
        return self.ac_devices.get(device_id)
    
    def get_all_devices(self) -> List[ControlAirConditioner]:
        return list(self.ac_devices.values())
    
    def log_all_ac_status(self):
        for ac_id, ac_device in self.ac_devices.items():
            print(f"AC: {ac_id}: {ac_device.device_id} is {ac_device.state}")
            
    def log_ac_status_by_id(self, id: Union[int]):
        ac_id = 'ac_' + str(id)
        if ac_id in self.ac_devices:
            print(f"AC: {ac_id}: {self.ac_devices[ac_id].device_id} is {self.ac_devices[ac_id].state}")
        return None
    
    # Kiet: This is not needed.
    
    #def log_ac_temperature(self):
    #    for ac_id, ac_device in self.ac_devices.items():
    #        print(f"AC: {ac_id}: {ac_device.device_id} has temperature {ac_device.temperature}°C")
    #        
    #def log_ac_temperature(self, id: Union[int]):
    #    ac_id = 'ac_' + str(id)
    #    if ac_id in self.ac_devices:
    #        print(f"AC: {ac_id}: {self.ac_devices[ac_id].device_id} has temperature {self.ac_devices[ac_id].temperature}°C")
    #    return None
    #
    #def log_ac_fan_speed(self):
    #    for ac_id, ac_device in self.ac_devices.items():
    #        print(f"AC: {ac_id}: {ac_device.device_id} has fan speed {ac_device.fan_speed}")
    #        
    #def log_ac_fan_speed(self, id: Union[int]):
    #    ac_id = 'ac_' + str(id)
    #    if ac_id in self.ac_devices:
    #        print(f"AC: {ac_id}: {self.ac_devices[ac_id].device_id} has fan speed {self.ac_devices[ac_id].fan_speed}")
    #    return None
    #
    #def log_ac_humidity(self):
    #    for ac_id, ac_device in self.ac_devices.items():
    #        print(f"AC: {ac_id}: {ac_device.device_id} has humidity {ac_device.humidity}%")
    #        
    #def log_ac_humidity(self, id: Union[int]):
    #    ac_id = 'ac_' + str(id)
    #    if ac_id in self.ac_devices:
    #        print(f"AC: {ac_id}: {self.ac_devices[ac_id].device_id} has humidity {self.ac_devices[ac_id].humidity}%")
    #    return None
    
    def turn_on_by_id(self, id: Union[int]):
        ac_id = 'ac_' + str(id)
        if ac_id in self.ac_devices:
            self.ac_devices[ac_id].turn_on()
            self.log_ac_status(id)
        return None
    
    def turn_off_by_id(self, id: Union[int]):
        ac_id = 'ac_' + str(id)
        if ac_id in self.ac_devices:
            self.ac_devices[ac_id].turn_off()
            self.log_ac_status(id)
        return None
    
    def set_temperature_by_id(self, id: Union[int], level: float):
        ac_id = 'ac_' + str(id)
        if ac_id in self.ac_devices:
            self.ac_devices[ac_id].set_temperature(id, level)
            self.log_ac_temperature(id)
        return None
    
    def set_fan_speed_by_id(self, id: Union[int], level: int):
        ac_id = 'ac_' + str(id)
        if ac_id in self.ac_devices:
            self.ac_devices[ac_id].set_fan_speed(id, level)
            self.log_ac_fan_speed(id)
        return None
    
    def set_humidity_by_id(self, id: Union[int], level: int):
        ac_id = 'ac_' + str(id)
        if ac_id in self.ac_devices:
            self.ac_devices[ac_id].set_humidity(id, level)
            self.log_ac_humidity(id)
        return None
    
    def set_mode_by_id(self, id: Union[int], mode: str):
        ac_id = 'ac_' + str(id)
        if ac_id in self.ac_devices:
            self.ac_devices[ac_id].set_mode(id, mode)
        return None
    
    def get_status_by_id(self) -> List[bool]:
        return [ac.state == "on" for ac in self.ac_devices.values()]
    
    def set_temp_for_all(self, level: float):
        for ac_device in self.ac_devices.values():
            ac_device.set_temperature(level)
        return None
    
    def turn_on_all(self):
        for ac_device in self.ac_devices.values():
            ac_device.turn_on()
        return None
    
    def turn_off_all(self):
        for ac_device in self.ac_devices.values():
            ac_device.turn_off()
        return None