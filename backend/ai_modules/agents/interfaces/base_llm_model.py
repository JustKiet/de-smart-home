from abc import ABC, abstractmethod

class BaseLLMModel(ABC):
    @abstractmethod
    def define_system_message(self):
        raise NotImplementedError
    
    @abstractmethod
    def model_generate(self):
        raise NotImplementedError
    