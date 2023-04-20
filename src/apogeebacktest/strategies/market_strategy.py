import numpy as np
from typing import Any, Optional, Tuple, List

from apogeebacktest.strategies import Strategy
from apogeebacktest.instruments import Portfolio


class MarketStrategy(Strategy):
    """A strategy that purchases an equal-weight porftolio of the entire market."""

    def __init__(self):
        from apogeebacktest.data import Market
        self._portfolio = None
        self.__market = Market()
        self._timeframe = self.__market.getTimeframe()


    def createPortfolio(self) -> None:
        """Create an initial portfolio."""
        instruments = self.__market.getInstruments()
        self._portfolio = Portfolio(instruments)


    def updatePortfolio(self, date:Any) -> None:
        """Update portfolio based on strategy/signal/indicator.

        Parameters
        ----------
        date : Any
            Date on which the portfolio is updated.
            Remember that the performance evaluation must be done at a later date.
        """
        if self._portfolio is None:
            self.createPortfolio()
        # There is no update since we are holding the market portfolio.


    def evalStrategy(self, timeframe:Optional[List[Any]]=None) -> Tuple[np.array, np.array, np.array]:
        """Evaluate strategy performance in a given timeframe.

        Parameters
        ----------
        timeframe : Optional[List[Any]]
            Intentionally left ambiguous, as it is just a key for column lookup in this case study.
            Default to market's entire timeframe.

        Returns
        -------
        Tuple[np.array, np.array, np.array]
            A tuple of (timeframe, geom_returns, log_returns)
        """
        if timeframe is None:
            timeframe = np.array(self._timeframe)
        else:
            timeframe = np.array(timeframe)
        geom_returns = np.zeros_like(timeframe, dtype=float)
        log_returns = np.zeros_like(timeframe, dtype=float)
        for i, date in enumerate(timeframe):
            self.updatePortfolio(date)
            geom_returns[i] = self._portfolio.getReturn(date)
            log_returns[i] = self._portfolio.getLogReturn(date)
        return timeframe, geom_returns, log_returns
