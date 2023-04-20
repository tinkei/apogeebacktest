"""A singleton module of the entire market of all tradeable instruments and their price data."""
from typing import Any, Optional, List

import numpy as np
import pandas as pd
from pathlib import Path
from functools import lru_cache

from apogeebacktest.instruments import Instrument, Stock


class __Market:
    """A class of the entire market of all tradeable instruments and their price data."""

    def __init__(self):
        
        # dataset_filename = 'CaseStudy/dataset.xlsx'
        resources_path = (Path(__file__) / '../../resources' ).resolve()
        data_file_path = (resources_path / 'dataset.xlsx').resolve()
        self.__data_file_path = data_file_path
        self._loadPandasDataFrame(data_file_path)


    def __call__(self):
        return self


    def switchDataSource(self, path:str) -> None:
        """Switch to another `.xlsx` data source.

        Parameters
        ----------
        path : str
            Path to the data file.
        """

        data_file_path = Path(path).resolve()
        self.__data_file_path = data_file_path.resolve()
        self._loadPandasDataFrame(data_file_path)
        self._clearCaches()


    def _loadPandasDataFrame(self, data_file_path:str) -> None:
        """Load a `.xlsx` data source into pandas.DataFrame.

        Parameters
        ----------
        data_file_path : str
            Path to the data file.
        """

        data_bp = pd.read_excel(data_file_path, sheet_name='Book to price', index_col=0)
        data_bp.index = [name.split(' ')[1] for name in data_bp.index]
        data_bp.index = data_bp.index.astype(int)
        data_bp.sort_index(inplace=True)
        data_bp.columns = data_bp.columns.astype(str)
        self.__data_bp = data_bp

        data_re = pd.read_excel(data_file_path, sheet_name='Return', index_col=0)
        data_re.index = [name.split(' ')[1] for name in data_re.index]
        data_re.index = data_re.index.astype(int)
        data_re.sort_index(inplace=True)
        data_re.columns = data_re.columns.astype(str)
        self.__data_re = data_re


    def _clearCaches(self) -> None:
        """Clear cache for all functions with `lru_cache` decorator."""
        self.getTimeframe.cache_clear()
        self.getInstruments.cache_clear()
        self.getName.cache_clear()
        self.getType.cache_clear()
        self.getReturn.cache_clear()
        self.getBP.cache_clear()


    def getDataFilePath(self) -> Path:
        """Get file path of current data source."""
        return self.__data_file_path


    @lru_cache(maxsize=1)
    def getTimeframe(self) -> np.ndarray:
        """Get the complete trading timeframe available in the market.

        Returns
        -------
        np.array
            An array of dates.
        """
        return self.__data_re.columns.to_numpy()


    @lru_cache(maxsize=1)
    def getInstruments(self) -> np.ndarray:
        """Get the complete list of tradable instruments in the market.

        Returns
        -------
        np.array
            List of tradable stock codes.
        """
        return self.__data_re.index.astype(str).to_numpy()


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
    def getType(self, code:str) -> Instrument:
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
            Return
        """
        return self.__data_re.loc[int(code), date]


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
        return self.__data_bp.loc[int(code), date]


# Singleton.
Market = __Market()
"""A singleton instance of the entire market of all tradeable instruments and their price data."""
