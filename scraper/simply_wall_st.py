import http
import logging
import re
import requests
import time

import googlesearch
from bs4 import BeautifulSoup
import pandas as pd

google_search_interval_seconds = 2
sws_interval_seconds = 1  # > 0.4


class SwsCyIds:
    company_title = "company-header-title"

    # Not currently used
    forecasted_earnings_growth = (
        "report-statement-isExpectedAnnualProfitGrowthAboveMarket"
    )
    forecasted_revenue_growth = "report-statement-isExpectedRevenueGrowthAboveMarket"
    debt_to_equity = "report-statement-hasDebtReducedOverTime"
    ocf_to_debt = "report-statement-isDebtCoveredByCashflow"


def _find_by_cy_id(
    soup: BeautifulSoup, cy_id: str, default: str = "", first_string=False
) -> str:
    """Returns the combined text inside the element with attribute `data-cy-id` equal to value of `cy_id`,
    or value of `default` if not found.
    Returns first (stripped) string if `first_string` = True.
    """
    found = soup.find(attrs={"data-cy-id": cy_id})
    if found is None:
        return default
    if first_string:
        for string in found.stripped_strings:
            return string
    return found.text


class Patterns:
    percentage_figure = r"-?\d+[\.\d]*%"
    # These 2 assume text is only for the revenue or only for earnings, ie. result of _find_by_cy_id
    forecasted_revenue_growth = rf" \(({percentage_figure}) per year\)"
    forecasted_earnings_growth = rf" \(({percentage_figure}) per year\)"
    debt_to_equity = rf" debt to equity ratio has \w+ from {percentage_figure} to ({percentage_figure})"
    ocf_to_debt = rf" well covered by operating cash flow \(({percentage_figure})\)"


def _find_first(pattern: str, page: str) -> str:
    """Returns the first regex match or empty string if none."""
    matches = re.findall(pattern, page)
    if matches:
        return matches[0]
    return ""


def simply_wall_st(table: pd.DataFrame) -> pd.DataFrame:  # noqa: C901 # FIXME: Refactor
    """Table should be a pandas.DataFrame with these columns (in order):
    - Ticker
    - SWS URL (optionally filled with values)
    """

    successful_tickers = []
    failed_tickers = []
    names = []
    urls = []
    forecasted_earnings_growth = []
    forecasted_revenue_growth = []
    debt_to_equity = []
    ocf_to_debt = []

    for index, row in table.iterrows():
        ticker = row[0]
        if len(row) >= 2:
            sws_url = row[1]
        else:
            sws_url = None

        logging.info(f"{index+1}/{len(table)}: {ticker}...")

        try:
            if not sws_url or sws_url is not str:
                try:
                    search_results = googlesearch.search(
                        f"site:simplywall.st {ticker}", num_results=1
                    )
                    sws_url = next(search_results)
                    sws_url = _main_url(sws_url)
                    # TODO: verify link, maybe by checking if it contains (nyse|nasdaq)
                    logging.info(sws_url)
                    if index != 0:
                        time.sleep(google_search_interval_seconds)

                except Exception as e:
                    logging.error(f"Google search failed with exception: {e}")
                    break

            logging.debug(f"{ticker}: {sws_url}")

            if index != 0:
                time.sleep(sws_interval_seconds)
            page = requests.get(sws_url)
            if page.status_code == http.HTTPStatus.TOO_MANY_REQUESTS:
                logging.error(
                    "{}: {}".format(
                        page.status_code, http.HTTPStatus.TOO_MANY_REQUESTS.brief
                    )
                )
                break
            page.raise_for_status()

            soup = BeautifulSoup(page.content, "html.parser")

            urls.append(sws_url)
            names.append(
                _find_by_cy_id(soup, SwsCyIds.company_title, first_string=True)
            )
            forecasted_earnings_growth.append(
                _find_first(
                    Patterns.forecasted_earnings_growth,
                    _find_by_cy_id(soup, SwsCyIds.forecasted_earnings_growth),
                )
            )
            forecasted_revenue_growth.append(
                _find_first(
                    Patterns.forecasted_revenue_growth,
                    _find_by_cy_id(soup, SwsCyIds.forecasted_revenue_growth),
                )
            )
            # TODO add case for "YQ is debt free."
            debt_to_equity.append(
                _find_first(
                    Patterns.debt_to_equity,
                    _find_by_cy_id(soup, SwsCyIds.debt_to_equity),
                )
            )
            ocf_to_debt.append(
                _find_first(
                    Patterns.ocf_to_debt, _find_by_cy_id(soup, SwsCyIds.ocf_to_debt)
                )
            )

            successful_tickers.append(ticker)

        except Exception as e:
            logging.error(f"Failed at ticker {ticker} with exception: {e}")
            failed_tickers.append(ticker)

    results = pd.DataFrame(
        {
            "Ticker": successful_tickers,
            "SimplyWall.St URL": urls,
            "Name": names,
            "Forecasted earnings growth": forecasted_earnings_growth,
            "Forecasted revenue growth": forecasted_revenue_growth,
            "Debt to equity ratio": debt_to_equity,
            "Operating Cash Flow to Debt": ocf_to_debt,
        }
    )

    return results


def _main_url(candidate_url: str) -> str:
    """Returns the main report url if given a news url."""
    news_index = candidate_url.find("/news/")
    if news_index != -1:
        candidate_url = candidate_url[:news_index]
    return candidate_url
