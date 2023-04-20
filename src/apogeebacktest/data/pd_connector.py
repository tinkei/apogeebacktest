"""A thin wrapper over a pandas.DataFrame instance."""
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Any, Optional, List

from apogeebacktest.instruments import Instrument, Stock


class PandasXLSXConnector:
    """A thin wrapper over a pandas.DataFrame instance."""

    def __init__(self, data_path:str, sheet_name:Optional[str]=None):
        self.__data_path = data_path
        self._loadDataFrame(data_path, sheet_name)


    def _loadDataFrame(self, data_path:str, sheet_name:Optional[str]=None) -> None:
        """Load a `.xlsx` data source into pandas.DataFrame.

        Parameters
        ----------
        data_path : str
            Path to the data file.
        sheet_name : str
            Name of the excel sheet.
        """

        df = pd.read_excel(data_path, sheet_name=sheet_name, index_col=0)
        df.index = [name.split(' ')[1] for name in df.index]
        df.index = df.index.astype(int)
        df.sort_index(inplace=True)
        df.columns = df.columns.astype(str)
        self.__df = df


    def switchDataSource(self, data_path:str, sheet_name:Optional[str]=None) -> None:
        """Switch to another `.xlsx` data source.

        Parameters
        ----------
        data_path : str
            Path to the data file.
        sheet_name : str
            Name of the excel sheet.
        """

        data_path = Path(data_path).resolve()
        self.__data_path = data_path
        self._loadDataFrame(data_path, sheet_name)


    def getDataPath(self) -> Path:
        """Get file path to current data source."""
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
            Return
        """
        return self.__df.loc[int(code), date]
