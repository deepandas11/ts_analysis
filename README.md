# Time Series Analysis:

## Getting Started: 
### Time Series Introduction:

This section would briefly introduce you to the core concepts in Time Series analysis and would serve as a primer before we delve into the code. 

Time series analysis can be applied to different kinds of data and can be used to answer questions like:**"*What could be the average number of passengers for an airline company next month?*"** or something like **"*What could be the stock price of Apple tomorrow?*"** :boom:

>**Definition**: A univariate time series is a sequence of measurements of the same variable collected over time.  Most often, the measurements are made at regular time intervals.


The following **factors** need to be considered when analyzing a time series: 

1. Is there an overall **trend** to the time series? This could imply the existence of a long-term increase or decrease in the measurements.
2. Is there a repeating pattern of highs or lows in the measurements, determined by the **seasonality** of the data.
3. Are there data points that are very far away from the other data points, commonly known as **outliers** ? This is the non-systematic component of the time-series. 


#### Analysis Tasks

The following tasks are the constitutents of Time Series Analysis:

**1. Smoothing:** The Time Series measurements can be estimated as the sum of the systematic output and a noise component. Smoothing aims to estimate the systematic output by trying to nullify the effect of the noise component. Usually, averaging methods are used. 

>***Why is Regression not used?***
Ans: In regression, each observation is independent. However, in time series, observations are time-dependent and may have a trend and seasonality component. 

**2. Modelling:** This helps in the development of a simple mathematical tool that explains observed patterns of the output and explains how it depends on unknown parameters, which are consequently estimated.

**3. Forecasting:** This aims to predict future observations from known past observations.


**4. Control:** Intervention with the process which is producing the output values. 


### Time Series Modeling

1. **White Noise:** This is a purely random model. The observations have the following features:

                    - Zero mean
                    - Constant Variance
                    - Uncorrelated random variable
2. **Auto-Regression:** Current observation depends on previous observations. 

                    - Output is a linear combination of previous observations weighted by parameters
                    - Task is to estimate parameters correctly
 
3. **Moving Average:** Current observation depends on previous random error terms which follow a white noise process. 

                    - Output is a linear combination of previous random error terms weighted by parameters
                    - Task is to estimate parameters correctly

2. **ARMA:** Combination of both AR and MA models.

                    - Output is a linear combination of previous random error terms and previous observations weighted by two distinct parameter sets.
                    - Task is to estimate parameters correctly
                    
                     
                     
#### Smoothing 

1. **Moving Average:** Calculates the average of the last n observations. 

    ```python
    numpy.average(series[-n:])`
    ```
    
The above piece of code should do the trick.

2. **Weighted Average:** A weight vector is multiplied with the observation values in the window. The weights add emphasis on cetain observations, and it is desirable that more recent observations are weighed heavily.

```python

def weighted_average(series, weights):
    result = 0.0
    weights.reverse()
    for n in range(len(weights)):
        result += series.iloc[-n-1] * weights[n]
    return float(result)
```

3. **Exponential Smoothing:** This is the rule of thumb technique to smooth a time series. Assigns exponentially deceasing weights over time over observation window. The factor alpha is called the smoothing factor and can be thought of as how quickly we will forget the last available true observation. The smaller alpha is the more influence the previous observations will have and smoother the series is. 

```python
   def exponential_smoothing(series, alpha):
   
    result = [series[0]] # first value is same as series
    for n in range(1, len(series)):
        result.append(alpha * series[n] + (1 - alpha) * result[n-1])
    return result
```

4. **Double Exponential Smoothing:** This enables us to predict two values in the future instead of one value and includes more smoothing. This includes the concept of trend in the smoothing event

```python
def double_exponential_smoothing(series, alpha, beta):
    result = [series[0]]
    trends = [series[0]]
    levels = [series[0]]
    for n in range(1, len(series)+1):
        if n == 1:
            level, trend = series[0], series[1] - series[0]
        if n >= len(series): # forecasting
            value = result[-1]
        else:
            value = series[n]
        last_level, level = level, alpha*value + (1-alpha)*(level+trend)
        trend = beta*(level-last_level) + (1-beta)*trend
        result.append(level+trend)
        trends.append(trend)
        levels.append(level)
    return result,levels,trends
```


 
#### Checking Stationarity of a Time Series

>Definition: If marginal distribution of output at a time t is the same at any other instant of time, it is a stationary series.

A non stationary series could be made stationary by differencing or differentiating. After d steps of differencing operations, the non stationary series becomes an integrated stationary series of order d. Therefore, an order 0 corresponds to a Stationary Series. 

If we observe an overall increasing trend along with some seasonal variables then we can infer non-stationarity. Two rigorous methods to check the stationarity of a time series are:

1. **Plotting Rolling Statistics:** We plot the moving average or moving variance and check if it varies with time. This is again, a visual technique.

2. **Dickey-Fuller Test:** Statistical test to check stationarity. The Null hypothesis states that the Time series is non stationary and the test result comprises of a Test Statistic and some critical values for different confident intervals. If Test Value is less than the critical value, we reject the null hypothesis and say the series is stationary. 

 
 #### Making a Time Series Stationary
 
 There are two major reasons behind Non stationarity as discussed before: Trend and Seasonality. 
 The underlying principle is to model or estimate the trend and seasonality in the series and remove them to get stationarity. The forecasted value would then have to be converted back to original scale by applying the trend and seasonality. 
 
 
### Forecasting a Time Series

In a time series with a significant dependence among values, we need a statistical model like **ARIMA** to forecast the data. The ARIMA forecasting for a stationary time series is nothing but a linear (like a linear regression) equation. The predictors depend on the parameters (p,d,q) of the ARIMA model. We determine the values of p and q from the **ACF and PACF** plots.

1. **p - (Number of AR terms):** AR terms are just lags of dependent variable. The lag value where the PACF chart crosses the upper confidence interval for the first time.
2. **q - (Number of MA terms):** MA terms are lagged forecast errors in the prediction equation. The lag value where the ACF chart crosses the upper confidence interval for the first time.
3. **d - (Number of differences):** These are the number of nonseasonal difference.


## Navigation :sparkle:

All codes, datasets and results can be found inside the folder timeseries_analysis. ***Ignore*** the initial commits.

1. **Smoothing:** Folder contains code and results as plots for smoothing time series data. 
2. **Forecasting:** Folder contains code and results as plots for forecasting using ARIMA.

Datasets:
1. For smoothing task, the Apple stock prices dataset has been used.
2. For the forecasting task, the Airplane passengers dataset has been used. 




## Thank you! :smile: 
 
 
 
 
Find me here: <div class="LI-profile-badge"  data-version="v1" data-size="medium" data-locale="en_US" data-type="vertical" data-theme="light" data-vanity="deepan-das-944b49b0"><a class="LI-simple-link" href='https://in.linkedin.com/in/deepan-das-944b49b0?trk=profile-badge'>Deepan Das</a></div>
