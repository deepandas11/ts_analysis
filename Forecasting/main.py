#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 00:17:16 2018
forecasting
@author: deepan
Link:  https://www.analyticsvidhya.com/blog/2016/02/time-series-forecasting-codes-python/
"""

import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from matplotlib.pylab import rcParams
rcParams['figure.figsize'] = 8,4
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.tsa.arima_model import ARIMA



dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m')
data = pd.read_csv('AirPassengers.csv', parse_dates=['Month'], index_col='Month',date_parser=dateparse)


ts = data['#Passengers']

plt.figure(1)
plt.plot(ts)
plt.grid('on')
plt.title('Overall Air Passengers Data')
plt.show()


a_diff = ts - ts.shift(12)
a_dif = a_diff


def test_stationarity(timeseries):
    
    rolmean = pd.rolling_mean(timeseries, window = 12)
    rolstd = pd.rolling_std(timeseries, window = 12)
    
    orig = plt.plot(timeseries, color='blue', label = 'Original')
    mean = plt.plot(rolmean, color = 'red', label='Rolling Mean')
    stdd = plt.plot(rolstd, color = 'black', label = 'Rolling STD')
    #wseason = plt.plot(a_diff['1950-01-01':], color = 'yellow',  label = 'WS' )
    
    
    
    plt.legend(loc = 'best')
    plt.title('Airplane Passengers Data')
    plt.grid('on')
    plt.show(block = False)
    
    print 'Results of Dickey-Fuller Test:'
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    print dfoutput
    
    
test_stationarity(ts)
'''
plt.figure(2)
ts_log = plt.plot(np.log(ts), color = 'green', label='Log')
'''


ts_log = np.log(ts)
mov_av = pd.rolling_mean(ts_log, 12)
expwighted_avg = pd.ewma(ts_log, halflife=12)
ts_log_movavg_diff = ts_log - mov_av
ts_log_movavg_diff.dropna(inplace=True)
ts_log_ewma_diff = ts_log - expwighted_avg

test_stationarity(ts_log_movavg_diff)
test_stationarity(ts_log_ewma_diff)


ts_log_diff = ts_log - ts_log.shift()
ts_log_diff.dropna(inplace=True)
test_stationarity(ts_log_diff)

#ACF PACF Plots
lag_acf = acf(ts_log_diff, nlags=20)
lag_pacf = pacf(ts_log_diff, nlags=20, method='ols')

plt.figure(2)
plt.subplot(121) 
plt.plot(lag_acf)
plt.axhline(y=0,linestyle='--',color='gray')
plt.axhline(y=-1.96/np.sqrt(len(ts_log_diff)),linestyle='--',color='gray')
plt.axhline(y=1.96/np.sqrt(len(ts_log_diff)),linestyle='--',color='gray')
plt.title('Autocorrelation Function')
plt.grid('on')
plt.subplot(122)
plt.plot(lag_pacf)
plt.axhline(y=0,linestyle='--',color='gray')
plt.axhline(y=-1.96/np.sqrt(len(ts_log_diff)),linestyle='--',color='gray')
plt.axhline(y=1.96/np.sqrt(len(ts_log_diff)),linestyle='--',color='gray')
plt.title('Partial Autocorrelation Function')
plt.grid('on')
plt.tight_layout()
plt.show()


#FORECAST
model = ARIMA(ts_log, order=(2, 1, 2))  
results_ARIMA = model.fit(disp=-1)  
plt.figure(3)
plt.plot(ts_log_diff)
plt.plot(results_ARIMA.fittedvalues, color='red')
plt.title('RSS: %.4f'% sum((results_ARIMA.fittedvalues-ts_log_diff)**2))


predictions_ARIMA_diff = pd.Series(results_ARIMA.fittedvalues, copy=True)
predictions_ARIMA_diff_cumsum = predictions_ARIMA_diff.cumsum()
predictions_ARIMA_log = pd.Series(ts_log.ix[0], index=ts_log.index)
predictions_ARIMA_log = predictions_ARIMA_log.add(predictions_ARIMA_diff_cumsum,fill_value=0)
predictions_ARIMA = np.exp(predictions_ARIMA_log)


plt.figure(4)
plt.plot(ts)
plt.plot(predictions_ARIMA)
plt.grid('on')
plt.title('RMSE: %.4f'% np.sqrt(sum((predictions_ARIMA-ts)**2)/len(ts)))
plt.show()