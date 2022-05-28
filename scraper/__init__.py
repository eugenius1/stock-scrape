import logging
import re
import requests
import time

from googlesearch import search
from bs4 import BeautifulSoup
import pandas as pd

interval_seconds = 2


class SwsCyIds:
    forecasted_earnings_growth = 'key-metric-value-forecasted-annual-earnings-growth'
    company_title = 'company-header-title'


def _find_by_cy_id(soup, cy_id, default='') -> str:
    found = soup.find(attrs={'data-cy-id': cy_id})
    if found is None:
        return default
    return found.text


def simply_wall_st(table):
    """Table should be a pandas.DataFrame with these columns (in order):
        - Ticker
        - SWS URL
    """

    successful_tickers = []
    failed_tickers = []
    names = []
    urls = []
    fegs = []
    frgs = []
    dtes = []

    for index, row in table.iterrows():
        ticker = row[0]
        if len(row) >= 2:
            sws_url = row[1]
        else:
            sws_url = None

        logging.info(f'{index+1}/{len(table)}: {ticker}...')

        try:
            if not sws_url or type(sws_url) != str:
                try:
                    sws_url = search(
                        f'site:simplywall.st {ticker}', num_results=1)[0]
                    sws_url = _main_url(sws_url)
                    logging.info(sws_url)
                    # TODO: verify link, maybe by checking if it contains (nyse|nasdaq)
                    time.sleep(interval_seconds)
                except Exception as e:
                    logging.error(f'Google search failed with exception: {e}')
                    break

            logging.debug(f'{ticker}: {sws_url}')

            page = requests.get(sws_url)
            page.raise_for_status()
            page_content = str(page.content)
            soup = BeautifulSoup(page.content, 'html.parser')

            urls.append(sws_url)
            names.append(_find_by_cy_id(soup, SwsCyIds.company_title))
            fegs.append(_find_by_cy_id(
                soup, SwsCyIds.forecasted_earnings_growth))
            frgs.append(_forecasted_revenue_growth(page_content))
            dtes.append(_debt_to_equity(page_content))

            successful_tickers.append(ticker)

        except Exception as e:
            logging.error(f'Failed at ticker {ticker} with exception: {e}')
            failed_tickers.append(ticker)

    results = pd.DataFrame({
        'Ticker': successful_tickers,
        'SimplyWall.St URL': urls,
        'Name': names,
        'Forecasted earnings growth': fegs,
        'Forecasted revenue growth': frgs,
        'Debt to equity ratio': dtes,
    })

    return results


def _forecasted_revenue_growth(page) -> str:
    """Finds the forecasted revenue growth percentage."""
    matches = re.findall(r' revenue \(([\d\.\%]+) per year\)', page)
    if matches:
        return matches[0]
    return ''


def _debt_to_equity(page) -> str:
    """Finds the debt to equity ratio."""
    matches = re.findall(r' debt to equity ratio \(([\d\.\%]+)\)', page)
    if matches:
        return matches[0]
    return ''


def _main_url(candidate_url: str) -> str:
    news_index = candidate_url.find('/news/')
    if news_index != -1:
        candidate_url = candidate_url[:news_index]
    return candidate_url
