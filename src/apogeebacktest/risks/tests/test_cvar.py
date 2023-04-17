import numpy as np
from apogeebacktest.risks import CVaR


def test_VaR_eval():
    a = np.arange(1,101)
    np.random.shuffle(a) # In-place.
    assert CVaR.eval(a) == 3 # (1+2+3+4+5)/3 == 3


if __name__ == "__main__":

    test_VaR_eval()
