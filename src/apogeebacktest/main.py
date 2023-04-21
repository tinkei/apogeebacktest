#!/usr/bin/env python
"""Entrypoint of the module."""

import sys
import inspect
import argparse
import pathlib
import numpy as np
from multiprocessing import Pool
from typing import Optional, List, Tuple

import apogeebacktest.strategies
from apogeebacktest.data import Market
from apogeebacktest.risks import VaR, CVaR
from apogeebacktest.utils import plot_performance
from apogeebacktest.utils import GeomReturn, LogReturn
from apogeebacktest.strategies import Strategy


def parse_arguments(args:List[str]) -> argparse.Namespace:
    """Parse command-line arguments and return the attributes.

    Parameters
    ----------
    args : List
        Arguments

    Returns
    -------
    argparse.Namespace
        Simple object holding the attributes as fields.
    """
    parser = argparse.ArgumentParser(
        description='A backtest package for a long-short strategy using book-to-price ratio.'
    )
    parser.add_argument(
        'strategies',
        metavar='strats',
        type=str, nargs='+',
        help='Backtest an investment strategy. E.g. MarketStrategy, BestBPStrategy, WorstBPStrategy, LongShortBPStrategy etc.'
    )
    parser.add_argument(
        '-o',
        '--output-path',
        type=str,
        default='backtest-output',
        help='Output plots as images. Default: "backtest-output".'
    )
    parser.add_argument(
        '-d',
        '--data',
        type=str,
        help='Specify input data directory. Default: None.'
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true'
    )
    return parser.parse_args(args)


def parallel_eval(strategy_name:str, strategy_instance:Strategy) -> Tuple[np.array, np.array, np.array]:
    """Wrapper for `multiprocessing.Pool.apply_async()`."""
    return strategy_instance.evalStrategy()


def main_cli(args:Optional[List[str]]=None):
    """Entry point of the module."""

    if args is None:
        args = parse_arguments(sys.argv[1:])
    else:
        args = parse_arguments(args)

    if args.verbose:
        print('Input arguments:')
        print(args)

    if args.verbose:
        print('==============================')
        print('=====   Apogee Backtest  =====')
        print('==============================')
        print('                              ')

    if args.data is not None:
        if args.verbose:
            print(f'Setting data source to {args.data}')
        Market.switchReturnsDataSource(args.data)
        Market.switchBookToPriceDataSource(args.data)
    if args.verbose:
        print(f'Current data source: {Market.getDataPath()}\n')

    if args.verbose:
        print('Going to backtest the following strategies:')
    strategies_to_execute = []
    # inspect.getmembers(): ('NAME_OF_CLASS', 'CLASS')
    strategies = inspect.getmembers(apogeebacktest.strategies, lambda member: inspect.isclass(member) and member.__module__.split('.')[-1] != 'strategy')
    strategies = dict(strategies)
    for strategy in args.strategies: 
        if strategy in strategies.keys():
            if args.verbose:
                print(strategy)
            strategies_to_execute.append((strategy, strategies[strategy]))
    if args.verbose:
        print('')

    all_timeframe = {}
    all_returns = {}
    all_log_returns = {}

    with Pool(processes=min(8, len(strategies_to_execute))) as pool:
        strategies_executed = [pool.apply_async(parallel_eval, (strategy[0], strategy[1]())) for strategy in strategies_to_execute]
        for strategy, res in zip(strategies_to_execute, strategies_executed):
            # timeframe, geom_returns, log_returns = strategy[1]().evalStrategy()
            timeframe, geom_returns, log_returns = res.get()
            all_timeframe[strategy[0]] = timeframe
            all_returns[strategy[0]] = geom_returns
            all_log_returns[strategy[0]] = log_returns
            print(f'Backtest summary of {strategy[0]} (monthly values)')
            print(f'Time range            : {timeframe[0]} to {timeframe[-1]}')
            print(f'Average geom return   : {GeomReturn.averageOverTime(geom_returns):+.6f}')
            print(f'Average log return    : {LogReturn.averageOverTime(log_returns):+.6f}')
            print(f'Average volatility    : {LogReturn.volatility(log_returns):+.6f}')
            print(f'Value at Risk (log)   : {VaR.eval(log_returns):+.6f}')
            print(f'Conditional VaR (log) : {CVaR.eval(log_returns):+.6f}')
            print('')

    pathlib.Path(args.output_path).mkdir(parents=True, exist_ok=True)
    plot_performance(args.output_path, strategies_to_execute, all_timeframe, all_returns, all_log_returns)

    if args.verbose:
        print('                              ')
        print('==============================')
        print('=====   End of program   =====')
        print('==============================')



if __name__ == "__main__":

    main_cli(['-v', 'LongShortBPStrategy', 'WorstBPStrategy', 'BestBPStrategy', 'MarketStrategy'])
