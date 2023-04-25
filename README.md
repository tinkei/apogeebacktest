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
   or `python -m build` then `pip install -U dist/apogeebacktest-0.0.3-py3-none-any.whl --force-reinstall`


## How-to

In a project one can extend the base `Strategy` and evaluate the result as follow:

```python
import numpy as np
from apogeebacktest.strategies import MarketStrategy, LongShortBPStrategy
from apogeebacktest.utils import GeomReturn, LogReturn
from apogeebacktest.risks import VaR, CVaR

baseline = MarketStrategy()
strategy = LongShortBPStrategy()
timeframe_base, geom_returns_base, log_returns_base = baseline.evalStrategy()
timeframe_lsbp, geom_returns_lsbp, log_returns_lsbp = strategy.evalStrategy()

print(f'Performance of baseline market portfolio')
print(f'Average log return    : {LogReturn.averageOverTime(log_returns_base):+.6f}')
print(f'Average volatility    : {LogReturn.volatility(log_returns_base):+.6f}')
print(f'Value at Risk (log)   : {VaR.eval(log_returns_base):+.6f}')
print(f'Conditional VaR (log) : {CVaR.eval(log_returns_base):+.6f}')

print(f'Performance of long-short strategy based on book-to-price ratio')
print(f'Average log return    : {LogReturn.averageOverTime(log_returns_lsbp):+.6f}')
print(f'Average volatility    : {LogReturn.volatility(log_returns_lsbp):+.6f}')
print(f'Value at Risk (log)   : {VaR.eval(log_returns_lsbp):+.6f}')
print(f'Conditional VaR (log) : {CVaR.eval(log_returns_lsbp):+.6f}')
```

```none
>>> Performance of baseline market portfolio
>>> Average log return    : +0.007678
>>> Average volatility    : +0.056428
>>> Value at Risk (log)   : -0.101199
>>> Conditional VaR (log) : -0.115912
>>> Performance of long-short strategy based on book-to-price ratio
>>> Average log return    : +0.006820
>>> Average volatility    : +0.066007
>>> Value at Risk (log)   : -0.073275
>>> Conditional VaR (log) : -0.167792
```

Or execute a strategy directly through CLI:

`apogeebacktest LongShortBPStrategy MarketStrategy -v`, using default dataset.

`apogeebacktest LongShortBPStrategy MarketStrategy -v --data path/to/dataset.xlsx`

A plot summarizing the performance will be created at `./backtest-output/Performance-of-... .jpg`


## Under the hood

A `Market` connects to a data source (currently only the sample `.xlsx` file) to obtain various information about an `Instrument` (e.g. its return and book-to-price ratio).

A (user-implemented subclass of) `Strategy` makes long and/or short trades in a `Market`. The selection of `Instrument`s to buy/sell in a `Portfolio` over time is based on a set of trading `Signal`s (a.k.a. _Attractiveness Score_), each of which is composed of a set of `Indicator`s (e.g. book-to-price ratio) computed from `Market` data.

Thereafter, `Strategy().evalStrategy()` is called to evaluate the portfolio performance, based on the defined `Strategy`, over the entire timeframe available in the `Market`, minus the "warm up" period required to compute a `Signal`. The resulting timeframe, geometric return, and log return, are _returned_ by the function call for postprocessing. For example, summary statistics can be computed, and charts can be plotted.


## Thought process

The long-short strategy was first replicated using Jupyter Notebook `CaseStudy-v1-ExploreData.ipynb`.
Then the project backbone was ported from my previous works (CLI, CI/CD, build script, tests, directory structure).
I then designed the architecture to decouple the framework into four components:
* Data I/O;
* Portfolio management;
* Strategy implementation; and
* Postprocessing (plotting).

With a soft 4-hour limit, I focused on creating the `Strategy` components to maximize reusability.
Steps that were often reused were grouped together into a base class.
The composite pattern could in principle be used, but was not explicitly implemented.

Next, a `Portfolio` class was implemented to keep track of the current holdings.
Algorithms for computing returns were implmented both as static methods and using the method chaining.
The latter was done to simplify reduction over portfolio returns and returns over time, and the conversion between geometric returns and logarithmic returns.

The data I/O was abstracted to hide behind a `Market` singleton interface, with the data sources passed during construction through `Connector` objects (mentioned, but not implemented).

Finally, the plotting was implemented as a helper function.
It used `matplotlib`'s OOP `subplots` implentation instead of plotting imperatively with `pyplot`.

Unit tests focused primarily on the `Returns` and `RiskMetric` classes, as analytical solutions could easily be found and asserted.
Other tests were either asserting lookup values from the sample data, or 'integration' (if a code runs).


## To do

- [x] Test calculation of returns.
- [x] Parallelize `Strategy` evaluation in `main.py`.
- [x] Decouple `Market` from `pandas.DataFrame`.
- [ ] Recover lost vectorization from OOP abstraction.
- [ ] Refactor `date` from `str` to a real `datetime` object.
- [ ] Use `logging` library instead of `print` statements.
- [ ] Persist results of `Strategy` evaluation.
- [ ] Fix potential race condition when switching data sources.
- [ ] Add MC simulation to compute VaR based on backtest statistics.


## Feedbacks

- [ ] Use dependency injection in `Market` class. User inject a `Connector`.
- [ ] Test the strategies! Do it by hand or something.
- [ ] Test `Portfolio`. See? Bug in constructor.
- [x] Add superclass `BPStrategy`.
- [ ] Call superclass constructor when necessary.
- [x] Mutables in constructor default arguments are instantiated only once! Subsequent instances will be sharing the same object! Use `None` and put the instantiation inside the constructor.
- [ ] `WorstBPStrategy` should also be long-only. It is only shorted in the long-short strategy.
