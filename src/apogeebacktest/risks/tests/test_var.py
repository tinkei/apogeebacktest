import numpy as np
from apogeebacktest.risks import VaR


def test_VaR_eval():
    a = np.arange(1,101)
    np.random.shuffle(a) # In-place.
    assert VaR.eval(a, 0.50) == 50.5
    assert VaR.eval(a, 0.25) == 25.75
    assert VaR.eval(a, 0.05) == 5.95


if __name__ == "__main__":

    test_VaR_eval()
