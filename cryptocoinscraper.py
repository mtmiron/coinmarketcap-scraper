import abc
import collections
import json
import logging

import pandas as pd
from pyquery import PyQuery
import requests


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


CryptoCoin = collections.namedtuple('CryptoCoin', ['name', 'symbol',
                                                   'circulatingSupply',
                                                   'price',
                                                   'percentChange24h',
                                                   'percentChange7d',
                                                   'marketCap',
                                                   'volume24h'])


class Scraper(abc.ABC):
    def __init__(self, urls):
        self.urls = urls

    def pages(self):
        for url in self.urls:
            resp = requests.get(url)
            if not resp.ok:
                raise RuntimeError("response code: {}".format(resp.status_code))
            yield resp.content

    @abc.abstractmethod
    def parse_html(self, html):
        raise NotImplementedError()


class CoinMarketCap(Scraper):
    URL = "https://coinmarketcap.com"

    def __init__(self):
        super().__init__([self.URL])

    def parse_html(self, html):
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
                                    percentChange7d, marketCap, volume24h)
            coins.append(cryptocoin)

        return pd.DataFrame(coins) 


# tests
if __name__ == "__main__":
    scraper = CoinMarketCap()
    for page in scraper.pages():
        df = scraper.parse_html(page)
        df.to_csv("output.csv", index=False)
