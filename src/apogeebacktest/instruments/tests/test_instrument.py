from apogeebacktest.instruments import Instrument


def test_Instrument():

    try:
        instrument = Instrument() # Nothing to do.
    except Exception as e:
        assert type(e).__name__ == 'TypeError'
        # TypeError: Can't instantiate abstract class Instrument with abstract method


if __name__ == "__main__":

    test_Instrument()
