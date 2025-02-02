from abc import ABC, abstractmethod
from typing import List

class Block:
    """A class to represent a block in a blockchain."""
    # Assuming Block is a predefined class
    pass

class Blockchain(ABC):
    """Abstract class for blockchain data structure."""
    
    def __init__(self, blockchain_data: List[Block]):
        self.blockchain_data = blockchain_data

    @abstractmethod
    def add_block(self, block: Block) -> None:
        """Add a block to the blockchain."""    
        pass

    @abstractmethod
    def validate_chain(self) -> bool:
        """Validate the blockchain."""
        pass