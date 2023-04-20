import numpy as np
from typing import Any, Optional, Tuple, List

from apogeebacktest.strategies import Strategy
from apogeebacktest.instruments import Portfolio
from apogeebacktest.signals import BestBPSignal, WorstBPSignal
from apogeebacktest.data import Market


class BestBPStrategy(Strategy):
    """A strategy that longs an equal-weight porftolio of stocks with the highest book-to-price ratios."""

    def __init__(self):
        self._portfolio = None
        self.__market = Market()
        self._timeframe = self.__market.getTimeframe()


    def createPortfolio(self) -> None:
        """Create an initial portfolio."""
        self._portfolio = Portfolio([],[])


    def updatePortfolio(self, date:Any, selection:float=0.2) -> None:
        """Update portfolio selection based on strategy/signal/indicator.

        Parameters
        ----------
        date : Any
            Date on which the portfolio is updated.
            Remember that the performance evaluation must be done at a later date.
        selection: float
            Proportion of stocks with the best/worst-performing book-to-price ratios to include in the portfolio.
        """
        if self._portfolio is None:
            self.createPortfolio()
        best_bp = BestBPSignal().getSignal(date)
        best_bp = best_bp[:int(selection*len(best_bp))]

        # print('List of best BP selected:')
        # print(best_bp)
        # print('List of worst BP selected:')
        # print(worst_bp)

        orders_executed = self._portfolio.diffUpdatePortfolio(
            list(map(lambda x: x[0], best_bp)), 
            []
        )


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
        geom_returns = np.zeros_like(timeframe[1:], dtype=float)
        log_returns = np.zeros_like(timeframe[1:], dtype=float)
        for i in range(len(timeframe[1:])):
            # print(f'Updated portfolio selection on {timeframe[i]}.')
            self.updatePortfolio(timeframe[i])
            # print(f'Evaluated portfolio returns on {timeframe[i+1]}.\n')
            geom_returns[i] = self._portfolio.getReturn(timeframe[i+1])
            log_returns[i] = self._portfolio.getLogReturn(timeframe[i+1])
        return timeframe[1:], geom_returns, log_returns



class WorstBPStrategy(Strategy):
    """A strategy that shorts an equal-weight porftolio of stocks with the lowest book-to-price ratios."""

    def __init__(self):
        self._portfolio = None
        self.__market = Market()
        self._timeframe = self.__market.getTimeframe()


    def createPortfolio(self) -> None:
        """Create an initial portfolio."""
        self._portfolio = Portfolio([],[])


    def updatePortfolio(self, date:Any, selection:float=0.2) -> None:
        """Update portfolio selection based on strategy/signal/indicator.

        Parameters
        ----------
        date : Any
            Date on which the portfolio is updated.
            Remember that the performance evaluation must be done at a later date.
        selection: float
            Proportion of stocks with the best/worst-performing book-to-price ratios to include in the portfolio.
        """
        if self._portfolio is None:
            self.createPortfolio()
        worst_bp = WorstBPSignal().getSignal(date)
        worst_bp = worst_bp[:int(selection*len(worst_bp))]

        # print('List of best BP selected:')
        # print(best_bp)
        # print('List of worst BP selected:')
        # print(worst_bp)

        orders_executed = self._portfolio.diffUpdatePortfolio(
            [], 
            list(map(lambda x: x[0], worst_bp))
        )


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
        geom_returns = np.zeros_like(timeframe[1:], dtype=float)
        log_returns = np.zeros_like(timeframe[1:], dtype=float)
        for i in range(len(timeframe[1:])):
            # print(f'Updated portfolio selection on {timeframe[i]}.')
            self.updatePortfolio(timeframe[i])
            # print(f'Evaluated portfolio returns on {timeframe[i+1]}.\n')
            geom_returns[i] = self._portfolio.getReturn(timeframe[i+1])
            log_returns[i] = self._portfolio.getLogReturn(timeframe[i+1])
        return timeframe[1:], geom_returns, log_returns



class LongShortBPStrategy(Strategy):
    """A strategy that longs an equal-weight porftolio of stocks with the highest 
    book-to-price ratios and shorts the lowest book-to-price ratios."""

    def __init__(self):
        self._portfolio = None
        self.__market = Market()
        self._timeframe = self.__market.getTimeframe()


    def createPortfolio(self) -> None:
        """Create an initial portfolio."""
        self._portfolio = Portfolio([],[])


    def updatePortfolio(self, date:Any, selection:float=0.2) -> None:
        """Update portfolio selection based on strategy/signal/indicator.

        Parameters
        ----------
        date : Any
            Date on which the portfolio is updated.
            Remember that the performance evaluation must be done at a later date.
        selection: float
            Proportion of stocks with the best/worst-performing book-to-price ratios to include in the portfolio.
        """
        if self._portfolio is None:
            self.createPortfolio()
        best_bp = BestBPSignal().getSignal(date)
        best_bp = best_bp[:int(selection*len(best_bp))]
        worst_bp = WorstBPSignal().getSignal(date)
        worst_bp = worst_bp[:int(selection*len(worst_bp))]
        
        # print('List of best BP selected:')
        # print(best_bp)
        # print('List of worst BP selected:')
        # print(worst_bp)

        orders_executed = self._portfolio.diffUpdatePortfolio(
            list(map(lambda x: x[0], best_bp)), 
            list(map(lambda x: x[0], worst_bp))
        )


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
        geom_returns = np.zeros_like(timeframe[1:], dtype=float)
        log_returns = np.zeros_like(timeframe[1:], dtype=float)
        for i in range(len(timeframe[1:])):
            # print(f'Updated portfolio selection on {timeframe[i]}.')
            self.updatePortfolio(timeframe[i])
            # print(f'Evaluated portfolio returns on {timeframe[i+1]}.\n')
            geom_returns[i] = self._portfolio.getReturn(timeframe[i+1])
            log_returns[i] = self._portfolio.getLogReturn(timeframe[i+1])
        return timeframe[1:], geom_returns, log_returns

