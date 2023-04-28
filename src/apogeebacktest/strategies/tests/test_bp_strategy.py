from apogeebacktest.strategies import BestBPStrategy, WorstBPStrategy, LongShortBPStrategy
from apogeebacktest.tests.test_helper import init_market
init_market()


def test_BestBPStrategy():

    strategy = BestBPStrategy()
    strategy.evalStrategy()


def test_WorstBPStrategy():

    strategy = WorstBPStrategy()
    strategy.evalStrategy()


def test_LongShortBPStrategy():

    strategy = LongShortBPStrategy()
    strategy.evalStrategy()


if __name__ == "__main__":

    test_BestBPStrategy()
    test_WorstBPStrategy()
    test_LongShortBPStrategy()
