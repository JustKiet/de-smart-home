from abc import ABC, abstractmethod

class Authenticate(ABC):
    """An interface for authenticating devices.

    Methods:
    - `authenticate` -- Authenticate the device.
    """
    @abstractmethod
    def authenticate(self):
        raise NotImplementedError