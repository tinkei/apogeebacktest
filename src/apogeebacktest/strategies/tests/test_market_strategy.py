from apogeebacktest.strategies import MarketStrategy


def test_MarketStrategy():

    strategy = MarketStrategy()
    strategy.evalStrategy()


if __name__ == "__main__":

    test_MarketStrategy()
