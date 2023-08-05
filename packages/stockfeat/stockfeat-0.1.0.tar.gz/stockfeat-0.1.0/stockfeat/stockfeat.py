# --------------------------------------------------
# Name        : stockfeat.py
# Author      : E.Taskesen
# Contact     : erdogant@gmail.com
# github      : https://github.com/erdogant/stockfeat
# Licence     : See licences
# --------------------------------------------------

import os
import numpy as np
import pandas as pd
import talib
import wget

# from stockfeat.volume import put_call_ratio, negative_volume_index, volume_price_trend, ease_of_movement, force_index, chaikin_money_flow, on_balance_volume_mean, on_balance_volume, acc_dist_index
from stockfeat.volume import *
from stockfeat.volatility import *
from stockfeat.trend import *
from stockfeat.momentum import *
from stockfeat.others import *
from stockfeat.others import rolling_return
# from stockfeat.timeseries_normalize_rolling import timeseries_normalize_rolling


class stockfeat():
    """stockfeat."""

    def __init__(self, col_close='close', col_open='open', col_high='high', col_low='low', col_volume='volume', fillna=False):
        """Initialize distfit with user-defined parameters.

        df (pandas.core.frame.DataFrame): Dataframe base.
        opencolumn (str): Name of 'open' column.
        high (str): Name of 'high' column.
        low (str): Name of 'low' column.
        close (str): Name of 'close' column.
        volume (str): Name of 'volume' column.
        fillna(bool): if True, fill nan values.


        Parameters
        ----------
        col_close : String, The default is 'close'.
            Close column.
        col_open : String, The default is 'open'.
            Open column.
        col_high : String, The default is 'high'.
            High column.
        col_low : TYPE, The default is 'low'.
            Low column. 
        col_volume : TYPE, The default is 'volume'.
            Volume column. 
        fillna : Bool, The default is False.
            Fill NaN values.

        Returns
        -------
        None.

        """
        self.close=col_close
        self.open=col_open
        self.high=col_high
        self.low=col_low
        self.volume=col_volume
        self.fillna=fillna

    def fit(self, df, verbose=3):
        """Compute indicators for the input dataframe."""
        # Create features for which only close price is required
        df = _add_close_only(df, self.close, fillna=self.fillna)
        df = _add_others_ta(df, self.close, fillna=self.fillna)
        df = _add_cycle_indicator(df, self.close, fillna=self.fillna)
        df = _add_momentum_indicator(df, self.close, fillna=self.fillna)
        
        # Create features for which multiple measurements are required
        if np.all(np.isin(df.columns,[self.low, self.volume, self.close, self.high])):
            df = _add_volume_ta(df, self.high, self.low, self.close, self.volume, fillna=self.fillna)
            df = _add_volatility_ta(df, self.high, self.low, self.close, fillna=self.fillna)
            df = _add_trend_ta(df, self.high, self.low, self.close, fillna=self.fillna)
            df = _add_momentum_ta(df, self.high, self.low, self.close, self.volume, self.open, fillna=self.fillna)
            df = _add_normalized_ta(df, self.high, self.low, self.volume, self.open, fillna=self.fillna)
            df = _add_stats(df, self.high, self.low, self.volume, self.open, fillna=self.fillna)
            df = _add_PriceTransform(df, self.high, self.low, self.volume, self.open, self.close, fillna=self.fillna)
            # df = _add_patternrecognition(df, self.open, self.high, self.low, self.close, fillna=self.fillna)
        
        if self.fillna:
            df.fillna(0, inplace=True)
        
        return df

    #  Import example dataset from github.
    def download_example(self, name='btc', verbose=3):
        """Import example dataset from github.
    
        Parameters
        ----------
        name : str, optional
            name of the file to download.
        verbose : int, optional
            Print message to screen. The default is 3.
    
        Returns
        -------
        tuple containing dataset and response variable (X,y).
    
        """
        if name=='facebook':
            url='https://erdogant.github.io/datasets/facebook_stocks.zip'
        else:
            url='https://erdogant.github.io/datasets/BTCUSDT_1m.zip'
    
        curpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
        PATH_TO_DATA = os.path.join(curpath, wget.filename_from_url(url))
    
        # Create dir
        if not os.path.isdir(curpath):
            os.makedirs(curpath, exist_ok=True)
    
        # Check file exists.
        if not os.path.isfile(PATH_TO_DATA):
            if verbose>=3: print('[classeval] Downloading example dataset..')
            wget.download(url, curpath)
    
        # Import local dataset
        if verbose>=3: print('[caerus] Import dataset..')
        df = pd.read_csv(PATH_TO_DATA)
        # Return
        
        if name=='btc':
            df.index = pd.to_datetime(df['Date'].values)
            del df['Date']
        
        return df


#%%
def _add_PriceTransform(df, high, low, volume, opencolumn, close, fillna=False):
    df['AVGPRICE'] = talib.AVGPRICE(df[opencolumn], df[high], df[low], df[close])
    df['MEDPRICE'] = talib.MEDPRICE(df[high], df[low]).fillna(method='backfill')
    df['TYPPRICE'] = talib.TYPPRICE(df[high], df[low], df[close]).fillna(method='backfill')
    df['WCLPRICE'] = talib.WCLPRICE(df[high], df[low], df[close]).fillna(method='backfill')
    return(df)

#%%
def _add_momentum_indicator(df, close, fillna=False):
    df['APO'] = talib.APO(df[close], fastperiod=12, slowperiod=26).fillna(method='backfill')
    df['CMO'] = talib.CMO(df[close], timeperiod=14).fillna(method='backfill')
    df['MOM'] = talib.MOM(df[close]).fillna(method='backfill')
    df['PPO'] = talib.PPO(df[close], fastperiod=12, slowperiod=26).fillna(method='backfill')
    df['ROC'] = talib.ROC(df[close]).fillna(method='backfill')
    df['ROCP'] = talib.ROCP(df[close], timeperiod=10).fillna(method='backfill')
    df['ROCR'] = talib.ROCR(df[close], timeperiod=10).fillna(method='backfill')
    df['ROCR100'] = talib.ROCR100(df[close], timeperiod=10).fillna(method='backfill')
    [df['RSI_fastk'],df['RSI_fastd']] = talib.STOCHRSI(df[close], timeperiod=14)
    df['RSI_fastk']=df['RSI_fastk'].fillna(method='backfill')
    df['RSI_fastd']=df['RSI_fastd'].fillna(method='backfill')
    return(df)

#%%
def _add_cycle_indicator(df, close, fillna=False):
    df['HT_DCPERIOD'] = talib.HT_DCPERIOD(df[close])
    df['HT_DCPHASE'] = talib.HT_DCPHASE(df[close])
    [df['inphase'],df['quadrature']] = talib.HT_PHASOR(df[close])
    [df['sine'],df['leadsine']] = talib.HT_SINE(df[close])
    df['HT_TRENDMODE'] = talib.HT_TRENDMODE(df[close])

    if fillna:
        df['HT_DCPERIOD'] = df['HT_DCPERIOD'].replace([np.inf, -np.inf], np.nan).fillna(method='backfill')
        df['HT_DCPHASE'] = df['HT_DCPHASE'].replace([np.inf, -np.inf], np.nan).fillna(method='backfill')
        df['inphase'] = df['inphase'].replace([np.inf, -np.inf], np.nan).fillna(method='backfill')
        df['quadrature'] = df['quadrature'].replace([np.inf, -np.inf], np.nan).fillna(method='backfill')
        df['sine'] = df['sine'].replace([np.inf, -np.inf], np.nan).fillna(method='backfill')
        df['leadsine'] = df['leadsine'].replace([np.inf, -np.inf], np.nan).fillna(method='backfill')
        df['HT_TRENDMODE'] = df['HT_TRENDMODE'].replace([np.inf, -np.inf], np.nan).fillna(method='backfill')

    return df


#%%
def _add_stats(df, high, low, volume, opencolumn, window=50, fillna=False):
    df['CORREL'] = talib.CORREL(df[high], df[low], timeperiod=30)
    df['BETA'] = talib.BETA(df[high], df[low], timeperiod=5)

    if fillna:
        df['CORREL'] = df['CORREL'].replace([np.inf, -np.inf], np.nan).fillna(method='backfill')
        df['BETA'] = df['BETA'].replace([np.inf, -np.inf], np.nan).fillna(method='backfill')

    return df

#%%
def _add_normalized_ta(df, high, low, volume, opencolumn, window=50, fillna=False):
    # df['rolling_scaled_volume'] = timeseries_normalize_rolling(df[volume].values, np.arange(0,df.shape[0]), interval='rolling', mode='minmax', window=50, fillna=fillna, showfig=False)
    df['std_volume'] = df[volume].rolling(window=50).agg(['std'])
    
    if fillna:
        df['std_volume'] = df['std_volume'].replace([np.inf, -np.inf], np.nan).fillna(method='backfill')
    
    return df

#%%
def _add_close_only(df, close, fillna=False):
    df['volatility_dch'] = donchian_channel_hband(df[close], n=20, fillna=fillna)
    df['volatility_dcl'] = donchian_channel_lband(df[close], n=20, fillna=fillna)
    df['volatility_dchi'] = donchian_channel_hband_indicator(df[close], n=20, fillna=fillna)
    df['volatility_dcli'] = donchian_channel_lband_indicator(df[close], n=20, fillna=fillna)
    df['volatility_bbh'] = bollinger_hband(df[close], n=20, ndev=2, fillna=fillna)
    df['volatility_bbl'] = bollinger_lband(df[close], n=20, ndev=2, fillna=fillna)
    df['volatility_bbm'] = bollinger_mavg(df[close], n=20, fillna=fillna)
    df['volatility_bbhi'] = bollinger_hband_indicator(df[close], n=20, ndev=2, fillna=fillna)
    df['volatility_bbli'] = bollinger_lband_indicator(df[close], n=20, ndev=2, fillna=fillna)
    
    [macd, macdsignal, macdhist] = talib.MACD(df[close], fastperiod=12, slowperiod=26, signalperiod=9)
    df['trend_macd'] = macd
    df['trend_macd_signal'] = macdsignal
    df['trend_macd_diff'] = macdhist
    df['trend_ema_12'] = ema_indicator(df[close], n=12, fillna=fillna)
    df['trend_ema_26'] = ema_indicator(df[close], n=26, fillna=fillna)
    df['trend_ema_5'] = ema_indicator(df[close], n=5, fillna=fillna)
    df['trend_ema_20'] = ema_indicator(df[close], n=20, fillna=fillna)
    df['trend_ema_50'] = ema_indicator(df[close], n=50, fillna=fillna)
    df['trend_ema_100'] = ema_indicator(df[close], n=100, fillna=fillna)
    df['trend_ema_200'] = ema_indicator(df[close], n=200, fillna=fillna)
    df['trend_trix'] = trix(df[close], n=15, fillna=fillna)
    df['trend_dpo'] = dpo(df[close], n=20, fillna=fillna)
    df['trend_kst'] = kst(df[close], r1=10, r2=15, r3=20, r4=30, n1=10, n2=10, n3=10, n4=15, fillna=fillna)
    df['trend_kst_sig'] = kst_sig(df[close], r1=10, r2=15, r3=20, r4=30, n1=10, n2=10, n3=10, n4=15, nsig=9, fillna=fillna)
    df['trend_kst_diff'] = df['trend_kst'] - df['trend_kst_sig']
    df['trend_aroon_up'] = aroon_up(df[close], n=25, fillna=fillna)
    df['trend_aroon_down'] = aroon_down(df[close], n=25, fillna=fillna)
    df['trend_aroon_ind'] = df['trend_aroon_up'] - df['trend_aroon_down']

    df['momentum_rsi'] = rsi(df[close], n=14, fillna=fillna)
    df['momentum_tsi'] = tsi(df[close], r=25, s=13, fillna=fillna)

    df['DEMA_30'] = talib.DEMA(df[close], timeperiod=30).fillna(method='backfill')
    df['HT_TRENDLINE'] = talib.HT_TRENDLINE(df[close]).fillna(method='backfill')
    df['KAMA'] = talib.KAMA(df[close], timeperiod=30).fillna(method='backfill')
#    df['MAMA'] = talib.MAMA(df[close], fastlimit=0, slowlimit=0)
    df['T3'] = talib.T3(df[close], timeperiod=5, vfactor=0).fillna(method='backfill')
    df['TEMA'] = talib.TEMA(df[close], timeperiod=30).fillna(method='backfill')
    df['TRIMA'] = talib.TRIMA(df[close], timeperiod=30).fillna(method='backfill')
    df['WMA'] = talib.WMA(df[close], timeperiod=30).fillna(method='backfill')
    
    # Normalization of prices to avoid extreme volitality
    # df['rolling_scaled_close'] = timeseries_normalize_rolling(df[close].values, np.arange(0,df.shape[0]), interval='rolling', mode='minmax', window=50, fillna=fillna, showfig=False)
    df['std_close'] = df[close].rolling(window=50).agg(['std'])

    return df

#%%
def _add_volume_ta(df, high, low, close, volume, fillna=False):
    """Add volume technical analysis features to dataframe.

    Args:
        df (pandas.core.frame.DataFrame): Dataframe base.
        high (str): Name of 'high' column.
        low (str): Name of 'low' column.
        close (str): Name of 'close' column.
        volume (str): Name of 'volume' column.
        fillna(bool): if True, fill nan values.

    Returns:
        pandas.core.frame.DataFrame: Dataframe with new features.
    """
    df['volume_adi'] = acc_dist_index(df[high], df[low], df[close], df[volume], fillna=fillna)
    df['volume_obv'] = on_balance_volume(df[close], df[volume], fillna=fillna)
    df['volume_obvm'] = on_balance_volume_mean(df[close], df[volume], 10, fillna=fillna)
    df['volume_cmf'] = chaikin_money_flow(df[high], df[low], df[close], df[volume], fillna=fillna)
    df['volume_fi'] = force_index(df[close], df[volume], fillna=fillna)
    df['volume_em'] = ease_of_movement(df[high], df[low], df[close], df[volume], 14, fillna=fillna)
    df['volume_vpt'] = volume_price_trend(df[close], df[volume], fillna=fillna)
    df['volume_nvi'] = negative_volume_index(df[close], df[volume], fillna=fillna)
    
    df['volume_AD']             = talib.AD(df[high], df[low], df[close], df[volume]).fillna(method='backfill')
    df['volume_ADOSC']             = talib.ADOSC(df[high], df[low], df[close], df[volume]).fillna(method='backfill')
    df['volume_OBV'] = talib.OBV(df[close],df[volume]).fillna(method='backfill')

    return df

#%%
def _add_volatility_ta(df, high, low, close, fillna=False):
    """Add volatility technical analysis features to dataframe.

    Args:
        df (pandas.core.frame.DataFrame): Dataframe base.
        high (str): Name of 'high' column.
        low (str): Name of 'low' column.
        close (str): Name of 'close' column.
        fillna(bool): if True, fill nan values.

    Returns:
        pandas.core.frame.DataFrame: Dataframe with new features.
    """
    
#    print('VOLATILITY')
    df['volatility_atr'] = average_true_range(df[high], df[low], df[close], n=14, fillna=fillna)
    df['volatility_kcc'] = keltner_channel_central(df[high], df[low], df[close], n=10, fillna=fillna)
    df['volatility_kch'] = keltner_channel_hband(df[high], df[low], df[close], n=10, fillna=fillna)
    df['volatility_kcl'] = keltner_channel_lband(df[high], df[low], df[close], n=10, fillna=fillna)
    df['volatility_kchi'] = keltner_channel_hband_indicator(df[high], df[low], df[close], n=10, fillna=fillna)
    df['volatility_kcli'] = keltner_channel_lband_indicator(df[high], df[low], df[close], n=10, fillna=fillna)

    df['ATR']             = talib.ATR(df[high], df[low], df[close]).fillna(method='backfill')
    df['NATR']             = talib.NATR(df[high], df[low], df[close]).fillna(method='backfill')
    df['TRANGE']             = talib.TRANGE(df[high], df[low], df[close]).fillna(method='backfill')

    return df

#%%
def _add_trend_ta(df, high, low, close, fillna=False):
    """Add trend technical analysis features to dataframe.

    Args:
        df (pandas.core.frame.DataFrame): Dataframe base.
        high (str): Name of 'high' column.
        low (str): Name of 'low' column.
        close (str): Name of 'close' column.
        fillna(bool): if True, fill nan values.

    Returns:
        pandas.core.frame.DataFrame: Dataframe with new features.
    """

    df['trend_adxr']             = talib.ADXR(df[high], df[low], df[close], timeperiod=14).fillna(method='backfill')
    df['trend_adx']             = talib.ADX(df[high], df[low], df[close], timeperiod=14).fillna(method='backfill')
    df['trend_adx_pos']         = adx_pos(df[high], df[low], df[close], n=14, fillna=fillna)
    df['trend_adx_neg']         = adx_neg(df[high], df[low], df[close], n=14, fillna=fillna)
    df['trend_vortex_ind_pos']  = vortex_indicator_pos(df[high], df[low], df[close], n=14, fillna=fillna)
    df['trend_vortex_ind_neg'] = vortex_indicator_neg(df[high], df[low], df[close], n=14, fillna=fillna)
    df['trend_vortex_diff'] = abs(df['trend_vortex_ind_pos'] - df['trend_vortex_ind_neg'])
    df['trend_mass_index'] = mass_index(df[high], df[low], n=9, n2=25, fillna=fillna)
    df['trend_cci'] = cci(df[high], df[low], df[close], n=20, c=0.015, fillna=fillna)
    df['trend_ichimoku_a'] = ichimoku_a(df[high], df[low], n1=9, n2=26, fillna=fillna)
    df['trend_ichimoku_b'] = ichimoku_b(df[high], df[low], n2=26, n3=52, fillna=fillna)
    df['trend_visual_ichimoku_a'] = ichimoku_a(df[high], df[low], n1=9, n2=26, visual=True, fillna=fillna)
    df['trend_visual_ichimoku_b'] = ichimoku_b(df[high], df[low], n2=26, n3=52, visual=True, fillna=fillna)

    df['MIDPRICE']             = talib.MIDPRICE(df[high],df[low], timeperiod=14).fillna(method='backfill')
    df['SAR']             = talib.SAR(df[high],df[low], acceleration=0.02, maximum=0.2).fillna(method='backfill')
    df['SAREXT']             = talib.SAREXT(df[high],df[low]).fillna(method='backfill')
    df['SAREXT']             = talib.SAREXT(df[high],df[low]).fillna(method='backfill')


    return df

#%%
def _add_momentum_ta(df, high, low, close, volume, opencolumn, fillna=False):
    """Add trend technical analysis features to dataframe.

    Args:
        df (pandas.core.frame.DataFrame): Dataframe base.
        high (str): Name of 'high' column.
        low (str): Name of 'low' column.
        close (str): Name of 'close' column.
        fillna(bool): if True, fill nan values.

    Returns:
        pandas.core.frame.DataFrame: Dataframe with new features.
    """
    df['momentum_mfi'] = money_flow_index(df[high], df[low], df[close], df[volume], n=14, fillna=fillna)
    df['momentum_uo'] = uo(df[high], df[low], df[close], fillna=fillna)
    df['momentum_stoch'] = stoch(df[high], df[low], df[close], fillna=fillna)
    df['momentum_stoch_signal'] = stoch_signal(df[high], df[low], df[close], fillna=fillna)
    df['momentum_wr'] = wr(df[high], df[low], df[close], fillna=fillna)
    df['momentum_ao'] = ao(df[high], df[low], fillna=fillna)

    df['ADX'] = talib.ADX(df[high], df[low], df[close], timeperiod=14).fillna(method='backfill')
    df['ADXR'] = talib.ADXR(df[high], df[low], df[close], timeperiod=14).fillna(method='backfill')
    [df['aroondown'], df['aroonup']] = talib.AROON(df[high], df[low], timeperiod=14)
    df['aroondown']=df['aroondown'].fillna(method='backfill')
    df['aroonup']=df['aroonup'].fillna(method='backfill')
    df['AROONOSC'] = talib.AROONOSC(df[high], df[low], timeperiod=14).fillna(method='backfill')
    df['BOP'] = talib.BOP(df[opencolumn], df[high], df[low], df[close]).fillna(method='backfill')
    df['CCI'] = talib.CCI(df[high], df[low], df[close], timeperiod=14).fillna(method='backfill')
    df['DX'] = talib.DX(df[high], df[low], df[close], timeperiod=14).fillna(method='backfill')
    df['MFI'] = talib.MFI(df[high], df[low], df[close], df[volume], timeperiod=14).fillna(method='backfill')
    df['MINUS_DI'] = talib.MINUS_DI(df[high], df[low], df[close], timeperiod=14).fillna(method='backfill')
    df['MINUS_DM'] = talib.MINUS_DM(df[high], df[low], timeperiod=14).fillna(method='backfill')
    df['PLUS_DI'] = talib.PLUS_DI(df[high], df[low], df[close], timeperiod=14).fillna(method='backfill')
    df['PLUS_DM'] = talib.PLUS_DM(df[high], df[low], timeperiod=14).fillna(method='backfill')
    [df['STOCHF_fastk'],df['STOCHF_fastd']] = talib.STOCHF(df[high], df[low], df[close])
    df['STOCHF_fastk']=df['STOCHF_fastk'].fillna(method='backfill')
    df['STOCHF_fastd']=df['STOCHF_fastd'].fillna(method='backfill')
    df['ULTOSC'] = talib.ULTOSC(df[high], df[low], df[close]).fillna(method='backfill')
    df['WILLR'] = talib.WILLR(df[high], df[low], df[close]).fillna(method='backfill')

    return df

#%%
def _add_others_ta(df, close, fillna=False):
    """Add others analysis features to dataframe.

    Args:
        df (pandas.core.frame.DataFrame): Dataframe base.
        close (str): Name of 'close' column.
        fillna(bool): if True, fill nan values.

    Returns:
        pandas.core.frame.DataFrame: Dataframe with new features.
    """
    df['others_dr']  = daily_return(df[close], fillna=fillna)
    df['others_dlr'] = daily_log_return(df[close], fillna=fillna)
    df['others_cr']  = cumulative_return(df[close], fillna=fillna)
    df['rolling_return_50'] = rolling_return(df[close], window=50, fillna=fillna)
    df['rolling_return_200'] = rolling_return(df[close], window=200, fillna=fillna)

    # Statistic Functions
    df['LINEARREG_INTERCEPT'] = talib.LINEARREG_INTERCEPT(df[close], timeperiod=14)
    df['LINEARREG_SLOPE'] = talib.LINEARREG_SLOPE(df[close], timeperiod=14)
    df['LINEARREG_ANGLE'] = talib.LINEARREG_ANGLE(df[close], timeperiod=14)
    df['LINEARREG'] = talib.LINEARREG(df[close], timeperiod=14)
    df['TSF'] = talib.TSF(df[close], timeperiod=14)
    df['VAR'] = talib.VAR(df[close], timeperiod=5, nbdev=1)
    df['STDDEV'] = talib.STDDEV(df[close], timeperiod=5, nbdev=1)

    # Math Transform Functions
#    df['ACOS'] = talib.ACOS(df[close])
#    df['ASIN'] = talib.ASIN(df[close])
    df['ATAN'] = talib.ATAN(df[close])
    df['COS'] = talib.COS(df[close])
#    df['COSH'] = talib.COSH(df[close])
    df['SIN'] = talib.SIN(df[close])
#    df['SINH'] = talib.SINH(df[close])
    df['TAN'] = talib.TAN(df[close])
#    df['TANH'] = talib.TANH(df[close])

    if fillna:
#        df['ACOS'] = df['ACOS'].replace([np.inf, -np.inf], np.nan).fillna(method='backfill')
#        df['ASIN'] = df['ASIN'].replace([np.inf, -np.inf], np.nan).fillna(method='backfill')
        df['ATAN'] = df['ATAN'].replace([np.inf, -np.inf], np.nan).fillna(method='backfill')
        df['COS'] = df['COS'].replace([np.inf, -np.inf], np.nan).fillna(method='backfill')
#        df['COSH'] = df['COSH'].replace([np.inf, -np.inf], np.nan).fillna(method='backfill')
        df['SIN'] = df['SIN'].replace([np.inf, -np.inf], np.nan).fillna(method='backfill')
#        df['SINH'] = df['SINH'].replace([np.inf, -np.inf], np.nan).fillna(method='backfill')
        df['TAN'] = df['TAN'].replace([np.inf, -np.inf], np.nan).fillna(method='backfill')
#        df['TANH'] = df['TANH'].replace([np.inf, -np.inf], np.nan).fillna(method='backfill')

    if fillna:
        df['LINEARREG_INTERCEPT'] = df['LINEARREG_INTERCEPT'].replace([np.inf, -np.inf], np.nan).fillna(method='backfill')
        df['LINEARREG_SLOPE'] = df['LINEARREG_SLOPE'].replace([np.inf, -np.inf], np.nan).fillna(method='backfill')
        df['LINEARREG_ANGLE'] = df['LINEARREG_ANGLE'].replace([np.inf, -np.inf], np.nan).fillna(method='backfill')
        df['LINEARREG'] = df['LINEARREG'].replace([np.inf, -np.inf], np.nan).fillna(method='backfill')
        df['TSF'] = df['TSF'].replace([np.inf, -np.inf], np.nan).fillna(method='backfill')
        df['VAR'] = df['VAR'].replace([np.inf, -np.inf], np.nan).fillna(method='backfill')
        df['STDDEV'] = df['STDDEV'].replace([np.inf, -np.inf], np.nan).fillna(method='backfill')

    return df

#%%
def _add_patternrecognition(df, opencolumn, high, low, close, fillna=False):
    funcnames=['CDL2CROWS',
               'CDL3BLACKCROWS',
               'CDL3INSIDE',
               'CDL3LINESTRIKE',
               'CDL3OUTSIDE',
               'CDL3STARSINSOUTH',
               'CDL3WHITESOLDIERS',
               'CDLABANDONEDBABY',
               'CDLADVANCEBLOCK',
               'CDLBELTHOLD',
               'CDLBREAKAWAY',
               'CDLCLOSINGMARUBOZU',
               'CDLCONCEALBABYSWALL',
               'CDLCOUNTERATTACK',
               'CDLDARKCLOUDCOVER',
               'CDLDOJI',
               'CDLDOJISTAR',
               'CDLDRAGONFLYDOJI',
               'CDLENGULFING',
               'CDLEVENINGDOJISTAR',
               'CDLEVENINGSTAR',
               'CDLGAPSIDESIDEWHITE',
               'CDLGRAVESTONEDOJI',
               'CDLHAMMER',
               'CDLHANGINGMAN',
               'CDLHARAMI',
               'CDLHARAMICROSS',
               'CDLHIGHWAVE',
               'CDLHIKKAKE',
               'CDLHIKKAKEMOD',
               'CDLHOMINGPIGEON',
               'CDLIDENTICAL3CROWS',
               'CDLINNECK',
               'CDLINVERTEDHAMMER',
               'CDLKICKING',
               'CDLKICKINGBYLENGTH',
               'CDLLADDERBOTTOM',
               'CDLLONGLEGGEDDOJI',
               'CDLLONGLINE',
               'CDLMARUBOZU',
               'CDLMATCHINGLOW',
               'CDLMATHOLD',
               'CDLMORNINGDOJISTAR',
               'CDLMORNINGSTAR',
               'CDLONNECK',
               'CDLPIERCING',
               'CDLRICKSHAWMAN',
               'CDLRISEFALL3METHODS',
               'CDLSEPARATINGLINES',
               'CDLSHOOTINGSTAR',
               'CDLSHORTLINE',
               'CDLSPINNINGTOP',
               'CDLSTALLEDPATTERN',
               'CDLSTICKSANDWICH',
               'CDLTAKURI',
               'CDLTASUKIGAP',
               'CDLTHRUSTING',
               'CDLTRISTAR',
               'CDLUNIQUE3RIVER',
               'CDLUPSIDEGAP2CROWS',
               'CDLXSIDEGAP3METHODS',
               ]
    
    for i in range(0,len(funcnames)):
        fn = getattr(talib, funcnames[i])
        df[funcnames[i]] = fn(df[opencolumn], df[high], df[low], df[close])
        if fillna:
            df[funcnames[i]] = df[funcnames[i]].replace([np.inf, -np.inf], np.nan).fillna(method='backfill')

    return df



