import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.options.display.float_format = '{:.5f}'.format

plt.style.use("seaborn")

data = pd.read_csv("bitcoin.csv", parse_dates=["Date"], index_col="Date")
data = data[["Close", "Volume"]].copy()
data.Close.plot(figsize=(12, 8), title="BTC/USDT", fontsize=12)
data.Volume.plot(figsize=(12, 8), title="BTC/USDT", fontsize=12)
data.Volume.loc["2021"].plot(figsize=(12, 8), title="BTC/USDT", fontsize=12)
data["returns"] = np.log(data.Close.div(data.Close.shift(1)))
data.returns.plot(kind="hist", bins=100, figsize=(12, 8))
data.returns.nlargest(10)
data.returns.nsmallest(10)
data.Close / data.Close[0]
data.returns.sum()
multiple = np.exp(data.returns.sum())
data["creturns"] = data.returns.cumsum().apply(np.exp)
data.Close / data.Close[0]
data.creturns.plot(figsize=(12, 8), title="BTC/USDT - Buy and Hold", fontsize=12)
