"""A thin wrapper over a pandas.DataFrame instance."""
import pathlib
import numpy as np
import pandas as pd
from typing import Any, Optional, Callable, Tuple, Dict

from apogeebacktest.data import Connector


class PandasXLSXConnector(Connector):
    """A thin wrapper over a `pandas.DataFrame` instance."""

    def __init__(self, name:str, load_func:Callable, func_args:Dict[str,Any], **kwargs) -> None:
        """Constructor.

        Parameters
        ----------
        name : str
            The name of the connector. Must be unique within a `Market`.
        load_func : Callable
            User-defined function to parse their custom `.xlsx` file into `pandas.DataFrame`.
        func_args : Dict[str,Any]
            Arguments to the aforementioned user-defined function.
        """
        super(PandasXLSXConnector, self).__init__(name, **kwargs)
        self._loadDataFrame = load_func
        self.__df, self.__data_path = self._loadDataFrame(**func_args)


    @staticmethod
    def _loadDataFrame(data_path:pathlib.Path, sheet_name:Optional[str]=None) -> Tuple[pd.DataFrame, pathlib.Path]:
        """User-injected custom processing logic to parse your particular Excel file.

        Load a `.xlsx` data source into pandas.DataFrame.
        Indices are stock code, and columns are date.
        This is a reference implementation.
        This function is replaced upon `__init__` and is never called.

        Parameters
        ----------
        data_path : pathlib.Path
            Path to the data file.
        sheet_name : str
            Name of the excel sheet.

        Returns
        -------
        Tuple[pd.DataFrame, pathlib.Path]
            The parsed dataframe and the path to the data source.
        """
        raise NotImplementedError

        df = pd.read_excel(data_path, sheet_name=sheet_name, index_col=0)
        df.index = [name.split(' ')[1] for name in df.index]
        df.index = df.index.astype(int)
        df.sort_index(inplace=True)
        df.columns = df.columns.astype(str)
        return df, data_path


    def switchDataFrame(self, func_args) -> None:
        """Switch to another `.xlsx` data source.

        Not implemented because it will break the cache in `Market`.

        Parameters
        ----------
        func_args : Dict[str,Any]
            Arguments to the user-defined `_loadDataFrame()` function.
        """
        raise NotImplementedError
        self.__df, self.__data_path = self._loadDataFrame(**func_args)


    def getDataPath(self) -> pathlib.Path:
        """Get file path to current data source.

        Returns
        -------
        pathlib.Path
            The file path to the data source."""
        return self.__data_path


    def getTimeframe(self) -> np.ndarray:
        """Get the complete trading timeframe available in the market.

        Returns
        -------
        np.array
            An array of dates.
        """
        return self.__df.columns.to_numpy()


    def getInstruments(self) -> np.ndarray:
        """Get the complete list of tradable instruments in the market.

        Returns
        -------
        np.array
            List of tradable stock codes.
        """
        return self.__df.index.astype(str).to_numpy()


    def getData(self, code:str, date:Any) -> float:
        """Get the data of an instrument given its listed code and trading day.

        Parameters
        ----------
        code : str
            Instrument's listed code.
        date : any
            Date to evaluate return.

        Returns
        -------
        float
            Data point
        """
        return self.__df.loc[int(code), date]
