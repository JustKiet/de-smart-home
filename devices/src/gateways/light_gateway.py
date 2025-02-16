
from typing import List, Union
from devices.src.smart_devices.interfaces.control_light import ControlLight
from devices.src.gateways.interfaces.common.control_gateway import ControlGateway
from devices.src.smart_devices.interfaces.common.device_status import DeviceStatus
from devices.src.smart_devices.interfaces.common.control_power import ControlPower

# TODO: Rework this class. Only import the interface, not the implementation.
class LightGateway:
    def __init__(self, light_devices: List[ControlLight]):
        self.light_devices = {light_device.device_id: light_device for light_device in light_devices}
    
    # Kiet: These logging methods should be merged into one method.
    # def log_light_status(self):
    #     for light_id, light_device in self.light_devices.items():
    #         print(f"Light {light_id}: {light_device.device_id} is {light_device.state}")
    #         
    # def log_light_status(self, id: Union[int]):
    #     light_id = 'light_' + str(id)
    #     if light_id in self.light_devices:
    #         print(f"Light {light_id}: {self.light_devices[light_id].device_id} is {self.light_devices[light_id].state}")
    #     return None
    #         
    # def log_light_brightness(self):
    #     for light_id, light_device in self.light_devices.items():
    #         print(f"Light {light_id}: {light_device.light_id} has brightness {light_device.brightness}")
    #         
    # def log_light_brightness(self, id: Union[int]):
    #     light_id = 'light_' + str(id)
    #     if light_id in self.light_devices:
    #         print(f"Light {light_id}: {self.light_devices[light_id].device_id} has brightness {self.light_devices[light_id].brightness}")
    #     return None
    #         
    # def log_light_temperature(self):
    #     for light_id, light_device in self.light_devices.items():
    #         print(f"Light {light_id}: {light_device.light_id} has temperature {light_device.light.temperature}K")
    #         
    # def log_light_temperature(self, id: Union[int]):
    #     light_id = 'light_' + str(id)
    #     if light_id in self.light_devices:
    #         print(f"Light {light_id}: {self.light_devices[light_id].device_id} has temperature {self.light_devices[light_id].temperature}K")
    #     return None
    
    def log_light_status(self, id: Union[int, List[int]] = None):
        if id:
            if isinstance(id, int):
                light_id = 'light_' + str(id)
                if light_id in self.light_devices:
                    light_status = self.light_devices[light_id].get_status()
                    # Implement logging logic here.
                    print(light_status)
                    return light_status
            elif isinstance(id, list):
                events = []
                for light_id in id:
                    light_id = 'light_' + str(light_id)
                    if light_id in self.light_devices:
                        # Implement logging logic here.
                        light_status = self.light_devices[light_id].get_status()
                        events.append(light_status)
                        print(light_status)
                return events
        else:
            events = []
            for _, light_device in self.light_devices.items():
                # Implement logging logic here.
                light_status = light_device.get_status()
                print(light_status)
                events.append(light_status)
            return events
            
    def turn_on_by_id(self, id: Union[int, List[int]]):
        if isinstance(id, int):
            light_id = 'light_' + str(id)
            if light_id in self.light_devices:
                self.light_devices[light_id].turn_on(light_id)
                event = self.log_light_status(id)
                return event
        elif isinstance(id, list):
            events = []
            for light_id in id:
                light_id = 'light_' + str(light_id)
                if light_id in self.light_devices:
                    self.light_devices[light_id].turn_on(light_id)
                    event = self.log_light_status(id)
                    events.append(event)
            return events
    
    def turn_off_by_id(self, id: Union[int, List[int]]):
        if isinstance(id, int):
            light_id = 'light_' + str(id)
            if light_id in self.light_devices:
                self.light_devices[light_id].turn_off(light_id)
                event = self.log_light_status(id)
                return event
        elif isinstance(id, list):
            events = []
            for light_id in id:
                light_id = 'light_' + str(light_id)
                if light_id in self.light_devices:
                    self.light_devices[light_id].turn_off(light_id)
                    event = self.log_light_status(id)
                    events.append(event)
            return events
    
    def set_brightness_by_id(self, id: Union[int, List[int]], level: int):
        if isinstance(id, int):
            light_id = 'light_' + str(id)
            if light_id in self.light_devices:
                self.light_devices[light_id].set_brightness(light_id, level)
                event = self.log_light_brightness(id)
                return event
        elif isinstance(id, list):
            events = []
            for light_id in id:
                light_id = 'light_' + str(light_id)
                if light_id in self.light_devices:
                    self.light_devices[light_id].set_brightness(light_id, level)
                    event = self.log_light_status(id)
                    events.append(event)
            return events
    
    def set_light_temperature_by_id(self, id: Union[int, List[int]], temperature: float):
        if isinstance(id, int):
            light_id = 'light_' + str(id)
            if light_id in self.light_devices:
                self.light_devices[light_id].set_light_temperature(light_id, temperature)
                event = self.log_light_status(id)
                return event
        elif isinstance(id, list):
            events = []
            for light_id in id:
                light_id = 'light_' + str(light_id)
                if light_id in self.light_devices:
                    self.light_devices[light_id].set_light_temperature(light_id, temperature)
                    event = self.log_light_status(id)
            return events
    
    def turn_on_all(self):
        events = []
        for light_id, light_device in self.light_devices.items():
            light_device.turn_on(light_id)
        event = self.log_light_status()
        events.append(event)
        return events
    
    def turn_off_all(self):
        events = []
        for light_id, light_device in self.light_devices.items():
            light_device.turn_off(light_id)
        event = self.log_light_status()
        event.append(event)
        return events