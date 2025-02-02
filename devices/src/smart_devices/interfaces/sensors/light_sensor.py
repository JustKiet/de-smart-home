from abc import ABC, abstractmethod

class LightSensor(ABC):
    """Abstract class for light sensor devices"""
    def __init__(self, id: int, value: float):
        self.id = id
        self.value = value

    @abstractmethod
    def read_light_level(self) -> float:
        pass

    @abstractmethod
    def get_value(self) -> float:
        pass