# OOP Case Study: Backtest Framework

A backtest package for a long-short strategy using book-to-price ratio[^1].

[^1]: It is curious how the return should be calculated, given that the long-short strategy has a net zero position.


## Build and install

`cd` to the project root and run

1. `pip install -r requirements.txt`
1. `pip install -e .`  
   or `python -m build` then `pip install -U dist/apogeebacktest-0.0.1-py3-none-any.whl --force-reinstall`


## How to

Then in a project one can import like

```python
import numpy as np
from apogeebacktest.strategies import MarketStrategy, LongShortBPStrategy
from apogeebacktest.risks import VaR, CVaR

baseline = MarketStrategy()
strategy = LongShortBPStrategy()
timeframe_base, returns_base, log_returns_base = baseline.evalStrategy()
timeframe_lsbp, returns_lsbp, log_returns_lsbp = strategy.evalStrategy()

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

`apogeebacktest MarketStrategy LongShortBPStrategy -v`, using default dataset.

`apogeebacktest MarketStrategy LongShortBPStrategy -v --data CaseStudy/dataset.xlsx`


## To do

- [ ] Refactor `date` from `str` to a real `datetime` object.
- [ ] Refactor `Market`'s dependence on `DataFrame`.
- [ ] Use `logging` library instead of `print` statements.
- [ ] Parallelize `Strategy` evaluation.
- [ ] Add MC simulation to compute VaR based on backtest statistics.
