from abc import ABC, abstractmethod
from typing import List

class Command:
    # Assuming Command is a predefined class
    pass

class LIGHT:
    # Assuming LIGHT is a predefined class
    pass


class LightGateway(ABC):
    def __init__(self, light_state: bool, temp: float):
        self.light_state = light_state
        self.temp = temp

    @abstractmethod
    def receive_command(self, command: Command) -> None:
        pass

    @abstractmethod
    def manage_light(self, command: Command) -> None:
        pass

    @abstractmethod
    def adjust_temp_for_all(self, level: float) -> None:
        pass

    @abstractmethod
    def turn_off(self, id: int) -> None:
        pass

    @abstractmethod
    def turn_on(self, id: int) -> None:
        pass

    @abstractmethod
    def get_light_status(self) -> List[bool]:
        pass

    @abstractmethod
    def get_light_by_id(self, id: int) -> LIGHT:
        pass