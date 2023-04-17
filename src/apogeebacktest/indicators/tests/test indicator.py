from apogeebacktest.indicators import Indicator


def test_Indicator():

    try:
        indicator = Indicator() # Nothing to do.
    except Exception as e:
        assert type(e).__name__ == 'TypeError'
        # TypeError: Can't instantiate abstract class Indicator with abstract method


if __name__ == "__main__":

    test_Indicator()
