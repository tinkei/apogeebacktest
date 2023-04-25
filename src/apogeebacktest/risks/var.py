import numpy as np
from typing import List

from apogeebacktest.risks import RiskMetric


class VaR(RiskMetric):

    def __init__(self, **kwargs) -> None:
        super(VaR, self).__init__(**kwargs)


    @staticmethod
    def eval(returns:List[float], q:float=0.05) -> float:
        """Compute Value at Risk (VaR) of an array of returns.

        Parameters
        ----------
        returns : List[float]
            A list of returns.
        q : float
            Quantile to compute VaR.

        Returns
        -------
        float
            Value at Risk.
        """
        return np.quantile(returns, q, axis=0)
        # return sorted(returns)[:int(len(returns)*q)]
