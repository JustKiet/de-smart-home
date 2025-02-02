from abc import ABC, abstractmethod
from typing import List

class Device:
    # Assuming Device is a predefined class
    pass

class LightManager:
    # Assuming LightManager is a predefined class
    pass

class ACManager:
    # Assuming ACManager is a predefined class
    pass


class CameraManager:
    # Assuming CameraManager is a predefined class
    pass

class SmartManager(ABC):
    """Abstract class for smart device manager"""
    def __init__(self, device_list: List[Device]):
        self.device_list = device_list

    @abstractmethod
    def add_device(self, device: Device) -> None:
        pass

    @abstractmethod
    def remove_device(self, device: Device) -> None:
        pass

    @abstractmethod
    def send_command(self, light_manager: LightManager, ac_manager: ACManager, camera_manager: CameraManager, command: str) -> None:
        light_manager.execute_command(command)
        ac_manager.execute_command(command)
        camera_manager.execute_command(command)
        pass
    
    