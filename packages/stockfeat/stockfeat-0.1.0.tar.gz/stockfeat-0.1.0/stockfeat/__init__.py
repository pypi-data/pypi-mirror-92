from stockfeat.stockfeat import stockfeat

from stockfeat.volume import *
from stockfeat.volatility import *
from stockfeat.trend import *
from stockfeat.momentum import *
from stockfeat.others import *
from stockfeat.others import rolling_return
from stockfeat.timeseries_normalize_rolling import timeseries_normalize_rolling

__author__ = 'Erdogan Tasksen'
__email__ = 'erdogant@gmail.com'
__version__ = '0.1.0'

# module level doc-string
__doc__ = """
stockfeat
=====================================================================

Description
-----------
stockfeat is for...

Example
-------
>>> import stockfeat as stockfeat
>>> model = stockfeat.fit(X)
>>> fig,ax = stockfeat.plot(model)

References
----------
https://github.com/erdogant/stockfeat

"""
