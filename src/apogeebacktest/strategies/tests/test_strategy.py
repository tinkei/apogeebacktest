from apogeebacktest.strategies import Strategy


def test_Strategy():

    try:
        strategy = Strategy() # Nothing to do.
    except Exception as e:
        assert type(e).__name__ == 'TypeError'
        # TypeError: Can't instantiate abstract class Strategy with abstract method


if __name__ == "__main__":

    test_Strategy()
