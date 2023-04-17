from abc import ABC, abstractmethod


class Signal(ABC):
    """An abstract base class for trade signals."""

    @abstractmethod
    def getSignal(self):
        """Get trade signal."""
        NotImplementedError()
