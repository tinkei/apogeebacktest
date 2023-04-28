import numpy as np

from apogeebacktest.indicators import BookToPriceIndicator
from apogeebacktest.tests.test_helper import init_market
init_market()


def test_BookToPriceIndicator():

    indicator = BookToPriceIndicator()
    assert np.isclose(indicator.getValue(123, '20001031'), 0.0561641080855793)


if __name__ == "__main__":

    test_BookToPriceIndicator()
