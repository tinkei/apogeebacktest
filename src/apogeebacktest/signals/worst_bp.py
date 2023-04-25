import numpy as np
from typing import Any, Optional, Tuple, List

from apogeebacktest.signals import Signal
from apogeebacktest.indicators import BookToPriceIndicator


class WorstBPSignal(Signal):
    """Worst Book-to-Price ratio signal. The higher the better."""

    def __init__(self, **kwargs) -> None:
        super(WorstBPSignal, self).__init__(**kwargs)
        from apogeebacktest.data import Market
        self.__market = Market()


    def getSignal(self, date:Any) -> List[Tuple[str,float]]:
        """Get book-to-price ratio of available instruments, organized from worst to best.

        Parameters
        ----------
        date : any
            Intentionally left ambiguous, as it is just a key for column lookup in this case study.

        Returns
        -------
        List[Tuple[str,float]]
            Book-to-price ratio of available instruments, sorted from worst to best.
        """
        instruments = self.__market.getInstruments()
        bp = BookToPriceIndicator()
        bps = [bp.getValue(code, date) for code in instruments]
        perf = list(zip(instruments, bps))
        # print('List of BP:')
        # print(perf)
        perf = sorted(perf, key=lambda x: x[1])
        # print('List of BP sorted in ascending order:')
        # print(perf)
        return perf
