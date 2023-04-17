import pathlib
import tempfile

import apogeebacktest
from apogeebacktest.strategies import MarketStrategy, LongShortBPStrategy
from apogeebacktest.utils import plot_performance


def test_Plots():

    all_timeframe = {}
    all_returns = {}
    all_log_returns = {}
    strategies_to_execute = (('MarketStrategy', MarketStrategy), ('LongShortBPStrategy', LongShortBPStrategy))

    for strategy in strategies_to_execute:
        timeframe, returns, log_returns = strategy[1]().evalStrategy()
        all_timeframe[strategy[0]] = timeframe
        all_returns[strategy[0]] = returns
        all_log_returns[strategy[0]] = log_returns

    temp_path = tempfile.TemporaryDirectory(prefix=f'{apogeebacktest.__name__}-')
    output_path = pathlib.Path(temp_path.name)
    plot_performance(output_path, strategies_to_execute, all_timeframe, all_returns, all_log_returns)
    assert (output_path/'Performance-of-MarketStrategy-LongShortBPStrategy.jpg').is_file()
    assert (output_path/'Performance-of-MarketStrategy-LongShortBPStrategy.jpg').suffix == '.jpg'


if __name__ == "__main__":

    test_Plots()
