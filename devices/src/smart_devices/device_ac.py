from devices.src.smart_devices.interfaces.control_ac import ControlAirConditioner
from typing import Literal

class ACDevice(ControlAirConditioner):
    def __init__(self, device_id):
        self.device_id: str = "ac_" + str(device_id)
        self.state: Literal["on", "off"] = "off"
        self.temperature = 24
        self.fan_speed = 1
        self.humidity = 50
        self.mode: Literal["cool", "heat", "dry", "fan", "auto"] = "auto"
        
    def turn_on(self):
        self.state = "on"
        print(f"Air conditioner {self.device_id} turned on")
    
    def turn_off(self):
        self.state = "off"
        print(f"Air conditioner {self.device_id} turned off")
    
    def set_temperature(self, device_id: int, level: float):
        self.temperature = level
        print(f"Temperature of air conditioner {self.device_id} set to {self.temperature}°C")

    def get_temperature(self, device_id: int) -> float:
        return self.temperature
    
    def set_fan_speed(self, device_id: int, level: int):
        self.fan_speed = level
        print(f"Fan speed of air conditioner {self.device_id} set to {self.fan_speed}")
        
    def get_fan_speed(self, device_id: int) -> int:
        return self.fan_speed
    
    def set_humidity(self, device_id: int, level: int):
        self.humidity = level
        print(f"Humidity of air conditioner {self.device_id} set to {self.humidity}%")
        
    def get_humidity(self, device_id: int) -> int:
        return self.humidity
    
    def set_mode(self, device_id: int, mode: str):
        self.mode = mode
        print(f"Mode of air conditioner {self.device_id} set to {self.mode}")
        
    def get_mode(self, device_id: int) -> str:
        return self.mode