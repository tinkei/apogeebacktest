from abc import ABC, abstractmethod
import numpy as np
from typing import Any, Tuple


class Strategy(ABC):
    """An abstract base class for strategy."""

    def __init__(self, **kwargs) -> None:
        super(Strategy, self).__init__()


    @abstractmethod
    def updatePortfolio(self, date:Any) -> None:
        """Update portfolio selection based on strategy/signal/indicator.

        Parameters
        ----------
        date : Any
            Date on which the portfolio is updated.
            Remember that the performance evaluation must be done at a later date.
        """
        pass


    @abstractmethod
    def evalStrategy(self) -> Tuple[np.array, np.array, np.array]:
        pass
