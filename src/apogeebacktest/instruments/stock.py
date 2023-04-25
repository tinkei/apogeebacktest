from typing import Any

from apogeebacktest.instruments import Instrument


class Stock(Instrument):
    """A stock."""

    def __init__(self, code:str, **kwargs) -> None:
        super(Stock, self).__init__(**kwargs)
        from apogeebacktest.data import Market
        self.__market = Market()
        self._code = code
        self._name = self.__market.getName(self._code)


    @property
    def code(self):
        """Stock code. Should be unique."""
        return self._code


    @code.setter
    def code(self, value:str):
        self._code = value


    @property
    def name(self):
        """Stock name."""
        return self._name


    @name.setter
    def name(self, value:str):
        self._name = value


    @name.deleter
    def name(self):
        del self._name


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
        return self.__market.getReturn(self._code, date)
