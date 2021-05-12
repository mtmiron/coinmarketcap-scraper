import cryptocoinscraper
import sql

doc = b"""<html><script id="__NEXT_DATA__">{"props":{"isServer":true,"initialState":{"app":{"locale":"en-US","theme":"DAY","lang":"en","currency":{"global":"usd","table":"","isUnconverted":false},"bottomBannerHeights":{},"browser":{},"window":{"width":0,"height":0,"isNarrowLayout":false},"modal":{"instance":0,"data":{}},"message":""},"calendarEvent":{"listingLatest":{"data":[]},"calendarEventsById":{},"current":{}},"converter":{"isConverting":false,"values":{"from":"","to":"","amount":"","fromLabel":"","toLabel":""},"options":[],"conversions":{},"errors":{}},"cryptocurrency":{"listingLatest":{"page":1,"sort":"rank","sortDirection":"asc","data":[{"id":1,"name":"Bitcoin","symbol":"BTC","slug":"bitcoin","tags":["mineable","pow","sha-256","store-of-value","state-channels","coinbase-ventures-portfolio","three-arrows-capital-portfolio","polychain-capital-portfolio","binance-labs-portfolio","arrington-xrp-capital","blockchain-capital-portfolio","boostvc-portfolio","cms-holdings-portfolio","dcg-portfolio","dragonfly-capital-portfolio","electric-capital-portfolio","fabric-ventures-portfolio","framework-ventures","galaxy-digital-portfolio","huobi-capital","alameda-research-portfolio","a16z-portfolio","1confirmation-portfolio","winklevoss-capital","usv-portfolio","placeholder-ventures-portfolio","pantera-capital-portfolio","multicoin-capital-portfolio","paradigm-xzy-screener"],"cmcRank":1,"marketPairCount":9539,"circulatingSupply":18707500,"totalSupply":18707500,"maxSupply":21000000,"ath":64863.0989077,"atl":65.52600098,"high24h":57354.72648628,"low24h":54608.65245902,"isActive":1,"lastUpdated":"2021-05-12T02:22:02.000Z","dateAdded":"2013-04-28T00:00:00.000Z","quotes":[{"name":"btc","price":1,"volume24h":1065480.87152563,"volume7d":8045531.0415937,"volume30d":331901841.15321016,"marketCap":18707500,"percentChange1h":0,"percentChange24h":0,"percentChange7d":0,"lastUpdated":"2021-05-12T02:22:02.000Z","percentChange30d":-4.6447431,"percentChange60d":1.44213607,"percentChange90d":28.059192,"fullyDilluttedMarketCap":1199367186316.21,"dominance":42.3674,"turnover":0.05695474,"ytdPriceChangePercentage":94.4319},{"name":"eth","price":13.60206085,"volume24h":14492735.64636164,"volume7d":109435802.77837844,"volume30d":4514549038.770293,"marketCap":254460553.30500355,"percentChange1h":-0.581838,"percentChange24h":-4.7516,"percentChange7d":-17.588809,"lastUpdated":"2021-05-12T02:22:02.000Z","percentChange30d":-4.6447431,"percentChange60d":1.44213607,"percentChange90d":28.059192,"fullyDilluttedMarketCap":1199367186316.21,"dominance":42.3674,"turnover":0.05695474,"ytdPriceChangePercentage":94.4319},{"name":"USD","price":57112.72315791473,"volume24h":60852514045.49726,"volume7d":459502187036.9503,"volume30d":18955817969385.48,"marketCap":1068436268476.6897,"percentChange1h":-0.07326618,"percentChange24h":2.15775513,"percentChange7d":3.48917157,"lastUpdated":"2021-05-12T02:22:02.000Z","percentChange30d":-4.6447431,"percentChange60d":1.44213607,"percentChange90d":28.059192,"fullyDilluttedMarketCap":1199367186316.21,"dominance":42.3674,"turnover":0.05695474,"ytdPriceChangePercentage":94.4319}],"rank":1,"hasFilters":false,"noLazyLoad":true,"quote":{"btc":{"name":"btc","price":1,"volume24h":1065480.87152563,"volume7d":8045531.0415937,"volume30d":331901841.15321016,"marketCap":18707500,"percentChange1h":0,"percentChange24h":0,"percentChange7d":0,"lastUpdated":"2021-05-12T02:22:02.000Z","percentChange30d":-4.6447431,"percentChange60d":1.44213607,"percentChange90d":28.059192,"fullyDilluttedMarketCap":1199367186316.21,"dominance":42.3674,"turnover":0.05695474,"ytdPriceChangePercentage":94.4319},"eth":{"name":"eth","price":13.60206085,"volume24h":14492735.64636164,"volume7d":109435802.77837844,"volume30d":4514549038.770293,"marketCap":254460553.30500355,"percentChange1h":-0.581838,"percentChange24h":-4.7516,"percentChange7d":-17.588809,"lastUpdated":"2021-05-12T02:22:02.000Z","percentChange30d":-4.6447431,"percentChange60d":1.44213607,"percentChange90d":28.059192,"fullyDilluttedMarketCap":1199367186316.21,"dominance":42.3674,"turnover":0.05695474,"ytdPriceChangePercentage":94.4319},"USD":{"name":"USD","price":57112.72315791473,"volume24h":60852514045.49726,"volume7d":459502187036.9503,"volume30d":18955817969385.48,"marketCap":1068436268476.6897,"percentChange1h":-0.07326618,"percentChange24h":2.15775513,"percentChange7d":3.48917157,"lastUpdated":"2021-05-12T02:22:02.000Z","percentChange30d":-4.6447431,"percentChange60d":1.44213607,"percentChange90d":28.059192,"fullyDilluttedMarketCap":1199367186316.21,"dominance":42.3674,"turnover":0.05695474,"ytdPriceChangePercentage":94.4319}},"hasAdListingButton":true}]}}}}}</script></html>"""

PRICE = 57112.72315791473
VOLUME24H = 60852514045.49726
PERCENTCHANGE7D = 3.48917157


def test_parser():

    scraper = cryptocoinscraper.CoinMarketCap()
    df = scraper.parse_html(doc)
    assert df.iloc[0]["name"] == "Bitcoin"
    assert df.iloc[0]["symbol"] == "BTC"
    assert df.iloc[0]["price"] == PRICE
    assert df.iloc[0]['volume24h'] == VOLUME24H
    assert df.iloc[0]['percentChange7d'] == PERCENTCHANGE7D


def test_database():
    scraper = cryptocoinscraper.CoinMarketCap()
    df = scraper.parse_html(doc)

    sql.insert_dataframe(df, ":memory:")
    with sql.Session(bind=sql.get_engine()) as session:
        coin = session.query(sql.CryptoCurrency).filter_by(name='Bitcoin', symbol='BTC').first()
        data = session.query(sql.MarketData).filter_by(currency_id=coin.id).first()
        assert data.price == PRICE
        assert data.volume24h == VOLUME24H
        assert data.percentChange7d == PERCENTCHANGE7D

