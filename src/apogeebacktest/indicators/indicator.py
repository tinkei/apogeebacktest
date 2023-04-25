from abc import ABC, abstractmethod


class Indicator(ABC):
    """An abstract base class for any indicator."""

    def __init__(self, **kwargs) -> None:
        super(Indicator, self).__init__()


    @abstractmethod
    def getValue(self):
        """Get value of indicator."""
        raise NotImplementedError
