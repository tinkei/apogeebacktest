# OOP Case Study: Backtest Framework

![Workflow status - Apogee Backtest - Master branch](https://github.com/tinkei/apogeebacktest/actions/workflows/python-package.yml/badge.svg?branch=master)
![GitHub language count](https://img.shields.io/github/languages/count/tinkei/apogeebacktest)
![GitHub top language](https://img.shields.io/github/languages/top/tinkei/apogeebacktest)
![GitHub last commit](https://img.shields.io/github/last-commit/tinkei/apogeebacktest)

A backtest package for a long-short strategy using book-to-price ratio[^1].

[^1]: It is curious how the return should be calculated, given that the long-short strategy has a net zero position.


## Build and install

`cd` to the project root and run

1. `pip install -r requirements.txt`
1. `pip install -e .`  
   or `python -m build` then `pip install -U dist/apogeebacktest-0.0.2-py3-none-any.whl --force-reinstall`


## How-to

In a project one can extend the base `Strategy` and evaluate the result as follow:

```python
import numpy as np
from apogeebacktest.strategies import MarketStrategy, LongShortBPStrategy
from apogeebacktest.risks import VaR, CVaR

baseline = MarketStrategy()
strategy = LongShortBPStrategy()
timeframe_base, geom_returns_base, log_returns_base = baseline.evalStrategy()
timeframe_lsbp, geom_returns_lsbp, log_returns_lsbp = strategy.evalStrategy()

print(f'Performance of baseline market portfolio')
print(f'Average log return    : {np.mean(log_returns_base):+.6f}')
print(f'Average volatility    : {np.std(log_returns_base):+.6f}')
print(f'Value at Risk (log)   : {VaR.eval(log_returns_base):+.6f}')
print(f'Conditional VaR (log) : {CVaR.eval(log_returns_base):+.6f}')

print(f'Performance of long-short strategy based on book-to-price ratio')
print(f'Average log return    : {np.mean(log_returns_lsbp):+.6f}')
print(f'Average volatility    : {np.std(log_returns_lsbp):+.6f}')
print(f'Value at Risk (log)   : {VaR.eval(log_returns_lsbp):+.6f}')
print(f'Conditional VaR (log) : {CVaR.eval(log_returns_lsbp):+.6f}')
```

Or execute a strategy directly through CLI:

`apogeebacktest LongShortBPStrategy MarketStrategy -v`, using default dataset.

`apogeebacktest LongShortBPStrategy MarketStrategy -v --data path/to/dataset.xlsx`

A plot summarizing the performance will be created at `./backtest-output/Performance-of-... .jpg`


## Under the hood

A `Market` connects to a data source (currently only the sample `.xlsx` file) to obtain various information about an `Instrument` (e.g. its return and book-to-price ratio).

A (user-implemented subclass of) `Strategy` makes long and/or short trades in a `Market`. The selection of `Instrument`s to buy/sell in a `Portfolio` over time is based on a set of trading `Signal`s (a.k.a. _Attractiveness Score_), each of which is composed of a set of `Indicator`s (e.g. book-to-price ratio) computed from `Market` data.

Thereafter, `Strategy().evalStrategy()` is called to evaluate the portfolio performance, based on the defined `Strategy`, over the entire timeframe available in the `Market`, minus the "warm up" period required to compute a `Signal`. The resulting timeframe, geometric return, and log return, are _returned_ by the function call for postprocessing. For example, summary statistics can be computed, and charts can be plotted.


## To do

- [x] Test calculation of returns.
- [ ] Refactor `date` from `str` to a real `datetime` object.
- [ ] Refactor `Market`'s dependence on `DataFrame`.
- [ ] Use `logging` library instead of `print` statements.
- [ ] Persist results of `Strategy` evaluation.
- [x] Parallelize `Strategy` evaluation in `main.py`.
- [ ] Reenable lost vectorization from OOP abstraction.
- [ ] Add MC simulation to compute VaR based on backtest statistics.
