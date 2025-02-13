
from typing import List, Union
from devices.src.smart_devices.device_light import LightDevice

class LightGateway:
    def __init__(self, light_devices: List[LightDevice]):
        self.light_devices = {light_device.device_id: light_device for light_device in light_devices}
        
    def log_light_status(self):
        for light_id, light_device in self.light_devices.items():
            print(f"Light {light_id}: {light_device.device_id} is {light_device.state}")
            
    def log_light_status(self, id: Union[int]):
        light_id = 'light_' + str(id)
        if light_id in self.light_devices:
            print(f"Light {light_id}: {self.light_devices[light_id].device_id} is {self.light_devices[light_id].state}")
        return None
            
    def log_light_brightness(self):
        for light_id, light_device in self.light_devices.items():
            print(f"Light {light_id}: {light_device.light_id} has brightness {light_device.brightness}")
            
    def log_light_brightness(self, id: Union[int]):
        light_id = 'light_' + str(id)
        if light_id in self.light_devices:
            print(f"Light {light_id}: {self.light_devices[light_id].device_id} has brightness {self.light_devices[light_id].brightness}")
        return None
            
    def log_light_temperature(self):
        for light_id, light_device in self.light_devices.items():
            print(f"Light {light_id}: {light_device.light_id} has temperature {light_device.light.temperature}K")
            
    def log_light_temperature(self, id: Union[int]):
        light_id = 'light_' + str(id)
        if light_id in self.light_devices:
            print(f"Light {light_id}: {self.light_devices[light_id].device_id} has temperature {self.light_devices[light_id].temperature}K")
        return None
        
    def turn_on_by_id(self, id: Union[int]):
        light_id = 'light_' + str(id)
        if light_id in self.light_devices:
            self.light_devices[light_id].turn_on(light_id)
            self.log_light_status(id)
        return None
    
    def turn_off_by_id(self, id: Union[int]):
        light_id = 'light_' + str(id)
        if light_id in self.light_devices:
            self.light_devices[light_id].turn_off(light_id)
            self.log_light_status(id)
        return None
    
    def set_brightness_by_id(self, id: Union[int], level: int):
        light_id = 'light_' + str(id)
        if light_id in self.light_devices:
            self.light_devices[light_id].set_brightness(light_id, level)
            self.log_light_brightness(id)
        return None
    
    def get_brightness_by_id(self, id: Union[int]) -> int:
        light_id = 'light_' + str(id)
        if light_id in self.light_devices:
            return self.light_devices[light_id].get_brightness(light_id)
        return 0
    
    def set_light_temperature_by_id(self, id: Union[int], temperature: float):
        light_id = 'light_' + str(id)
        if light_id in self.light_devices:
            self.light_devices[light_id].set_light_temperature(light_id, temperature)
            self.log_light_temperature(id)
        return None
    
    def get_light_temperature_by_id(self, id: Union[int]) -> float:
        light_id = 'light_' + str(id)
        if light_id in self.light_devices:
            return self.light_devices[light_id].get_light_temperature(light_id)
        return 0.0 # 0.0K is absolute zero
    
    def turn_on_all(self):
        for light_id, light_device in self.light_devices.items():
            light_device.turn_on(light_id)
        self.log_light_status()
        return None
    
    def turn_off_all(self):
        for light_id, light_device in self.light_devices.items():
            light_device.turn_off(light_id)
        self.log_light_status()
        return None