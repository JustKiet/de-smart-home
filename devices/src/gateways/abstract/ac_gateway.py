from abc import ABC, abstractmethod
from typing import List

class Command:
    # Assuming Command is a predefined class
    pass

class AC:
    # Assuming AC is a predefined class
    pass

class ACGateway(ABC):
    def __init__(self, ac_state: bool, temp: float):
        self.ac_state = ac_state
        self.temp = temp

    @abstractmethod
    def receive_command(self, command: Command) -> None:
        pass

    @abstractmethod
    def manage_ac(self, command: Command) -> None:
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
    def get_ac_status(self) -> List[bool]:
        pass

    @abstractmethod
    def get_ac_by_id(self, id: int) -> AC:
        pass