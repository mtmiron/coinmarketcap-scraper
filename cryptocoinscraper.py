"""
This module implements a scraper for CoinMarketCap.com.
"""
import os
import sys
import abc
import collections
import json
import logging
import datetime

import pandas as pd
from pyquery import PyQuery
import requests


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


CryptoCoin = collections.namedtuple('CryptoCoin', ['name', 'symbol',
                                                   'price',
                                                   'circulatingSupply',
                                                   'percentChange24h',
                                                   'percentChange7d',
                                                   'marketCap',
                                                   'volume24h',
                                                   'datetime'])


class Scraper(abc.ABC):
    """
    Abstract base class for a web scraper.
    """
    def __init__(self, urls: list):
        """
        Initialize a scraper object.

        Args:
            urls (list): a list of the URLs that will be scraped.
        """
        self.urls = urls

    def pages(self):
        """
        Generator that iterates over all pages and yields each HTML document.
        """
        for url in self.urls:
            resp = requests.get(url)
            if not resp.ok:
                raise RuntimeError("response code: {}".format(resp.status_code))
            yield resp.content

    @abc.abstractmethod
    def parse_html(self, html: str) -> pd.DataFrame:
        """
        For implementation by subclasses: parse an HTML document.

        Args:
            html (str): the HTML, as a string, that contains our desired data.

        Returns:
            A Pandas DataFrame with the desired entries.
        """
        raise NotImplementedError()


class CoinMarketCap(Scraper):
    URL = "https://coinmarketcap.com"

    def __init__(self):
        super().__init__([self.URL])

    def parse_html(self, html: str) -> pd.DataFrame:
        pq = PyQuery(html)
        elems = pq('script#__NEXT_DATA__')
        if len(elems) == 0:
            raise ValueError("unrecognized HTML structure")

        outer_data = json.loads(elems[0].text)
        try:
            outer_data = outer_data['props']['initialState']['cryptocurrency']
            data = outer_data['listingLatest']['data']
        except KeyError as exc:
            logger.error("unrecognized structure: {}".format(exc))
            raise exc

        return self._parse_json_data(data)

    def _parse_json_data(self, data: list) -> pd.DataFrame:
        """
        Parse a list of dictionary objects, each with a structure as seen on
        CoinMarketCap.com.

        Args:
            data (list): a list of dict objects (e.g. loaded from JSON)

        Returns:
            A Pandas DataFrame.
        """
        coins = []
        for coin in data:
            name = coin['name']
            symbol = coin['symbol']
            circulatingSupply = coin['circulatingSupply']

            quote = coin['quote']
            price = quote['USD']['price']
            percentChange24h = quote['USD']['percentChange24h']
            percentChange7d = quote['USD']['percentChange7d']
            marketCap = quote['USD']['marketCap']
            volume24h = quote['USD']['volume24h']

            cryptocoin = CryptoCoin(name, symbol, price,
                                    circulatingSupply, percentChange24h,
                                    percentChange7d, marketCap, volume24h,
                                    datetime.datetime.now())
            coins.append(cryptocoin)

        return pd.DataFrame(coins)

    def to_dataframe(self) -> pd.DataFrame:
        """
        Convenience method to return a Pandas DataFrame in one line.
        
        Returns:
            A Pandas DataFrame of the current market data.
        """
        dfs = []
        for page in self.pages():
            dfs.append(self.parse_html(page))
        return pd.concat(dfs)


# tests
if __name__ == "__main__":
    try:
        scraper = CoinMarketCap()
        for page in scraper.pages():
            df = scraper.parse_html(page)
            df.to_csv(None, index=False)
    except Exception as exc:
        logger.error("tests failed: {}".format(exc))
        sys.exit(os.EX_SOFTWARE)

    logger.info("tests passed")
    sys.exit(os.EX_OK)
