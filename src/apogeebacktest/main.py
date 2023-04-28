#!/usr/bin/env python
"""Entrypoint of the module."""

import sys
import inspect
import argparse
import pathlib
import numpy as np
import pandas as pd
from multiprocessing import Pool
from typing import Optional, List, Tuple

import apogeebacktest.strategies
from apogeebacktest.data import Connector, PandasXLSXConnector
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


def parallel_eval(strategy_instance:Strategy, connectors:List[Connector]) -> Tuple[np.array, np.array, np.array]:
    """Wrapper for `multiprocessing.Pool.apply_async()`.

    Parameters
    ----------
    strategy_instance : Strategy
        A `Strategy` instance to backtest.
    connectors : List[Connector]
        A list of `Connector` objects.

    Returns
    -------
    Tuple[np.array, np.array, np.array]
        A tuple of (timeframe, geom_returns, log_returns)
    """
    from apogeebacktest.data import Market
    for connector in connectors:
        Market.addDataSource(connector)
    return strategy_instance.evalStrategy()


def load_dataframe(data_path:pathlib.Path, sheet_name:Optional[str]=None) -> Tuple[pd.DataFrame, pathlib.Path]:
    """User-injected custom processing logic to parse your particular Excel file.

    Load a `.xlsx` data source into pandas.DataFrame.
    Indices are stock code, and columns are date.

    Parameters
    ----------
    data_path : pathlib.Path
        Path to the data file.
    sheet_name : str
        Name of the Excel sheet.

    Returns
    -------
    Tuple[pd.DataFrame, pathlib.Path]
        The parsed dataframe and the path to the data source.
    """
    df = pd.read_excel(data_path, sheet_name=sheet_name, index_col=0)
    df.index = [name.split(' ')[1] for name in df.index]
    df.index = df.index.astype(int)
    df.sort_index(inplace=True)
    df.columns = df.columns.astype(str)
    return df, data_path


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

    # Setup data sources.
    if args.data is None:
        # Load default market data.
        resources_folder = (pathlib.Path(__file__) / '../resources' ).resolve()
        data_path = (resources_folder / 'dataset.xlsx').resolve()
        if args.verbose:
            print(f'Using default data source at {data_path}.')
    else:
        data_path = pathlib.Path(args.data).resolve()
        if args.verbose:
            print(f'Setting data source to {data_path}')
    returns_source = PandasXLSXConnector('returns', load_dataframe, {'data_path': data_path, 'sheet_name': 'Return'})
    bpratio_source = PandasXLSXConnector('bpratio', load_dataframe, {'data_path': data_path, 'sheet_name': 'Book to price'})
    connectors = [returns_source, bpratio_source]
    from apogeebacktest.data import Market
    if not Market.hasDataSource('returns'):
        Market.addDataSource(returns_source)
    if not Market.hasDataSource('bpratio'):
        Market.addDataSource(bpratio_source)

    # Backtest strategies.
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
        strategies_executed = [pool.apply_async(parallel_eval, (strategy[1](), connectors)) for strategy in strategies_to_execute]
        for strategy, res in zip(strategies_to_execute, strategies_executed):
            timeframe, geom_returns, log_returns = res.get()
        # for strategy in strategies_to_execute:
        #     timeframe, geom_returns, log_returns = strategy[1]().evalStrategy()
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
        # print('                              ')
        print('==============================')
        print('=====   End of program   =====')
        print('==============================')



if __name__ == "__main__":

    main_cli(['-v', 'LongShortBPStrategy', 'WorstBPStrategy', 'BestBPStrategy', 'MarketStrategy'])
