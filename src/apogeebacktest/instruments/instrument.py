from abc import ABC, abstractmethod


class Instrument(ABC):
    """An abstract base class for any tradeable instrument."""

    # If we add @abstractmethod, this abstract class can't be instantiated.
    # But then subclasses will be forced to implement __init__()...
    # @abstractmethod
    def __init__(self, multiplier:int=1, **kwargs) -> None:
        super(Instrument, self).__init__()
        self._multiplier = multiplier


    @property
    # @abstractmethod
    def multiplier(self):
        """Multiplier of an instrument."""
        return self._multiplier


    @multiplier.setter
    def multiplier(self, value:int):
        self._multiplier = value


    @abstractmethod
    def getReturn(self, date) -> float:
        """Monthly geometric return.

        Parameters
        ----------
        date : any
            Intentionally left ambiguous, as it is just a key for column lookup in this case study.

        Returns
        -------
        float
            Monthly geometric return.
        """
        raise NotImplementedError
