import numpy as np

from apogeebacktest.signals import WorstBPSignal


def test_WorstBPSignal():

    signal = WorstBPSignal()
    assert signal.getSignal('20001031')[7][0] == '232'
    assert np.isclose(signal.getSignal('20001031')[7][1], -0.0507256296296296)


if __name__ == "__main__":

    test_WorstBPSignal()
