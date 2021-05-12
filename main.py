#!/usr/bin/env python3
import argparse
import sys
import datetime

import cryptocoinscraper
import sql

def get_parser():
    """
    Return an argument parser with the appropriate options.
    """
    parser = argparse.ArgumentParser(description="CoinMarketCap scraper.")
    parser.add_argument("-o", "--out", help="file to write the CSV to (default is STDOUT).")
    parser.add_argument("-s", "--sql", help="sqlite3 database to update (default is don't update any database).")
    return parser


def handle_cli(args):
    """
    Perform the operations dictated by the command line arguments.
    """
    scraper = cryptocoinscraper.CoinMarketCap()
    for page in scraper.pages():
        df = scraper.parse_html(page)

        # csv output
        output = df.to_csv(args.out, index=False)
        if (output):
            print(output)

        # sqlite3 output
        if args.sql:
            sql.insert_dataframe(df, args.sql)


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    if args.out == "-":
        args.out = None

    handle_cli(args)
