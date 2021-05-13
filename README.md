[![Tests](https://github.com/mtmiron/coinmarketcap-scraper/actions/workflows/pytest.yml/badge.svg)](https://github.com/mtmiron/coinmarketcap-scraper/actions/workflows/pytest.yml)

# Crypto Currency Scraper

*N.B.: this was actually a coding assessment as part of an interviewing process; normally I wouldn't release details of it, let alone the code, but in this instance a repository was requested by the interviewer*

A simple utility to scrape the data from [CoinMarketCap](https://coinmarketcap.com) and store it in CSV and/or SQLite3 files.  A new CSV file will be written every time the program is run, but an existing database will be updated with new data/timestamps.

# Usage
Make sure all requirements have been installed by running the command `pip install -r requirements.txt`

Then:

```
usage: coinmarketcap-scraper.py [-h] [-o OUT] [-s SQL]

CoinMarketCap scraper.

optional arguments:
  -h, --help         show this help message and exit
  -o OUT, --out OUT  file to write the CSV to (default is STDOUT).
  -s SQL, --sql SQL  sqlite3 database to update (default is don't update any
                     database).
```

Alternatively, it can be installed via (note, though, that `pip install -r requirements.txt` will still be a necessary prerequisite):

```
$ python3 setup.py install --user
```


# Comments

It would be pretty trivial to change the database from SQLite3 to MySQL or whatever else is desired (`sql.py` uses SQLAlchemy); the simple SQLite3 schema can be seen below.

```
CREATE TABLE cryptocurrencies (
        id INTEGER NOT NULL,
        name VARCHAR(255),
        symbol VARCHAR(15),
        PRIMARY KEY (id)
);

CREATE TABLE marketdata (
        id INTEGER NOT NULL,
        currency_id INTEGER,
        price FLOAT,
        "circulatingSupply" FLOAT,
        "percentChange24h" FLOAT,
        "percentChange7d" FLOAT,
        "marketCap" FLOAT,
        volume24h FLOAT,
        datetime TIME,
        PRIMARY KEY (id),
        FOREIGN KEY(currency_id) REFERENCES cryptocurrencies (id)
);
```
