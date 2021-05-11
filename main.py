#!/usr/bin/env python3
import argparse
import sys

import cryptocoinscraper


def get_parser():
    parser = argparse.ArgumentParser(description="CoinMarketCap scraper.")
    parser.add_argument("-o", "--out", help="file to write the CSV to")
    return parser


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    if args.out == "-":
        args.out = None

    scraper = cryptocoinscraper.CoinMarketCap()
    for page in scraper.pages():
        df = scraper.parse_html(page)
        output = df.to_csv(args.out, index=False)
        if (output):
            print(output)
