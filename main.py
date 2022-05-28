#!/usr/bin/env python3

import argparse
import logging
import os

import pandas as pd

import scraper

logging.basicConfig(level=logging.INFO)


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--tickers', '-t', default='tickers.csv',
                        help='Headerless CSV with tickers and optionally the SimplyWall.St URL')
    parser.add_argument('--output', '-o', default='output.csv',
                        help='Output CSV for results')

    args = parser.parse_args()
    if not os.path.isfile(args.tickers):
        raise FileNotFoundError(f'{args.tickers} is not a file.')
    return args


def main():
    args = _parse_args()

    results = scraper.simply_wall_st(pd.read_csv(args.tickers, header=None))

    logging.info(f'Writing to {args.output}')
    results.to_csv(args.output, index=False)


if __name__ == "__main__":
    main()
