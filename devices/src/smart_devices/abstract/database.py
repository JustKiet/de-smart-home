from abc import ABC, abstractmethod
from typing import List

class Record:
    # Assuming Record is a predefined class
    pass

class Query:
    # Assuming Query is a predefined class
    pass

class Database(ABC):
    """Abstract class for database connection."""
    def __init__(self, data: List[Record]):
        self.data = data
        
    @abstractmethod
    def connect(self) -> None:
        pass
    
    @abstractmethod
    def disconnect(self) -> None:
        pass

    @abstractmethod
    def store_data(self, record: Record) -> None:
        pass

    @abstractmethod
    def retrieve_data(self, query: Query) -> List[Record]:
        pass