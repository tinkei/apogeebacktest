import numpy as np
from typing import List

from apogeebacktest.risks import RiskMetric, VaR


class CVaR(RiskMetric):

    @staticmethod
    def eval(returns:List[float], q:float=0.05) -> float:
        """Compute Conditional Value at Risk (CVaR) of an array of geometric returns.

        Parameters
        ----------
        returns : List[float]
            A list of geometric returns.
        q : float
            Quantile to compute CVaR.

        Returns
        -------
        float
            Conditional Value at Risk.
        """
        # var = VaR.eval(returns, q)
        var = np.quantile(returns, q, axis=0)
        cvar = np.where(returns <= var, returns, np.nan)
        cvar = np.nanmean(cvar, axis=0)
        return cvar
