#!/usr/bin/env python

from distutils.core import setup

setup(name='coinmarketcap-scraper',
      packages=['coinmarketcap-scraper'],
      package_dir={'coinmarketcap-scraper': '.'},
      version='1.0',
      description='Simple utility to scrape https://coinmarketcap.com',
      author='Murray Miron',
      author_email='murrayTmiron@gmail.com',
      url='',
      scripts=['coinmarketcap-scraper.py'],
      package_data={'coinmarketcap-scraper': ['./requirements.txt']},
     )
