from abc import ABC, abstractmethod

class Light(ABC):
    """Abstract class for light devices"""
    def __init__(self, id: int, brightness: int, status: bool, color_temperature: int):
        self.id = id
        self.brightness = brightness
        self.status = status
        self.color_temperature = color_temperature

    @abstractmethod
    def turn_on(self) -> None:
        pass

    @abstractmethod
    def turn_off(self) -> None:
        pass

    @abstractmethod
    def adjust_brightness(self, level: int) -> None:
        pass

    @abstractmethod
    def set_color_temperature(self, temp: int) -> None:
        pass

    @abstractmethod
    def get_status(self) -> bool:
        pass

    @abstractmethod
    def get_brightness(self) -> int:
        pass

    @abstractmethod
    def get_color_temperature(self) -> int:
        pass