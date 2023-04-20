#!/usr/bin/env python

"""Primary functions of the module."""

import os
import sys
import inspect
import argparse
import pathlib
import numpy as np
from typing import List
from functools import reduce

# import apogeebacktest
import apogeebacktest.strategies
from apogeebacktest.data import Market
from apogeebacktest.risks import VaR, CVaR
from apogeebacktest.utils import plot_performance


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


def main_cli(args=None):
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
        Market.switchDataSource(args.data)
    if args.verbose:
        print(f'Current data source: {Market.getDataFilePath()}\n')

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

    for strategy in strategies_to_execute:
        print(f'Backtest summary of {strategy[0]} (monthly values)')
        timeframe, geom_returns, log_returns = strategy[1]().evalStrategy()
        all_timeframe[strategy[0]] = timeframe
        all_returns[strategy[0]] = geom_returns
        all_log_returns[strategy[0]] = log_returns
        avg_geom_return = np.power(reduce(lambda R, r: R * (1+r), geom_returns, 1), 1/len(geom_returns)) - 1
        avg_log_return = np.mean(log_returns)
        std_log_return = np.std(log_returns)
        print(f'Time range            : {timeframe[0]} to {timeframe[-1]}')
        print(f'Average geom. return  : {avg_geom_return:+.6f}')
        print(f'Average log return    : {avg_log_return:+.6f}')
        print(f'Average volatility    : {std_log_return:+.6f}')
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
