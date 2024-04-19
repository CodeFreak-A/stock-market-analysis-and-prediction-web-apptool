import pandas as pd
dataset = pd.read_csv("C:\\Users\\HP\\Downloads\\Stock-Price-Prediction-Project-Code\\NSE-Tata.csv")
dataset = dataset.reset_index()
dataset['Date'] = pd.to_datetime(dataset['Date'])
dataset.set_index('Date', inplace=True)
dataset = dataset['Close'].to_frame()


from pmdarima.arima import auto_arima

model = auto_arima(dataset['Close'], seasonal=False, trace=True)
print(model.summary())

from statsmodels.tsa.arima.model import ARIMA
import numpy as np

def arima_forecast(history):
    model = ARIMA(history, order=(0,1,0))
    model_fit = model.fit()

    output = model_fit.forecast()
    yhat = output[0]
    return yhat

X = dataset.values
size = int(len(X) * 0.8)
train, test = X[0:size], X[size:len(X)]

history = [x for x in train]
predictions = list()
for t in range(len(test)):
    yhat = arima_forecast(history)
    predictions.append(yhat)
    obs = test[t]
    history.append(obs)

import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6), dpi=100)
plt.plot(dataset.iloc[size:,:].index, test, label='Real Value')
plt.plot(dataset.iloc[size:,:].index, predictions, color='red', label='Predicted Value')
plt.title('ARIMA Predictions vs Actual Values')
plt.xlabel('Date')
plt.ylabel('Stock Price')
plt.legend()
plt.show()