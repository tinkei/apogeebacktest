import numpy as np

from apogeebacktest.signals import BestBPSignal
from apogeebacktest.tests.test_helper import init_market
init_market()


def test_BestBPSignal():

    signal = BestBPSignal()
    assert signal.getSignal('20001031')[7][0] == '164'
    assert np.isclose(signal.getSignal('20001031')[7][1], 2.31565670259347)


if __name__ == "__main__":

    test_BestBPSignal()
