from abc import ABC, abstractmethod

class AC(ABC):
    def __init__(self, id: int, temp: int, status: bool, humidity: float, fan_speed: int):
        self.id = id
        self.temp = temp
        self.status = status
        self.humidity = humidity
        self.fan_speed = fan_speed

    @abstractmethod
    def turn_on(self) -> None:
        pass

    @abstractmethod
    def turn_off(self) -> None:
        pass

    @abstractmethod
    def adjust_temp(self, level: int) -> None:
        pass

    @abstractmethod
    def set_humidity(self, humidity: float) -> None:
        pass

    @abstractmethod
    def set_fan_speed(self, fan_speed: int) -> None:
        pass

    @abstractmethod
    def get_status(self) -> bool:
        pass

    @abstractmethod
    def get_temp(self) -> int:
        pass

    @abstractmethod
    def get_humidity(self) -> float:
        pass