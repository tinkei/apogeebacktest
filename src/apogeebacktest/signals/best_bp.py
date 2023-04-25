import numpy as np
from typing import Any, Optional, Tuple, List

from apogeebacktest.signals import Signal
from apogeebacktest.indicators import BookToPriceIndicator


class BestBPSignal(Signal):
    """Best Book-to-Price ratio signal. The higher the better."""

    def __init__(self, **kwargs) -> None:
        super(BestBPSignal, self).__init__(**kwargs)
        from apogeebacktest.data import Market
        self.__market = Market()


    def getSignal(self, date:Any) -> List[Tuple[str,float]]:
        """Get book-to-price ratio of available instruments, organized from best to worst.

        Parameters
        ----------
        date : any
            Intentionally left ambiguous, as it is just a key for column lookup in this case study.

        Returns
        -------
        List[Tuple[str,float]]
            Book-to-price ratio of available instruments, sorted from best to worst.
        """
        instruments = self.__market.getInstruments()
        bp = BookToPriceIndicator()
        bps = [bp.getValue(code, date) for code in instruments]
        perf = list(zip(instruments, bps))
        # print('List of BP:')
        # print(perf)
        perf = sorted(perf, key=lambda x: x[1], reverse=True)
        # print('List of BP sorted in descending order:')
        # print(perf)
        return perf
