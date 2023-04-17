from apogeebacktest.instruments import Stock


def test_Stock():

    instrument = Stock('123')
    instrument.multiplier = 2


if __name__ == "__main__":

    test_Stock()
