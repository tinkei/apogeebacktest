import matplotlib.pyplot as plt
from itertools import accumulate
from typing import Any, Optional, Tuple, List, Dict

from apogeebacktest.strategies import Strategy


def prod(cum, r):
    return cum*(1+r)


def plot_performance(output_path:str, strategies:List[Tuple[str,Strategy]], all_timeframe:Dict[str,List[Any]], all_returns:Dict[str,List[float]], all_log_returns:Dict[str,List[float]]):

    fig, axes = plt.subplots(2, 2, figsize=(1600/100, 1000/100), dpi=100)
    ((ax1, ax2), (ax3, ax4)) = axes

    ax1.set_title('Monthly Geometric Return Over Time')
    ax1.axhline(0, ls='dotted', c='gray', alpha=0.5)
    ax1.set_xlabel('#Months from starting period')
    ax1.set_ylabel('Monthly Geometric Return')
    for strategy, returns in all_returns.items():
        if strategy == 'MarketStrategy':
            ax1.plot(returns[1:], ls='--', c='black', alpha=0.5, label=strategy)
        else:
            ax1.plot(returns, label=strategy)
    ax1.legend()

    ax2.set_title('Portfolio Value Over Time')
    ax2.axhline(1, ls='dotted', c='gray', alpha=0.5)
    ax2.set_xlabel('#Months from starting period')
    ax2.set_ylabel('Monthly Geometric Return')
    for strategy, returns in all_returns.items():
        if strategy == 'MarketStrategy':
            cum_returns = list(accumulate(returns[1:], func=prod, initial=1))
            ax2.plot(cum_returns, ls='--', c='black', alpha=0.5, label=strategy)
        else:
            cum_returns = list(accumulate(returns, func=prod, initial=1))
            ax2.plot(cum_returns, label=strategy)
    ax2.legend()

    ax3.set_title('Distribution of Monthly Geometric Returns')
    ax3.axvline(0, ls='dotted', c='gray', alpha=0.5)
    ax3.set_xlabel('Monthly Geometric Return')
    ax3.set_ylabel('Count')
    for strategy, returns in all_returns.items():
        if strategy == 'MarketStrategy':
            ax3.hist(returns[1:], color='black', alpha=0.5, label=strategy)
        else:
            ax3.hist(returns, alpha=0.7, label=strategy)
    ax3.legend()

    ax4.set_title('Distribution of Monthly Log Returns')
    ax4.axvline(0, ls='dotted', c='gray', alpha=0.5)
    ax4.set_xlabel('Monthly Log Return')
    ax4.set_ylabel('Count')
    for strategy, returns in all_log_returns.items():
        if strategy == 'MarketStrategy':
            ax4.hist(returns[1:], color='black', alpha=0.5, label=strategy)
        else:
            ax4.hist(returns, alpha=0.7, label=strategy)
    ax4.legend()

    strategies_str = ''
    for strategy in strategies:
        strategies_str += strategy[0] + '-'
    strategies_str = strategies_str[:-1]

    fig.savefig(f'{output_path}/Performance-of-{strategies_str}.jpg', dpi=fig.dpi, bbox_inches='tight', pil_kwargs={'quality':75}, facecolor=fig.get_facecolor())
    plt.close(fig)
