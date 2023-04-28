import numpy as np
from pathlib import Path

from apogeebacktest.data import Market
from apogeebacktest.tests.test_helper import init_market
init_market()


def test_Market():

    # Test singleton `__call__()` successfully overridden.
    market = Market()

    # Test switching data source.
    # resources_folder = (Path(__file__) / '../../../resources' ).resolve()
    # data_path = resources_folder / 'dataset.xlsx'

    # Test correctly reading reference data.
    assert market.getTimeframe()[10] == '20001031'
    assert market.getInstruments()[10] == '11'
    assert market.getName(123) == 'Stock 123'
    assert market.getType(123).__name__ == 'Stock'
    assert np.isclose(market.getData('returns', 123, '20001031'), 0.000464188132401866)
    assert np.isclose(market.getData('bpratio', 123, '20001031'), 0.0561641080855793)


if __name__ == "__main__":

    test_Market()
