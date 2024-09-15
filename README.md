# SimplyWall.St Scraper

![GitHub Actions workflow status badge](https://github.com/eugenius1/stock-scrape/actions/workflows/python-app.yml/badge.svg)
[![codecov](https://codecov.io/github/eugenius1/stock-scrape/graph/badge.svg?token=XO0TN6QM66)](https://codecov.io/github/eugenius1/stock-scrape)

Scrapes some stock metrics from [Simply Wall St.](https://simplywall.st/).

TODO:

- [ ] Values are currently not successfully parsed. `SwsCyIds` or the parsing logic needs to be updated.

## Pre-requisites

- [Python](https://www.python.org/downloads/)
- [Pipenv](https://pipenv.pypa.io/en/latest/installation.html)

## Install dependencies

```sh
make install
```

## Run

```sh
pipenv run python main.py --help
```

Usage:

```txt
usage: main.py [-h] [--tickers TICKERS] [--output OUTPUT]

options:
  -h, --help            show this help message and exit
  --tickers TICKERS, -t TICKERS
                        Headerless CSV with tickers and optionally the SimplyWall.St URL
  --output OUTPUT, -o OUTPUT
                        Output CSV for results
```

For example, an input CSV file with tickers and optional SWS URL (it will be searched if empty):

```csv
AAPL,
GOOG,https://simplywall.st/stocks/us/media/nasdaq-googl/alphabet
```

Output after running `pipenv run python main.py -t in.csv -o out.csv`:

```csv
Ticker,SimplyWall.St URL,Name,Forecasted earnings growth,Forecasted revenue growth,Debt to equity ratio,Operating Cash Flow to Debt
AAPL,https://simplywall.st/stocks/us/tech/nasdaq-aapl/apple,Apple,,,,
GOOG,https://simplywall.st/stocks/us/media/nasdaq-googl/alphabet,Alphabet,,,,
```
