import numpy as np
from typing import Any, Optional, List

from apogeebacktest.instruments import Instrument


class Portfolio(Instrument):
    """A portfolio of instruments, which itself is a composite instrument."""

    def __init__(self, codes_long:Optional[List[str]]=None, codes_short:Optional[List[str]]=None):
        """Initialize the portfolio.

        Parameters
        ----------
        codes_long : Optional[List[str]]
            List of instruments to long.
        codes_short : Optional[List[str]]
            List of instruments to short.
        """
        from apogeebacktest.data import Market
        self.__market = Market()
        if codes_long is None:
            codes_long = []
        if codes_short is None:
            codes_short = []

        self._portfolio_long = {
            code : {
                'code': code,
                'instrument': self.__market.getType(code)(code),
                'weight': 1 / len(codes_long),
            } for code in codes_long
        }
        self._portfolio_short = {
            code : {
                'code': code,
                'instrument': self.__market.getType(code)(code),
                'weight': 1 / len(codes_short),
            } for code in codes_short
        }


    def diffUpdatePortfolio(self, codes_long:Optional[List[str]]=None, codes_short:Optional[List[str]]=None) -> List[str]:
        """Execute buy/sell trades on the existing portfolio to match a given new portfolio state.

        Parameters
        ----------
        codes_long : Optional[List[str]]
            List of instruments to long.
        codes_short : Optional[List[str]]
            List of instruments to short.

        Returns
        -------
        List[str]
            List of orders executed.
        """
        if codes_long is None:
            codes_long = []
        if codes_short is None:
            codes_short = []

        orders = []

        new_long = set(self._portfolio_long.keys()) ^ set(codes_long)
        # print(f'Number of differences in long portfolio: {len(new_long)}')
        # print(f'Difference in long portfolio: {new_long}')
        # print(f'Existing portfolio: {self._portfolio_long.keys()}')
        # print(f'New portfolio: {codes_long}')
        for code in new_long:
            if code in codes_long:
                self._portfolio_long[code] = {
                    'code': code,
                    'instrument': self.__market.getType(code)(code),
                    'weight': 1 / len(codes_long),
                }
                orders.append(f'Bought one unit of Stock {code}.')
            else:
                del self._portfolio_long[code] # .pop(code, None)
                orders.append(f'Sold one unit of Stock {code}.')

        new_short = set(self._portfolio_short.keys()) ^ set(codes_short)
        # print(f'Number of differences in short portfolio: {len(new_short)}')
        # print(f'Difference in short portfolio: {new_short}')
        # print(f'Existing portfolio: {self._portfolio_short.keys()}')
        # print(f'New portfolio: {codes_short}')
        for code in new_short:
            if code in codes_short:
                self._portfolio_short[code] = {
                    'code': code,
                    'instrument': self.__market.getType(code)(code),
                    'weight': - 1 / len(codes_short),
                }
                orders.append(f'Sold one unit of Stock {code}.')
            else:
                del self._portfolio_short[code] # .pop(code, None)
                orders.append(f'Bought one unit of Stock {code}.')

        # for order in orders:
        #     print(order)

        return orders


    def getReturn(self, date:Any) -> float:
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
        res = 0
        for instrument in self._portfolio_long.values():
            res += instrument['weight'] * instrument['instrument'].getReturn(date)
        for instrument in self._portfolio_short.values():
            res += instrument['weight'] * instrument['instrument'].getReturn(date)
        return res


    def getLogReturn(self, date:Any) -> float:
        """Monthly log return.

        Parameters
        ----------
        date : any
            Intentionally left ambiguous, as it is just a key for column lookup in this case study.

        Returns
        -------
        float
            Monthly log return.
        """
        return np.log(1 + self.getReturn(date))
