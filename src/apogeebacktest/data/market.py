"""A singleton module of the entire market of all tradeable instruments and their price data."""
from typing import Any, Optional, List, Type

import numpy as np
import pandas as pd
from pathlib import Path
from functools import lru_cache

from apogeebacktest.data import Connector, PandasXLSXConnector
from apogeebacktest.instruments import Instrument, Stock


class __Market:
    """A class of the entire market of all tradeable instruments and their price data."""

    def __init__(self, connection:List[Connector]=None, **kwargs) -> None:
        super().__init__() # Can't call `__Market`, because it gets auto-mangled into `_Market__Market`.
        
        # Load default market data.
        resources_folder = (Path(__file__) / '../../resources' ).resolve()
        data_path = (resources_folder / 'dataset.xlsx').resolve()
        self.__data_path = data_path
        self.__market_data_connector = PandasXLSXConnector(data_path, 'Return')
        self.__book_to_price_connector = PandasXLSXConnector(data_path, 'Book to price')


    def __call__(self):
        return self


    def switchReturnsDataSource(self, data_path:str) -> None:
        """Switch to another `.xlsx` data source.

        Parameters
        ----------
        data_path : str
            Path to the data file.
        """

        self.__data_path = data_path
        self.__market_data_connector = PandasXLSXConnector(data_path, 'Return')
        self._clearCaches()


    def switchBookToPriceDataSource(self, data_path:str) -> None:
        """Switch to another `.xlsx` data source.

        Parameters
        ----------
        data_path : str
            Path to the data file.
        """

        self.__data_path = data_path
        self.__book_to_price_connector = PandasXLSXConnector(data_path, 'Book to price')
        self._clearCaches()


    def _clearCaches(self) -> None:
        """Clear cache for all functions with `lru_cache` decorator."""
        self.getTimeframe.cache_clear()
        self.getInstruments.cache_clear()
        self.getName.cache_clear()
        self.getType.cache_clear()
        self.getReturn.cache_clear()
        self.getBP.cache_clear()


    def getDataPath(self) -> Path:
        """Get file path to current data source."""
        return self.__data_path


    @lru_cache(maxsize=1)
    def getTimeframe(self) -> np.ndarray:
        """Get the complete trading timeframe available in the market.

        Returns
        -------
        np.array
            An array of dates.
        """
        return self.__market_data_connector.getTimeframe()


    @lru_cache(maxsize=1)
    def getInstruments(self) -> np.ndarray:
        """Get the complete list of tradable instruments in the market.

        Returns
        -------
        np.array
            List of tradable stock codes.
        """
        return self.__market_data_connector.getInstruments()


    @lru_cache(maxsize=1000)
    def getName(self, code:str) -> str:
        """Get the name of instrument given its listed code.

        Returns
        -------
        str
            Name of instrument.
        """
        return f'Stock {code}'


    @lru_cache(maxsize=1000)
    def getType(self, code:str) -> Type['Instrument']:
        """Get the type of instrument given its listed code.

        Returns
        -------
        Instrument
            Class of the instrument.
        """
        return Stock


    @lru_cache(maxsize=10000)
    def getReturn(self, code:str, date:Any) -> float:
        """Get the return of an instrument given its listed code and trading day.

        Parameters
        ----------
        code : str
            Instrument's listed code.
        date : any
            Date to evaluate return.

        Returns
        -------
        float
            Instrument return.
        """
        return self.__market_data_connector.getData(code, date)


    @lru_cache(maxsize=10000)
    def getBP(self, code:str, date:Any) -> float:
        """Get the book-to-price ratio of an instrument given its listed code and trading day.

        Parameters
        ----------
        code : str
            Instrument's listed code.
        date : any
            Date to evaluate book-to-price ratio.

        Returns
        -------
        float
            Book-to-price ratio.
        """
        return self.__book_to_price_connector.getData(code, date)


# Singleton.
Market = __Market()
"""A singleton instance of the entire market of all tradeable instruments and their price data."""
