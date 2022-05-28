import unittest

import scraper


class TestForecastedRevenueScraper(unittest.TestCase):
    def test_simple(self):
        page = "Revenue vs Market: MAR's revenue (24.4% per year) is forecast to grow faster than the US market (10.7% per year)."
        result = scraper._forecasted_revenue_growth(page)
        self.assertEqual(result, '24.4%')


class TestDebtToEquityScraper(unittest.TestCase):
    def test_simple(self):
        page = "Debt Level: MAR's debt to equity ratio (4734.5%) is considered high."
        result = scraper._debt_to_equity(page)
        self.assertEqual(result, '4734.5%')


class TestUrlVerifier(unittest.TestCase):
    def test_(self):
        news_url = 'https://simplywall.st/stocks/us/semiconductors/nasdaq-xlnx/xilinx/news/is-it-too-late-to-consider-buying-xilinx-inc-nasdaqxlnx'
        main_url = 'https://simplywall.st/stocks/us/semiconductors/nasdaq-xlnx/xilinx'
        self.assertEqual(main_url, scraper._main_url(news_url))


if __name__ == '__main__':
    unittest.main()
