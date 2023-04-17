"""A singleton module of the entire market of all tradeable instruments and their price data."""
from typing import Any, Optional, List

import numpy as np
import pandas as pd
from pathlib import Path

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


    def switchDataSource(self, path:str):

        data_file_path = Path(path).resolve()
        self.__data_file_path = data_file_path.resolve()
        self._loadPandasDataFrame(data_file_path)


    def _loadPandasDataFrame(self, data_file_path:str):

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


    def getDataFilePath(self) -> Path:
        return self.__data_file_path


    def getTimeframe(self) -> np.ndarray:
        return self.__data_re.columns.to_numpy()


    def getInstruments(self) -> np.ndarray:
        return self.__data_re.index.astype(str).to_numpy()


    def getName(self, code:str) -> str:
        return f'Stock {code}'


    def getType(self, code:str) -> Instrument:
        return Stock


    def getReturn(self, code:str, date:Any) -> float:
        return self.__data_re.loc[int(code), date]


    def getBP(self, code:str, date:Any) -> float:
        return self.__data_bp.loc[int(code), date]


# Singleton.
Market = __Market()
"""A singleton instance of the entire market of all tradeable instruments and their price data."""
