from abc import ABC, abstractmethod


class Indicator(ABC):
    """An abstract base class for any indicator."""

    @abstractmethod
    def getValue(self):
        """Get value of indicator."""
        NotImplementedError()
