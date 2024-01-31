from abc import ABC, abstractmethod

class IHandler(ABC):
    @abstractmethod
    def execute_handler(self):
        pass