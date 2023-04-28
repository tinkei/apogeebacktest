from apogeebacktest.strategies import MarketStrategy
from apogeebacktest.tests.test_helper import init_market
init_market()


def test_MarketStrategy():

    strategy = MarketStrategy()
    strategy.evalStrategy()


if __name__ == "__main__":

    test_MarketStrategy()
