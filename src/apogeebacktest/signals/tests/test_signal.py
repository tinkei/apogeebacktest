from apogeebacktest.signals import Signal


def test_Signal():

    try:
        signal = Signal() # Nothing to do.
    except Exception as e:
        assert type(e).__name__ == 'TypeError'
        # TypeError: Can't instantiate abstract class Signal with abstract method


if __name__ == "__main__":

    test_Signal()
