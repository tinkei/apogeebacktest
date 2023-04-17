from abc import ABC, abstractmethod

class Strategy(ABC):
    """An abstract base class for strategy."""

    @abstractmethod
    def evalStrategy(self):
        pass
