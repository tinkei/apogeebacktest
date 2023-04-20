import numpy as np
from functools import reduce


class GeomReturn:
    """A collection of convenience functions for manipulating geometric returns.

    How geometric return averages across a portfolio differs from how it behaves over time.
    Logarithmic return behaves vert differently as well.
    While the calulations are trivial, they are encapsulated here to avoid careless mistakes.

    $$GeomR_{t} = S_{t} / S_{t-1} - 1$$
    $$LogR_{t} = ln{(S_{t} / S_{t-1})}$$
    """

    def __init__(self, returns:np.array):
        assert returns is not None
        self.__returns = returns
        # To enable builder pattern.
        self.toLogReturn = self._toLogReturn
        self.averageOverPortfolio = self._averageOverPortfolio
        self.averageOverTime = self._averageOverTime
        self.compoundOverTime = self._compoundOverTime
        self.accumulateOverTime = self._accumulateOverTime
        self.averageOverPortfolioAndTime = self._averageOverPortfolioAndTime
        self.compoundOverPortfolioAndTime = self._compoundOverPortfolioAndTime
        self.accumulateOverPortfolioAndTime = self._accumulateOverPortfolioAndTime


    def result(self) -> np.array:
        """Return processed geometric return.

        Returns
        -------
        np.array
            Geometric return.
        """
        return self.__returns


    def getReturns(self) -> np.array:
        """Return processed geometric return.

        Returns
        -------
        np.array
            Geometric return.
        """
        return self.__returns


    @staticmethod
    def toLogReturn(returns:np.array) -> np.array:
        """Convert geometric return into log return.

        Parameters
        ----------
        returns: np.array
            Geometric return.

        Returns
        -------
        np.array
            Log return.
        """
        return np.log(1 + returns)


    def _toLogReturn(self) -> 'LogReturn':
        """Convert geometric return into log return.

        Returns
        -------
        LogReturn
            Log return object.
        """
        return LogReturn(np.log(1 + self.__returns))


    @staticmethod
    def averageOverPortfolio(returns:np.array, weights:np.array=None, portfolio_axis:int=1) -> np.array:
        """Average returns over portfolio axis.

        Parameters
        ----------
        returns: np.array
            Geometric return. 1D or 2D. Default shape (portfolio,) or (time,portfolio).
        weights: np.array
            Portfolio weights. 1D or 2D, if exists. Default shape (portfolio,) or (time,portfolio).
        portfolio_axis: int
            Axis where the portfolio weights at a slice of time is given.
            Inferred if not provided.

        Returns
        -------
        np.array
            Geometric return. One less dimension than input.
        """
        assert returns is not None and returns.ndim > 0
        if weights is None and returns.ndim == 1:
            return np.mean(returns)
        if weights is None and returns.ndim > 1:
            return np.mean(returns, axis=portfolio_axis)
        if returns.ndim == 1 and weights.ndim == 1:
            return np.dot(returns, weights)
        if weights.ndim == 1:
            return np.tensordot(returns, weights, axes=([portfolio_axis],[0]))
        if weights.ndim > 1:
            return np.tensordot(returns, weights, axes=([portfolio_axis],[portfolio_axis]))
        raise ValueError


    def _averageOverPortfolio(self, weights:np.array=None, portfolio_axis:int=1) -> 'GeomReturn':
        """Average returns over portfolio axis.

        Parameters
        ----------
        weights: np.array
            Portfolio weights. 1D or 2D, if exists. Default shape (portfolio,) or (time,portfolio).
        portfolio_axis: int
            Axis where the portfolio weights at a slice of time is given.
            Inferred if not provided.

        Returns
        -------
        GeomReturn
            Geometric return object. One less dimension than input.
        """
        assert self.__returns.ndim > 0
        if weights is None and self.__returns.ndim == 1:
            self.__returns = np.mean(self.__returns)
            return self
        if weights is None and self.__returns.ndim > 1:
            self.__returns = np.mean(self.__returns, axis=portfolio_axis)
            return self
        if self.__returns.ndim == 1 and weights.ndim == 1:
            self.__returns = np.dot(self.__returns, weights)
            return self
        if weights.ndim == 1:
            self.__returns = np.tensordot(self.__returns, weights, axes=([portfolio_axis],[0]))
            return self
        if weights.ndim > 1:
            self.__returns = np.tensordot(self.__returns, weights, axes=([portfolio_axis],[portfolio_axis]))
            return self
        raise ValueError


    @staticmethod
    def averageOverTime(returns:np.array, portfolio_axis:int=1) -> np.array:
        """Average returns over time.

        Parameters
        ----------
        returns: np.array
            Geometric return. 1D or 2D. Default shape (time,) or (time,portfolio).
        portfolio_axis: int
            Axis where the portfolio weights at a slice of time is given, if exists.
            Inferred if not provided.

        Returns
        -------
        np.array
            Geometric return. One less dimension than input.
        """
        assert returns is not None and returns.ndim > 0
        if returns.ndim == 1:
            time_axis = 0
        else:
            time_axis = tuple(axis for axis in range(returns.ndim) if axis != portfolio_axis)
        # return np.power(reduce(lambda R_cum, r: R_cum * (1+r), returns, 1), 1/len(returns)) - 1
        return np.power(np.multiply.reduce(np.add(returns, 1), initial=1, axis=time_axis), 1/len(returns)) - 1


    def _averageOverTime(self, portfolio_axis:int=1) -> 'GeomReturn':
        """Average returns over time.

        Parameters
        ----------
        portfolio_axis: int
            Axis where the portfolio weights at a slice of time is given, if exists.
            Inferred if not provided.

        Returns
        -------
        GeomReturn
            Geometric return object. One less dimension than input.
        """
        assert self.__returns.ndim > 0
        if self.__returns.ndim == 1:
            time_axis = 0
        else:
            time_axis = tuple(axis for axis in range(self.__returns.ndim) if axis != portfolio_axis)
        # return np.power(reduce(lambda R_cum, r: R_cum * (1+r), returns, 1), 1/len(returns)) - 1
        self.__returns = np.power(np.multiply.reduce(np.add(self.__returns, 1), initial=1, axis=time_axis), 1/len(self.__returns)) - 1
        return self


    @staticmethod
    def compoundOverTime(returns:np.array, portfolio_axis:int=1) -> np.array:
        """Compound returns over time.

        Parameters
        ----------
        returns: np.array
            Geometric return. 1D or 2D. Default shape (time,) or (time,portfolio).
        portfolio_axis: int
            Axis where the portfolio weights at a slice of time is given, if exists.
            Inferred if not provided.

        Returns
        -------
        np.array
            Geometric return. One less dimension than input.
        """
        assert returns is not None and returns.ndim > 0
        if returns.ndim == 1:
            time_axis = 0
        else:
            time_axis = tuple(axis for axis in range(returns.ndim) if axis != portfolio_axis)
        # return reduce(lambda R_cum, r: R_cum * (1+r), returns, 1) - 1
        return np.multiply.reduce(np.add(returns, 1), initial=1, axis=time_axis) - 1


    def _compoundOverTime(self, portfolio_axis:int=1) -> 'GeomReturn':
        """Compound returns over time.

        Parameters
        ----------
        portfolio_axis: int
            Axis where the portfolio weights at a slice of time is given, if exists.
            Inferred if not provided.

        Returns
        -------
        GeomReturn
            Geometric return object. One less dimension than input.
        """
        assert self.__returns.ndim > 0
        if self.__returns.ndim == 1:
            time_axis = 0
        else:
            time_axis = tuple(axis for axis in range(self.__returns.ndim) if axis != portfolio_axis)
        # return reduce(lambda R_cum, r: R_cum * (1+r), returns, 1) - 1
        self.__returns = np.multiply.reduce(np.add(self.__returns, 1), initial=1, axis=time_axis) - 1
        return self


    @staticmethod
    def accumulateOverTime(returns:np.array, portfolio_axis:int=1) -> np.array:
        """Accumulate returns over time.

        Parameters
        ----------
        returns: np.array
            Geometric return. 1D or 2D. Default shape (time,) or (time,portfolio).
        portfolio_axis: int
            Axis where the portfolio weights at a slice of time is given, if exists.
            Inferred if not provided.

        Returns
        -------
        np.array
            Geometric return. Same dimensions as input.
        """
        assert returns is not None and returns.ndim > 0
        if returns.ndim == 1:
            time_axis = 0
        else:
            time_axis = tuple(axis for axis in range(returns.ndim) if axis != portfolio_axis)
        return np.multiply.accumulate(np.add(returns, 1), axis=time_axis) - 1


    def _accumulateOverTime(self, portfolio_axis:int=1) -> 'GeomReturn':
        """Accumulate returns over time.

        Parameters
        ----------
        portfolio_axis: int
            Axis where the portfolio weights at a slice of time is given, if exists.
            Inferred if not provided.

        Returns
        -------
        GeomReturn
            Geometric return object. Same dimensions as input.
        """
        assert self.__returns.ndim > 0
        if self.__returns.ndim == 1:
            time_axis = 0
        else:
            time_axis = tuple(axis for axis in range(self.__returns.ndim) if axis != portfolio_axis)
        self.__returns = np.multiply.accumulate(np.add(self.__returns, 1), axis=time_axis) - 1
        return self


    @staticmethod
    def averageOverPortfolioAndTime(returns:np.array, weights:np.array=None, portfolio_axis:int=1) -> np.array:
        """Average returns over time.

        Parameters
        ----------
        returns: np.array
            Geometric return. 2D. Default shape (time,portfolio).
        weights: np.array
            Portfolio weights. 1D or 2D, if exists. Default shape (portfolio,) or (time,portfolio).
        portfolio_axis: int
            Axis where the portfolio weights at a slice of time is given, if exists.
            Inferred if not provided.

        Returns
        -------
        np.array
            Geometric return. Two less dimensions than input.
        """
        assert returns is not None and returns.ndim > 1
        if weights is None or (weights is not None and weights.ndim == 1):
            # Hold the same number of shares from start to end.
            return GeomReturn.averageOverPortfolio(GeomReturn.averageOverTime(returns, portfolio_axis), weights)
        if weights is not None and weights.ndim > 1:
            # Dynamically rebalance the portfolio over time.
            return GeomReturn.averageOverTime(GeomReturn.averageOverPortfolio(returns, weights, portfolio_axis))


    def _averageOverPortfolioAndTime(self, weights:np.array=None, portfolio_axis:int=1) -> 'GeomReturn':
        """Average returns over time.

        Parameters
        ----------
        weights: np.array
            Portfolio weights. 1D or 2D, if exists. Default shape (portfolio,) or (time,portfolio).
        portfolio_axis: int
            Axis where the portfolio weights at a slice of time is given, if exists.
            Inferred if not provided.

        Returns
        -------
        GeomReturn
            Geometric return object. Two less dimensions than input.
        """
        assert self.__returns.ndim > 1
        if weights is None or (weights is not None and weights.ndim == 1):
            # Hold the same number of shares from start to end.
            return self.averageOverTime(portfolio_axis).averageOverPortfolio(weights)
        if weights is not None and weights.ndim > 1:
            # Dynamically rebalance the portfolio over time.
            return self.averageOverPortfolio(weights, portfolio_axis).averageOverTime()


    @staticmethod
    def compoundOverPortfolioAndTime(returns:np.array, weights:np.array=None, portfolio_axis:int=1) -> np.array:
        """Compound returns over time.

        Parameters
        ----------
        returns: np.array
            Geometric return. 2D. Default shape (time,portfolio).
        weights: np.array
            Portfolio weights. 1D or 2D, if exists. Default shape (portfolio,) or (time,portfolio).
        portfolio_axis: int
            Axis where the portfolio weights at a slice of time is given, if exists.
            Inferred if not provided.

        Returns
        -------
        np.array
            Geometric return. Two less dimensions than input.
        """
        assert returns is not None and returns.ndim > 1
        if weights is None or (weights is not None and weights.ndim == 1):
            # Hold the same number of shares from start to end.
            return GeomReturn.averageOverPortfolio(GeomReturn.compoundOverTime(returns, portfolio_axis), weights)
        if weights is not None and weights.ndim > 1:
            # Dynamically rebalance the portfolio over time.
            return GeomReturn.compoundOverTime(GeomReturn.averageOverPortfolio(returns, weights, portfolio_axis))


    def _compoundOverPortfolioAndTime(self, weights:np.array=None, portfolio_axis:int=1) -> 'GeomReturn':
        """Compound returns over time.

        Parameters
        ----------
        weights: np.array
            Portfolio weights. 1D or 2D, if exists. Default shape (portfolio,) or (time,portfolio).
        portfolio_axis: int
            Axis where the portfolio weights at a slice of time is given, if exists.
            Inferred if not provided.

        Returns
        -------
        GeomReturn
            Geometric return object. Two less dimensions than input.
        """
        assert self.__returns.ndim > 1
        if weights is None or (weights is not None and weights.ndim == 1):
            # Hold the same number of shares from start to end.
            return self.compoundOverTime(portfolio_axis).averageOverPortfolio(weights)
        if weights is not None and weights.ndim > 1:
            # Dynamically rebalance the portfolio over time.
            return self.averageOverPortfolio(weights, portfolio_axis).compoundOverTime()


    @staticmethod
    def accumulateOverPortfolioAndTime(returns:np.array, weights:np.array=None, portfolio_axis:int=1) -> np.array:
        """Accumulate returns over time.

        Parameters
        ----------
        returns: np.array
            Geometric return. 2D. Default shape (time,portfolio).
        weights: np.array
            Portfolio weights. 1D or 2D, if exists. Default shape (portfolio,) or (time,portfolio).
        portfolio_axis: int
            Axis where the portfolio weights at a slice of time is given, if exists.
            Inferred if not provided.

        Returns
        -------
        np.array
            Geometric return. One less dimension than input.
        """
        assert returns is not None and returns.ndim > 1
        if weights is None or (weights is not None and weights.ndim == 1):
            # Hold the same number of shares from start to end.
            return GeomReturn.averageOverPortfolio(GeomReturn.accumulateOverTime(returns, portfolio_axis), weights, portfolio_axis)
        if weights is not None and weights.ndim > 1:
            # Dynamically rebalance the portfolio over time.
            return GeomReturn.accumulateOverTime(GeomReturn.averageOverPortfolio(returns, weights, portfolio_axis), portfolio_axis)


    def _accumulateOverPortfolioAndTime(self, weights:np.array=None, portfolio_axis:int=1) -> 'GeomReturn':
        """Accumulate returns over time.

        Parameters
        ----------
        weights: np.array
            Portfolio weights. 1D or 2D, if exists. Default shape (portfolio,) or (time,portfolio).
        portfolio_axis: int
            Axis where the portfolio weights at a slice of time is given, if exists.
            Inferred if not provided.

        Returns
        -------
        GeomReturn
            Geometric return object. One less dimension than input.
        """
        assert self.__returns.ndim > 1
        if weights is None or (weights is not None and weights.ndim == 1):
            # Hold the same number of shares from start to end.
            return self.accumulateOverTime(portfolio_axis).averageOverPortfolio(weights, portfolio_axis)
        if weights is not None and weights.ndim > 1:
            # Dynamically rebalance the portfolio over time.
            return self.averageOverPortfolio(weights, portfolio_axis).accumulateOverTime(portfolio_axis)


class LogReturn:
    """A collection of convenience functions for manipulating logarithmic returns.
    
    How logarithmic return averages across a portfolio differs from how it behaves over time.
    Geometric return behaves vert differently as well.
    While the calulations are trivial, they are encapsulated here to avoid careless mistakes.

    $$GeomR_{t} = S_{t} / S_{t-1} - 1$$
    $$LogR_{t} = ln{(S_{t} / S_{t-1})}$$
    """

    def __init__(self, returns:np.array):
        assert returns is not None
        self.__returns = returns
        # To enable builder pattern.
        self.toGeomReturn = self._toGeomReturn
        self.averageOverPortfolio = self._averageOverPortfolio
        self.averageOverTime = self._averageOverTime
        self.compoundOverTime = self._compoundOverTime
        self.accumulateOverTime = self._accumulateOverTime
        self.averageOverPortfolioAndTime = self._averageOverPortfolioAndTime
        self.compoundOverPortfolioAndTime = self._compoundOverPortfolioAndTime
        self.accumulateOverPortfolioAndTime = self._accumulateOverPortfolioAndTime


    def result(self) -> np.array:
        """Return processed log return.

        Returns
        -------
        np.array
            Log return.
        """
        return self.__returns


    def getReturns(self) -> np.array:
        """Return processed log return.

        Returns
        -------
        np.array
            Log return.
        """
        return self.__returns


    @staticmethod
    def toGeomReturn(returns:np.array) -> np.array:
        """Convert log return into geometric return.

        Parameters
        ----------
        returns: np.array
            Log return.

        Returns
        -------
        np.array
            Geometric return.
        """
        return np.exp(returns) - 1


    def _toGeomReturn(self) -> 'GeomReturn':
        """Convert log return into geometric return.

        Returns
        -------
        GeomReturn
            Geometric return object.
        """
        return GeomReturn(np.exp(self.__returns) - 1)


    @staticmethod
    def averageOverPortfolio(returns:np.array, weights:np.array=None, portfolio_axis:int=1) -> np.array:
        """Average returns over portfolio axis.

        Parameters
        ----------
        returns: np.array
            Log return. 1D or 2D. Default shape (portfolio,) or (time,portfolio).
        weights: np.array
            Portfolio weights. 1D or 2D, if exists. Default shape (portfolio,) or (time,portfolio).
        portfolio_axis: int
            Axis where the portfolio weights at a slice of time is given.
            Inferred if not provided.

        Returns
        -------
        np.array
            Log return. One less dimension than input.
        """
        assert returns is not None and returns.ndim > 0
        if weights is None and returns.ndim == 1:
            return np.log(np.mean(np.exp(returns)))
        if weights is None and returns.ndim > 1:
            return np.log(np.mean(np.exp(returns), axis=portfolio_axis))
        if returns.ndim == 1 and weights.ndim == 1:
            return np.log(1 + np.dot(np.exp(returns) - 1, weights))
        if weights.ndim == 1:
            return np.log(1 + np.tensordot(np.exp(returns) - 1, weights, axes=([portfolio_axis],[0])))
        if weights.ndim > 1:
            return np.log(1 + np.tensordot(np.exp(returns) - 1, weights, axes=([portfolio_axis],[portfolio_axis])))
        raise ValueError


    def _averageOverPortfolio(self, weights:np.array=None, portfolio_axis:int=1) -> 'LogReturn':
        """Average returns over portfolio axis.

        Parameters
        ----------
        weights: np.array
            Portfolio weights. 1D or 2D, if exists. Default shape (portfolio,) or (time,portfolio).
        portfolio_axis: int
            Axis where the portfolio weights at a slice of time is given.
            Inferred if not provided.

        Returns
        -------
        LogReturn
            Log return object. One less dimension than input.
        """
        assert self.__returns.ndim > 0
        if weights is None and self.__returns.ndim == 1:
            self.__returns = np.log(np.mean(np.exp(self.__returns)))
            return self
        if weights is None and self.__returns.ndim > 1:
            self.__returns = np.log(np.mean(np.exp(self.__returns), axis=portfolio_axis))
            return self
        if self.__returns.ndim == 1 and weights.ndim == 1:
            self.__returns = np.log(1 + np.dot(np.exp(self.__returns) - 1, weights))
            return self
        if weights.ndim == 1:
            self.__returns = np.log(1 + np.tensordot(np.exp(self.__returns) - 1, weights, axes=([portfolio_axis],[0])))
            return self
        if weights.ndim > 1:
            self.__returns = np.log(1 + np.tensordot(np.exp(self.__returns) - 1, weights, axes=([portfolio_axis],[portfolio_axis])))
            return self
        raise ValueError


    @staticmethod
    def averageOverTime(returns:np.array, portfolio_axis:int=1) -> np.array:
        """Average returns over time.

        Parameters
        ----------
        returns: np.array
            Log return. 1D or 2D. Default shape (time,) or (time,portfolio).
        portfolio_axis: int
            Axis where the portfolio weights at a slice of time is given, if exists.
            Inferred if not provided.

        Returns
        -------
        np.array
            Log return. One less dimension than input.
        """
        assert returns is not None and returns.ndim > 0
        if returns.ndim == 1:
            time_axis = 0
        else:
            time_axis = tuple(axis for axis in range(returns.ndim) if axis != portfolio_axis)
        return np.mean(returns, axis=time_axis)


    def _averageOverTime(self, portfolio_axis:int=1) -> 'LogReturn':
        """Average returns over time.

        Parameters
        ----------
        portfolio_axis: int
            Axis where the portfolio weights at a slice of time is given, if exists.
            Inferred if not provided.

        Returns
        -------
        LogReturn
            Log return object. One less dimension than input.
        """
        assert self.__returns.ndim > 0
        if self.__returns.ndim == 1:
            time_axis = 0
        else:
            time_axis = tuple(axis for axis in range(self.__returns.ndim) if axis != portfolio_axis)
        self.__returns = np.mean(self.__returns, axis=time_axis)
        return self


    @staticmethod
    def compoundOverTime(returns:np.array, portfolio_axis:int=1) -> np.array:
        """Compound returns over time.

        Parameters
        ----------
        returns: np.array
            Log return. 1D or 2D. Default shape (time,) or (time,portfolio).
        portfolio_axis: int
            Axis where the portfolio weights at a slice of time is given, if exists.
            Inferred if not provided.

        Returns
        -------
        np.array
            Log return. One less dimension than input.
        """
        assert returns is not None and returns.ndim > 0
        if returns.ndim == 1:
            time_axis = 0
        else:
            time_axis = tuple(axis for axis in range(returns.ndim) if axis != portfolio_axis)
        return np.sum(returns, axis=time_axis)


    def _compoundOverTime(self, portfolio_axis:int=1) -> 'LogReturn':
        """Compound returns over time.

        Parameters
        ----------
        portfolio_axis: int
            Axis where the portfolio weights at a slice of time is given, if exists.
            Inferred if not provided.

        Returns
        -------
        LogReturn
            Log return object. One less dimension than input.
        """
        assert self.__returns.ndim > 0
        if self.__returns.ndim == 1:
            time_axis = 0
        else:
            time_axis = tuple(axis for axis in range(self.__returns.ndim) if axis != portfolio_axis)
        self.__returns = np.sum(self.__returns, axis=time_axis)
        return self


    @staticmethod
    def accumulateOverTime(returns:np.array, portfolio_axis:int=1) -> np.array:
        """Accumulate returns over time.

        Parameters
        ----------
        returns: np.array
            Log return. 1D or 2D. Default shape (time,) or (time,portfolio).
        portfolio_axis: int
            Axis where the portfolio weights at a slice of time is given, if exists.
            Inferred if not provided.

        Returns
        -------
        np.array
            Log return. Same dimensions as input.
        """
        assert returns is not None and returns.ndim > 0
        if returns.ndim == 1:
            time_axis = 0
        else:
            time_axis = tuple(axis for axis in range(returns.ndim) if axis != portfolio_axis)
        return np.add.accumulate(returns, axis=time_axis)


    def _accumulateOverTime(self, portfolio_axis:int=1) -> 'LogReturn':
        """Accumulate returns over time.

        Parameters
        ----------
        portfolio_axis: int
            Axis where the portfolio weights at a slice of time is given, if exists.
            Inferred if not provided.

        Returns
        -------
        LogReturn
            Log return object. Same dimensions as input.
        """
        assert self.__returns.ndim > 0
        if self.__returns.ndim == 1:
            time_axis = 0
        else:
            time_axis = tuple(axis for axis in range(self.__returns.ndim) if axis != portfolio_axis)
        self.__returns = np.add.accumulate(self.__returns, axis=time_axis)
        return self


    @staticmethod
    def averageOverPortfolioAndTime(returns:np.array, weights:np.array=None, portfolio_axis:int=1) -> np.array:
        """Average returns over time.

        Parameters
        ----------
        returns: np.array
            Log return. 2D. Default shape (time,portfolio).
        weights: np.array
            Portfolio weights. 1D or 2D, if exists. Default shape (portfolio,) or (time,portfolio).
        portfolio_axis: int
            Axis where the portfolio weights at a slice of time is given, if exists.
            Inferred if not provided.

        Returns
        -------
        np.array
            Log return. Two less dimensions than input.
        """
        assert returns is not None and returns.ndim > 1
        if weights is None or (weights is not None and weights.ndim == 1):
            # Hold the same number of shares from start to end.
            return LogReturn.averageOverPortfolio(LogReturn.averageOverTime(returns, portfolio_axis), weights)
        if weights is not None and weights.ndim > 1:
            # Dynamically rebalance the portfolio over time.
            return LogReturn.averageOverTime(LogReturn.averageOverPortfolio(returns, weights, portfolio_axis))


    def _averageOverPortfolioAndTime(self, weights:np.array=None, portfolio_axis:int=1) -> 'LogReturn':
        """Average returns over time.

        Parameters
        ----------
        weights: np.array
            Portfolio weights. 1D or 2D, if exists. Default shape (portfolio,) or (time,portfolio).
        portfolio_axis: int
            Axis where the portfolio weights at a slice of time is given, if exists.
            Inferred if not provided.

        Returns
        -------
        LogReturn
            Log return object. Two less dimensions than input.
        """
        assert self.__returns.ndim > 1
        if weights is None or (weights is not None and weights.ndim == 1):
            # Hold the same number of shares from start to end.
            return self.averageOverTime(portfolio_axis).averageOverPortfolio(weights)
        if weights is not None and weights.ndim > 1:
            # Dynamically rebalance the portfolio over time.
            return self.averageOverPortfolio(weights, portfolio_axis).averageOverTime()


    @staticmethod
    def compoundOverPortfolioAndTime(returns:np.array, weights:np.array=None, portfolio_axis:int=1) -> np.array:
        """Compound returns over time.

        Parameters
        ----------
        returns: np.array
            Log return. 2D. Default shape (time,portfolio).
        weights: np.array
            Portfolio weights. 1D or 2D, if exists. Default shape (portfolio,) or (time,portfolio).
        portfolio_axis: int
            Axis where the portfolio weights at a slice of time is given, if exists.
            Inferred if not provided.

        Returns
        -------
        np.array
            Log return. Two less dimensions than input.
        """
        assert returns is not None and returns.ndim > 1
        if weights is None or (weights is not None and weights.ndim == 1):
            # Hold the same number of shares from start to end.
            return LogReturn.averageOverPortfolio(LogReturn.compoundOverTime(returns, portfolio_axis), weights)
        if weights is not None and weights.ndim > 1:
            # Dynamically rebalance the portfolio over time.
            return LogReturn.compoundOverTime(LogReturn.averageOverPortfolio(returns, weights, portfolio_axis))


    def _compoundOverPortfolioAndTime(self, weights:np.array=None, portfolio_axis:int=1) -> 'LogReturn':
        """Compound returns over time.

        Parameters
        ----------
        weights: np.array
            Portfolio weights. 1D or 2D, if exists. Default shape (portfolio,) or (time,portfolio).
        portfolio_axis: int
            Axis where the portfolio weights at a slice of time is given, if exists.
            Inferred if not provided.

        Returns
        -------
        LogReturn
            Log return object. Two less dimensions than input.
        """
        assert self.__returns.ndim > 1
        if weights is None or (weights is not None and weights.ndim == 1):
            # Hold the same number of shares from start to end.
            return self.compoundOverTime(portfolio_axis).averageOverPortfolio(weights)
        if weights is not None and weights.ndim > 1:
            # Dynamically rebalance the portfolio over time.
            return self.averageOverPortfolio(weights, portfolio_axis).compoundOverTime()


    @staticmethod
    def accumulateOverPortfolioAndTime(returns:np.array, weights:np.array=None, portfolio_axis:int=1) -> np.array:
        """Accumulate returns over time.

        Parameters
        ----------
        returns: np.array
            Log return. 2D. Default shape (time,portfolio).
        weights: np.array
            Portfolio weights. 1D or 2D, if exists. Default shape (portfolio,) or (time,portfolio).
        portfolio_axis: int
            Axis where the portfolio weights at a slice of time is given, if exists.
            Inferred if not provided.

        Returns
        -------
        np.array
            Log return. One less dimension than input.
        """
        assert returns is not None and returns.ndim > 1
        if weights is None or (weights is not None and weights.ndim == 1):
            # Hold the same number of shares from start to end.
            return LogReturn.averageOverPortfolio(LogReturn.accumulateOverTime(returns, portfolio_axis), weights, portfolio_axis)
        if weights is not None and weights.ndim > 1:
            # Dynamically rebalance the portfolio over time.
            return LogReturn.accumulateOverTime(LogReturn.averageOverPortfolio(returns, weights, portfolio_axis), portfolio_axis)


    def _accumulateOverPortfolioAndTime(self, weights:np.array=None, portfolio_axis:int=1) -> 'LogReturn':
        """Accumulate returns over time.

        Parameters
        ----------
        weights: np.array
            Portfolio weights. 1D or 2D, if exists. Default shape (portfolio,) or (time,portfolio).
        portfolio_axis: int
            Axis where the portfolio weights at a slice of time is given, if exists.
            Inferred if not provided.

        Returns
        -------
        LogReturn
            Log return object. One less dimension than input.
        """
        assert self.__returns.ndim > 1
        if weights is None or (weights is not None and weights.ndim == 1):
            # Hold the same number of shares from start to end.
            return self.accumulateOverTime(portfolio_axis).averageOverPortfolio(weights, portfolio_axis)
        if weights is not None and weights.ndim > 1:
            # Dynamically rebalance the portfolio over time.
            return self.averageOverPortfolio(weights, portfolio_axis).accumulateOverTime(portfolio_axis)


    # ==================================================
    # Builder pattern not implemented for the following.
    # ==================================================

    def annualizedReturn(log_return:float, T:float) -> float:
        """Compute annualized return, a.k.a. drift.

        Parameters
        ----------
        log_return: float
            Overall log return.
        T: float
            Total time over which the above log return is calculated. Unit: years.
            e.g. If the input is average monthly return, then T=1/12.
            If the input is total return over 3 years, then T=3.

        Returns
        -------
        float
            Annualized portfolio log return.
        """
        return log_return / T


    def volatility(returns:np.array, weights:np.array=None, portfolio_axis:int=1) -> float:
        """Compute volatility.

        Parameters
        ----------
        returns: np.array
            Log return. 1D or 2D. Default shape (time,) or (time,portfolio).
        weights: np.array
            Portfolio weights. 1D or 2D, if exists. Default shape (portfolio,) or (time,portfolio).
        portfolio_axis: int
            Axis where the portfolio weights at a slice of time is given, if exists.
            Inferred if not provided.

        Returns
        -------
        float
            Volatility of portfolio.
        """
        assert returns is not None and returns.ndim > 0
        if returns.ndim == 1:
            return np.std(returns)
        else:
            return np.std(LogReturn.averageOverPortfolio(returns, weights, portfolio_axis))


    def annualizedVolatility(volatility:float, dt:float) -> float:
        """Compute annualized volatility.

        Parameters
        ----------
        volatility: float
            Volatility over a certain time period.
        dt: float
            Time step between datapoints when computing the above volatility, per unit year.
            e.g. Monthly data: dt=1/12; weekly data: dt=1/52.; daily data: dt=1/252.

        Returns
        -------
        float
            Annualized volatility.
        """
        return volatility / np.sqrt(dt)
