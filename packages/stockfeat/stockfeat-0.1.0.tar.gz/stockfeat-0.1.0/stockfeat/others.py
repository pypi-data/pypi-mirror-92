# -*- coding: utf-8 -*-
"""
.. module:: others
   :synopsis: Others Indicators.

"""
import numpy as np
import pandas as pd


def rolling_return(close, window=50, fillna=False):
    rr = close.pct_change().rolling(window).apply(multi_period_return)
    if fillna:
        rr = rr.replace([np.inf, -np.inf], np.nan).fillna(0)
    return pd.Series(rr, name='rolling_return_'+str(window))


def multi_period_return(r):
    return (np.prod(r + 1) - 1) * 100

def daily_return(close, fillna=False):
    """Daily Return (DR)

    Args:
        close(pandas.Series): dataset 'Close' column.
        fillna(bool): if True, fill nan values.

    Returns:
        pandas.Series: New feature generated.
    """
    dr = (close / close.shift(1)) - 1
    dr *= 100
    if fillna:
        dr = dr.replace([np.inf, -np.inf], np.nan).fillna(0)
    return pd.Series(dr, name='daily_return')


def daily_log_return(close, fillna=False):
    """Daily Log Return (DLR)

    https://stackoverflow.com/questions/31287552/logarithmic-returns-in-pandas-dataframe

    Args:
        close(pandas.Series): dataset 'Close' column.
        fillna(bool): if True, fill nan values.

    Returns:
        pandas.Series: New feature generated.
    """
    dr = np.log(close).diff()
    dr *= 100
    if fillna:
        dr = dr.replace([np.inf, -np.inf], np.nan).fillna(0)
    return pd.Series(dr, name='daily_log_return')


def cumulative_return(close, fillna=False):
    """Cumulative Return (CR)

    Args:
        close(pandas.Series): dataset 'Close' column.
        fillna(bool): if True, fill nan values.

    Returns:
        pandas.Series: New feature generated.
    """
    cr = (close / close.iloc[0]) - 1
    cr *= 100
    if fillna:
        cr = cr.replace([np.inf, -np.inf], np.nan).fillna(method='backfill')
    return pd.Series(cr, name='cumulative_return')
