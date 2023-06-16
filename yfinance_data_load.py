# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.6
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

import pandas as pd
import yfinance as yf


def get_etf_price_data():
    """
    Import stock price data of specified ETFs in Yahoo Finance.
    
    :return: Weekly close price DataFrame.
    """
    
    tickers = ['XLB', 'XLE', 'XLF', 'XLI', 'XLK', 'XLP', 'XLU', 'XLV', 'XLY']
    etf = yf.Tickers(tickers)
    data = etf.history(start='2013-06-01', actions=False)
    data.drop(['Open', 'High', 'Low', 'Volume'], inplace=True, axis=1)
    data = data.droplevel(0, axis=1)
    data.ffill(inplace=True)
    data = data.resample('W').last().iloc[:-1]

    return data
