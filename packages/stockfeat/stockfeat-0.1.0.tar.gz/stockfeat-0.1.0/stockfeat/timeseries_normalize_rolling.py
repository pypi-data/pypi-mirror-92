""" This function provides computes the normalized value on the stats of n values, and also depends on the mode, and (non) linear scaling.

	A= timeseries_normalize_rolling(data, n , <optional>)

 INPUT:
   data:           Numpy array with numbers

   ds:             pandas array of datetime
                   e.g., dates= pd.to_datetime(['08-08-2018','10-08-2018','10-09-2018'])

   interval:       String: window that is used to normalize.
                   'rolling' (default)
                   'year'
                   'month'
                   'year_overlap' (per year with 30 overlapping days across years)

 OPTIONAL

   mode:           String: 
                   'zscore': (default)
                   'minmax': [0-1]

   window:         Integer: (only for rolling)
                   50: (default)

 OUTPUT
     Returns a numpy array that is modified to fit the data from [-1 to 1]


 DESCRIPTION
     

 EXAMPLE
   %reset -f
   import sys, os, importlib
   sys.path.append('D://stack/TOOLBOX_PY/PY/')
   import predictors.helpers.timeseries_normalize_rolling as eta
   importlib.reload(eta)
   import pandas as pd

   data=pd.read_pickle('D://stack/TOOLBOX_PY/DATA/STOCK/btcyears.pkl')
   ds=data['ds']
   data=data['y'].values
   A = eta.timeseries_normalize_rolling(data, ds, interval='year',showfig=True)
   A = eta.timeseries_normalize_rolling(data, ds, interval='year_overlap',showfig=True)
   A = eta.timeseries_normalize_rolling(data, ds, interval='rolling', mode='minmax', window=50, showfig=True)
   A = eta.timeseries_normalize_rolling(data, ds, interval='rolling', mode='zscore', window=50, showfig=True)

   
   [fig, (ax1,ax2)]=plt.subplots(1,2, figsize=(10,4));
   ax1.plot(date, y);ax1.grid(True)
   ax2.plot(date, A);ax2.grid(True)

 SEE ALSO
   timeseries_prediction
   
"""
#print(__doc__)

#--------------------------------------------------------------------------
# Name        : timeseries_normalize_rolling.py
# Version     : 1.0
# Author      : E.Taskesen
# Contact     : erdogant@gmail.com
# Date        : Aug. 2018
#--------------------------------------------------------------------------

#from matplotlib.pyplot import plot

#%% Libraries
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

#%%
def timeseries_normalize_rolling(data, ds, interval='rolling', mode='minmax', window=50, fillna=True, showfig=False, width=15, heigth=8):
	#%% DECLARATIONS
    out =[]
    # Make dictionary to store Parameters
    Param = {}
    Param['mode'] = mode
    Param['interval'] = interval
    Param['window'] = window
    Param['showfig'] = showfig

    #%% Convert to pandas
    out=[]
    if 'pandas' in str(type(data)):
        data = data.values
    #end

    # output dataframe
    out = np.zeros(len(data))*np.nan
    
    #%% Setup 
    if Param['interval']=='year':
        getid=ds.dt.year
    elif Param['interval']=='month':
        getid=ds.dt.year.astype(str)+'_'+ds.dt.month.astype(str)
    elif Param['interval']=='year_overlap':
        getid=ds.dt.year.astype(int)
        uiyears=getid.unique()
        for i in range(0,len(uiyears)):
            idx=np.max(np.where(uiyears[i]==ds.dt.year))
            getid.iloc[idx:idx+30]=getid[idx]
    elif Param['interval']=='rolling' and mode=='minmax':
        df = pd.DataFrame(data)
        out = df.rolling(Param['window']).apply(do_scaling_minmax).values.flatten()
    elif Param['interval']=='rolling' and mode=='zscore':
        df = pd.DataFrame(data)
        out = df.rolling(Param['window']).apply(do_scaling_zscore).values.flatten()
    else:
        print('Interval not found!')
        return(out)
    #end

    #%% Normalize/Scale
    if Param['interval']!='rolling':
        uiid=np.unique(getid)
        for i in range(0,len(uiid)):
            I=getid==uiid[i]
            if Param['mode']=='minmax':
                X=preprocessing.minmax_scale(data[I])
            if Param['mode']=='zscore':
                X=preprocessing.scale(data[I], with_std=True)
            out[I]=X
        #end

    #%% Fill NaNs
#    if fillna:
#        out = out.replace([np.inf, -np.inf], np.nan).fillna(0)
        
    #%% Show figure
    if Param['showfig']:
       [fig, (ax1,ax2)]=plt.subplots(1,2, figsize=(width,heigth));
       ax1.plot(ds, data, '.', color='k', markersize=6)
       ax1.plot(ds, data)
       ax1.grid(True)
       ax1.set_title('RAW')
       ax1.set_xlabel('Dates')
       ax1.set_ylabel('Value')

       ax2.plot(ds, out, '.', color='k', markersize=6)
       ax2.plot(ds, out)
       ax2.grid(True)
       ax2.set_title('Normalized')
       ax2.set_xlabel('Dates')
       ax2.set_ylabel('Value')
       plt.show()
   #end
        
    #%% RETURN
    return(out)

#%%
def do_scaling_zscore(r):
    scaler = StandardScaler(with_mean=True, with_std=True)
    r=r.reshape(-1, 1)
    scaler = scaler.fit(r)
    normalized = scaler.transform(r).mean()
    return(normalized)

def do_scaling_minmax(r):
    scaler = MinMaxScaler(feature_range=(0, 1))
    r=r.reshape(-1, 1)
    scaler = scaler.fit(r)
    normalized = scaler.transform(r).mean()
    return(normalized)