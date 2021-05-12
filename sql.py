"""
Provides database functionality for CryptoCoinScraper.
"""
import os
import sys
import logging

import pandas as pd
import sqlalchemy
from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table, Time
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

import cryptocoinscraper


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base()
Session = sessionmaker()
engine = None


class CryptoCurrency(Base):
    __tablename__ = "cryptocurrencies"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    symbol = Column(String(15))

    data = relationship('MarketData', backref='cryptocurrencies')


class MarketData(Base):
    __tablename__ = 'marketdata'

    id = Column(Integer, primary_key=True)
    currency_id = Column(Integer, ForeignKey('cryptocurrencies.id'))
    price = Column(Float)
    circulatingSupply = Column(Float)
    percentChange24h = Column(Float)
    percentChange7d = Column(Float)
    marketCap = Column(Float)
    volume24h = Column(Float)
    datetime = Column(Time)


def insert_dataframe(df: pd.DataFrame, filename:str):
    """
    Insert a Pandas DataFrame into the database.

    Args:
        df (pd.DataFrame): the DataFrame to get data from.
        filename (str): path to the database.
    """
    Base.metadata.create_all(get_engine(filename))
    with Session(bind=get_engine()) as session:
        for i in range(len(df)):
            row = df.iloc[i]
            coin = session.query(CryptoCurrency).filter_by(name=row.name, symbol=row.symbol).first()
            if coin is None:
                coin = CryptoCurrency(name=row.name, symbol=row.symbol)
                session.add(coin)
                session.commit()

            d = row.to_dict()
            d.pop('name')
            d.pop('symbol')
            d.update({'currency_id': coin.id, 'datetime': row.datetime.time()})

            data = MarketData(**d)
            session.add(data)

        session.commit()


def get_engine(filename=None):
    """
    Get a SQLAlchemy engine; note that subsequent calls will use the
    first `filename` argument that this function received.
    """
    global engine
    if engine is None:
        engine = sqlalchemy.create_engine("sqlite+pysqlite:///{}".format(filename))
    elif filename is not None:
        logger.warning("ignoring the provided filename in get_engine()".format(filename))
    return engine


# simple tests
if __name__ == '__main__':
    scraper = cryptocoinscraper.CoinMarketCap()
    df = scraper.to_dataframe()

    insert_dataframe(df, ":memory:")
    
    print("Tests passed.")
    sys.exit(os.EX_OK)
