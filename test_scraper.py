import unittest

import scraper


class TestRegexScrapers(unittest.TestCase):
    def test_forecasted_revenue_growth(self):
        page = "SMSN's revenue (7% per year) is forecast to grow faster than the UK market (4% per year)."
        result = scraper._find_first(
            scraper.Patterns.forecasted_revenue_growth, page)
        self.assertEqual(result, '7%')

    def test_forecasted_earnings_growth_negative(self):
        page = "BNTX's earnings are forecast to decline over the next 3 years (-40.2% per year)."
        result = scraper._find_first(
            scraper.Patterns.forecasted_earnings_growth, page)
        self.assertEqual(result, '-40.2%')

    def test_forecasted_earnings_growth(self):
        page = "SMSN's earnings (8.7% per year) are forecast to grow slower than the UK market (11.3% per year)."
        result = scraper._find_first(
            scraper.Patterns.forecasted_earnings_growth, page)
        self.assertEqual(result, '8.7%')

    def test_debt_to_equity(self):
        page = "SMSN's debt to equity ratio has reduced from 7% to 4.6% over the past 5 years."
        result = scraper._find_first(
            scraper.Patterns.debt_to_equity, page)
        self.assertEqual(result, '4.6%')

    def test_debt_coverage(self):
        page = "SMSN's debt is well covered by operating cash flow (427.4%)"
        result = scraper._find_first(
            scraper.Patterns.ocf_to_debt, page)
        self.assertEqual(result, '427.4%')


class TestUrlVerifier(unittest.TestCase):
    def test_(self):
        news_url = 'https://simplywall.st/stocks/us/semiconductors/nasdaq-xlnx/xilinx/news/is-it-too-late-to-consider-buying-xilinx-inc-nasdaqxlnx'
        main_url = 'https://simplywall.st/stocks/us/semiconductors/nasdaq-xlnx/xilinx'
        self.assertEqual(main_url, scraper._main_url(news_url))


if __name__ == '__main__':
    unittest.main()
