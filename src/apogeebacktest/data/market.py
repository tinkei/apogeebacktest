"""A singleton module of the entire market of all tradeable instruments and their price data."""
import numpy as np
from pathlib import Path
from functools import lru_cache
from typing import Any, Optional, List, Type, Dict

from apogeebacktest.data import Connector
from apogeebacktest.instruments import Instrument, Stock


class __Market:
    """A class of the entire market of all tradeable instruments and their price data."""

    def __init__(self, connectors:Optional[List[Connector]]=None, **kwargs) -> None:
        """Constructor.

        Parameters
        ----------
        connectors : List[Connector]
            A list of `Connector`s to various data sources.
        """
        super().__init__() # Can't call `__Market`, because it gets auto-mangled into `_Market__Market`.

        # Registry that contains various data source connectors.
        self.__registry:Dict[str, Connector] = {}
        if connectors is not None:
            for connector in connectors:
                self.addDataSource(connector)
        self._default_connector = 'returns' # Hardcoded for now.


    def __call__(self):
        return self


    def addDataSource(self, connector:Connector) -> None:
        """Attach a new data source.

        Parameters
        ----------
        connector : Connector
            A `Connector` object.
        """
        if connector.name in self.__registry:
            raise KeyError('Data source already registered.')
        self.__registry[connector.name] = connector


    def switchDataSource(self, connector:Connector) -> None:
        """Swap out an existing data source.

        Parameters
        ----------
        connector : Connector
            A `Connector` object.
        """
        if connector.name not in self.__registry:
            raise KeyError('Data source not registered.')
        self.__registry[connector.name] = connector
        self._clearCaches()


    def hasDataSource(self, connector_name:Optional[str]=None) -> np.ndarray:
        """Check if the data source is already registered.

        Parameters
        ----------
        connector_name : str
            The data source's name.

        Returns
        -------
        bool
            If the data source is already attached.
        """
        if connector_name is None:
            connector_name = self._default_connector
        return connector_name in self.__registry


    def _clearCaches(self) -> None:
        """Clear cache for all functions with `lru_cache` decorator."""
        self.getTimeframe.cache_clear()
        self.getInstruments.cache_clear()
        self.getName.cache_clear()
        self.getType.cache_clear()
        self.getData.cache_clear()


    @lru_cache(maxsize=2)
    def getDefaultConnectorName(self) -> str:
        """Get the name of the default `Connector`.

        Returns
        -------
        str
            The default data source's name.
        """
        return self._default_connector


    @lru_cache(maxsize=2)
    def getTimeframe(self, connector_name:Optional[str]=None) -> np.ndarray:
        """Get the complete trading timeframe available in the market.

        Parameters
        ----------
        connector_name : str
            The data source's name.

        Returns
        -------
        np.array
            An array of dates.
        """
        if connector_name is None:
            connector_name = self._default_connector
        return self.__registry[connector_name].getTimeframe()


    @lru_cache(maxsize=2)
    def getInstruments(self, connector_name:Optional[str]=None) -> np.ndarray:
        """Get the complete list of tradable instruments in the market.

        Parameters
        ----------
        connector_name : str
            The data source's name.

        Returns
        -------
        np.array
            List of tradable stock codes.
        """
        if connector_name is None:
            connector_name = self._default_connector
        return self.__registry[connector_name].getInstruments()


    @lru_cache(maxsize=1000)
    def getName(self, code:str) -> str:
        """Get the name of instrument given its listed code.

        Parameters
        ----------
        code : str
            Instrument's listed code.

        Returns
        -------
        str
            Name of instrument.
        """
        return f'Stock {code}'


    @lru_cache(maxsize=1000)
    def getType(self, code:str) -> Type['Instrument']:
        """Get the type of instrument given its listed code.

        Parameters
        ----------
        code : str
            Instrument's listed code.

        Returns
        -------
        Instrument
            Class of the instrument.
        """
        return Stock


    @lru_cache(maxsize=10000)
    def getData(self, connector_name:str, code:str, date:Any) -> float:
        """Get data point of an instrument given its listed code and trading day.

        Parameters
        ----------
        connector_name : str
            The data source's name.
        code : str
            Instrument's listed code.
        date : any
            Date to evaluate data.

        Returns
        -------
        float
            Data point.
        """
        return self.__registry[connector_name].getData(code, date)


# Singleton.
Market = __Market()
"""A singleton instance of the entire market of all tradeable instruments and their price data."""
# print(f'Memory address of Market: {id(Market)}')
