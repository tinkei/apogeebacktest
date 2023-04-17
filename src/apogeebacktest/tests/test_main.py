import numpy as np

from apogeebacktest import main


def test_parse_argument():

    args = ['-v', 'LongShortBPStrategy', 'WorstBPStrategy', 'BestBPStrategy', 'MarketStrategy', '-d', 'hello.xlsx', '--output-path', 'fake-path']
    parsed = main.parse_arguments(args)
    strategies = ['LongShortBPStrategy', 'WorstBPStrategy', 'BestBPStrategy', 'MarketStrategy']
    for strategy in parsed.strategies:
        assert strategy in strategies
    assert parsed.verbose
    assert parsed.output_path == 'fake-path'
    assert parsed.data == 'hello.xlsx'


def test_main_cli():

    # Just a test run to see the pipeline works. No assert.
    main.main_cli(['-v', 'LongShortBPStrategy', 'WorstBPStrategy', 'BestBPStrategy', 'MarketStrategy'])


if __name__ == "__main__":

    test_parse_argument()
    test_main_cli()
