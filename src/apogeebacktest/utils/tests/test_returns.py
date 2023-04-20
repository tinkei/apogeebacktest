import numpy as np
from functools import reduce

from apogeebacktest.utils import GeomReturn, LogReturn


def test_Returns_static():
    """Test a fixed portfolio that does not rebalance."""

    # Portfolio of 10 stocks over 50 time periods.
    # geom_returns = np.random.uniform(-0.05, 0.05, size=(50,10))
    # log_returns = GeomReturn.toLogReturn(geom_returns)
    log_returns = np.random.randn(50,10)
    geom_returns = LogReturn.toGeomReturn(log_returns)
    weights = np.ones_like(geom_returns[0,:]) / len(geom_returns[0,:])
    assert weights.shape == (10,)

    # Assert conversion between geometric and logarithmic returns.
    assert np.allclose(geom_returns, LogReturn.toGeomReturn(GeomReturn.toLogReturn(geom_returns)))
    assert np.allclose(log_returns,  GeomReturn.toLogReturn(LogReturn.toGeomReturn(log_returns)))
    assert np.allclose(geom_returns, GeomReturn(geom_returns).toLogReturn().toGeomReturn().result())
    assert np.allclose(log_returns,  LogReturn(log_returns).toGeomReturn().toLogReturn().result())

    # Assert equivalent implementation with and without weights.
    assert np.allclose(GeomReturn.averageOverPortfolio(geom_returns), GeomReturn.averageOverPortfolio(geom_returns, weights))
    assert np.allclose(LogReturn.averageOverPortfolio(log_returns), LogReturn.averageOverPortfolio(log_returns, weights))
    assert np.allclose(GeomReturn.averageOverPortfolio(geom_returns), LogReturn.toGeomReturn(LogReturn.averageOverPortfolio(log_returns)))

    # Assert numpy.ufunc.reduce behaves identically to reduce for 1D case.
    assert GeomReturn.averageOverTime(geom_returns[0,:]) == np.power(reduce(lambda R_cum, r: R_cum * (1+r), geom_returns[0,:], 1), 1/len(geom_returns[0,:])) - 1

    # Assert compounding returns over both portfolio and time.
    # The following two implementations are NOT equivalent! Not even for an "equal-weight" portfolio!
    # If I reduce over time first, I hold the same number of shares for each stock as I do at the beginning, till the end of time.
    time_first = GeomReturn.averageOverPortfolio(GeomReturn.compoundOverTime(geom_returns), weights, portfolio_axis=0)
    # However, if I average over portfolio first, I rebalance the portfolio to equal-weight EVERY SINGLE TIME STEP!
    port_first = GeomReturn.compoundOverTime(GeomReturn.averageOverPortfolio(geom_returns, weights, portfolio_axis=1))
    # assert np.allclose(time_first, port_first) # False!
    # Therefore, given only an 1D portfolio weights (without time dependence), the user must specify the desired behavior.
    # The default is to reduce over time first, i.e. WITHOUT rebalancing.

    # Assert alternate implementations.
    mixed_time_first = GeomReturn.toLogReturn(geom_returns)
    mixed_time_first = LogReturn.compoundOverTime(mixed_time_first, portfolio_axis=1)
    mixed_time_first = LogReturn.toGeomReturn(mixed_time_first)
    mixed_time_first = GeomReturn.averageOverPortfolio(mixed_time_first, weights, portfolio_axis=0)
    assert np.allclose(time_first, mixed_time_first)
    assert np.allclose(time_first, GeomReturn(geom_returns).toLogReturn().compoundOverTime(portfolio_axis=1).toGeomReturn().averageOverPortfolio(weights, portfolio_axis=0).result())
    mixed_port_first = GeomReturn.averageOverPortfolio(geom_returns, weights, portfolio_axis=1)
    mixed_port_first = GeomReturn.toLogReturn(mixed_port_first)
    mixed_port_first = LogReturn.compoundOverTime(mixed_port_first)
    mixed_port_first = LogReturn.toGeomReturn(mixed_port_first)
    assert np.allclose(port_first, mixed_port_first)
    assert np.allclose(port_first, GeomReturn(geom_returns).averageOverPortfolio(weights, portfolio_axis=1).toLogReturn().compoundOverTime().toGeomReturn().result())

    # Assert composite implementation.
    time_first_1d = GeomReturn.compoundOverPortfolioAndTime(geom_returns, weights, portfolio_axis=1)
    assert np.allclose(time_first, time_first_1d)

    # Do the same for accumulate.
    time_first = GeomReturn.averageOverPortfolio(GeomReturn.accumulateOverTime(geom_returns), weights, portfolio_axis=1)
    port_first = GeomReturn.accumulateOverTime(GeomReturn.averageOverPortfolio(geom_returns, weights, portfolio_axis=1))
    mixed_time_first = GeomReturn.toLogReturn(geom_returns)
    mixed_time_first = LogReturn.accumulateOverTime(mixed_time_first, portfolio_axis=1)
    mixed_time_first = LogReturn.toGeomReturn(mixed_time_first)
    mixed_time_first = GeomReturn.averageOverPortfolio(mixed_time_first, weights, portfolio_axis=1)
    assert np.allclose(time_first, mixed_time_first)
    assert np.allclose(time_first, GeomReturn(geom_returns).toLogReturn().accumulateOverTime(portfolio_axis=1).toGeomReturn().averageOverPortfolio(weights, portfolio_axis=1).result())
    mixed_port_first = GeomReturn.averageOverPortfolio(geom_returns, weights, portfolio_axis=1)
    mixed_port_first = GeomReturn.toLogReturn(mixed_port_first)
    mixed_port_first = LogReturn.accumulateOverTime(mixed_port_first, portfolio_axis=1)
    mixed_port_first = LogReturn.toGeomReturn(mixed_port_first)
    assert np.allclose(port_first, mixed_port_first)
    assert np.allclose(port_first, GeomReturn(geom_returns).averageOverPortfolio(weights, portfolio_axis=1).toLogReturn().accumulateOverTime(portfolio_axis=1).toGeomReturn().result())
    time_first_1d = GeomReturn.accumulateOverPortfolioAndTime(geom_returns, weights, portfolio_axis=1)
    assert np.allclose(time_first, time_first_1d)


def test_Returns_dynamic():
    """Test a portfolio that rebalances every time step."""

    # Portfolio of 10 stocks over 50 time periods.
    geom_returns = np.random.uniform(-0.05, 0.05, size=(50,10))
    log_returns = GeomReturn.toLogReturn(geom_returns)
    weights = np.ones_like(geom_returns) / len(geom_returns[0,:])
    assert weights.shape == (50,10)
    assert weights[0,0] == 1/10

    # Assert compounding returns over both portfolio and time.
    # The following two implementations are NOT equivalent! Not even for an "equal-weight" portfolio!
    # If I reduce over time first, I hold the same number of shares for each stock as I do at the beginning, till the end of time.
    # time_first = GeomReturn.averageOverPortfolio(GeomReturn.compoundOverTime(geom_returns), weights, portfolio_axis=1)
    # However, if I average over portfolio first, I rebalance the portfolio to equal-weight EVERY SINGLE TIME STEP!
    port_first = GeomReturn.compoundOverTime(GeomReturn.averageOverPortfolio(geom_returns, weights, portfolio_axis=1))
    # assert np.allclose(time_first, port_first) # False!
    # Therefore, given only an 1D portfolio weights (without time dependence), the user must specify the desired behavior.
    # The default is to reduce over time first, i.e. WITHOUT rebalancing.

    # Assert composite implementation.
    port_first_1d = GeomReturn.compoundOverPortfolioAndTime(geom_returns, weights, portfolio_axis=1)
    assert np.allclose(port_first, port_first_1d)

    # Do the same for accumulate.
    port_first = GeomReturn.accumulateOverTime(GeomReturn.averageOverPortfolio(geom_returns, weights, portfolio_axis=1))
    port_first_1d = GeomReturn.accumulateOverPortfolioAndTime(geom_returns, weights, portfolio_axis=1)
    assert np.allclose(port_first, port_first_1d)


if __name__ == "__main__":

    test_Returns_static()
    test_Returns_dynamic()
