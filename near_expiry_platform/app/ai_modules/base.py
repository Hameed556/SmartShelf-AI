from abc import ABC, abstractmethod

class AIModule(ABC):
    @abstractmethod
    def run(self, *args, **kwargs):
        pass 