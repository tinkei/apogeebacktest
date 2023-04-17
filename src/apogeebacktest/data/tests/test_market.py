import numpy as np
from pathlib import Path

from apogeebacktest.data import Market


def test_Market():

    # Test singleton `__call__()` successfully overridden.
    market = Market()

    # Test switching data source.
    resources_path = (Path(__file__) / '../../../resources' ).resolve()
    data_file_path = resources_path / 'dataset.xlsx'
    market.switchDataSource(data_file_path)
    assert data_file_path == market.getDataFilePath()

    # Test correctly reading reference data.
    assert market.getTimeframe()[10] == '20001031'
    assert market.getInstruments()[10] == '11'
    assert market.getName(123) == 'Stock 123'
    assert market.getType(123).__name__ == 'Stock'
    assert np.isclose(market.getReturn(123, '20001031'), 0.000464188132401866)
    assert np.isclose(market.getBP(123, '20001031'), 0.0561641080855793)


if __name__ == "__main__":

    test_Market()
