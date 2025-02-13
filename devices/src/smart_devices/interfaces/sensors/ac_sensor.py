from abc import ABC, abstractmethod

class ACSensor(ABC):
    def __init__(self, id: int, value: float):
        self.id = id
        self.value = value

    @abstractmethod
    def read_humidity_level(self) -> float:
        pass

    @abstractmethod
    def get_value(self) -> float:
        pass