from abc import ABC, abstractmethod


class Signal(ABC):
    """An abstract base class for trade signals."""

    def __init__(self, **kwargs) -> None:
        super(Signal, self).__init__()


    @abstractmethod
    def getSignal(self):
        """Get trade signal."""
        raise NotImplementedError
