import pytest
import pathlib
import pandas as pd
from typing import Optional, Tuple

from apogeebacktest.data import Market, Connector, PandasXLSXConnector


def load_dataframe(data_path:pathlib.Path, sheet_name:Optional[str]=None) -> Tuple[pd.DataFrame, pathlib.Path]:
    """User-injected custom processing logic to parse your particular Excel file.

    Load a `.xlsx` data source into pandas.DataFrame.
    Indices are stock code, and columns are date.

    Parameters
    ----------
    data_path : pathlib.Path
        Path to the data file.
    sheet_name : str
        Name of the Excel sheet.

    Returns
    -------
    Tuple[pd.DataFrame, pathlib.Path]
        The parsed dataframe and the path to the data source.
    """
    df = pd.read_excel(data_path, sheet_name=sheet_name, index_col=0)
    df.index = [name.split(' ')[1] for name in df.index]
    df.index = df.index.astype(int)
    df.sort_index(inplace=True)
    df.columns = df.columns.astype(str)
    return df, data_path


# @pytest.fixture(scope='session')
def init_market():
    if not Market.hasDataSource():
        resources_folder = (pathlib.Path(__file__) / '../../resources' ).resolve()
        data_path = (resources_folder / 'dataset.xlsx').resolve()
        returns_source = PandasXLSXConnector('returns', load_dataframe, {'data_path': data_path, 'sheet_name': 'Return'})
        bpratio_source = PandasXLSXConnector('bpratio', load_dataframe, {'data_path': data_path, 'sheet_name': 'Book to price'})
        Market.addDataSource(returns_source)
        Market.addDataSource(bpratio_source)
