from typing import Any

from apogeebacktest.indicators import Indicator
from apogeebacktest.data import Market


class BookToPriceIndicator(Indicator):
    """Book-to-Price ratio."""

    def __init__(self):
        self.__market = Market()


    def getValue(self, code:str, date:Any) -> float:
        """Book-to-Price ratio of a stock at a given date.

        Parameters
        ----------
        code : str
            Stock code.
        date : any
            Intentionally left ambiguous, as it is just a key for column lookup in this case study.

        Returns
        -------
        float
            Book-to-Price ratio.
        """
        return self.__market.getBP(code, date)
