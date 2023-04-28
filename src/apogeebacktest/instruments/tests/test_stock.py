import numpy as np

from apogeebacktest.instruments import Stock
from apogeebacktest.tests.test_helper import init_market
init_market()


def test_Stock():

    instrument = Stock('120')
    instrument.multiplier = 2
    instrument.code
    instrument.name
    instrument.name = 'Hello Stock'
    del instrument.name
    instrument.code = '123'
    assert np.isclose(instrument.getReturn('20001031'), 0.000464188132401866)


if __name__ == "__main__":

    test_Stock()
