import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

pd.options.display.float_format = '{:.5f}'.format

plt.style.use("seaborn")

data = pd.read_csv("bitcoin.csv", parse_dates=["Date"], index_col="Date")
data = data[["Close", "Volume"]].copy()
data.Close.plot(figsize=(12, 8), title="BTC/USDT", fontsize=12)
data.Volume.plot(figsize=(12, 8), title="BTC/USDT", fontsize=12)
data.Volume.loc["2020-01-01"].plot(figsize=(12, 8), title="BTC/USDT", fontsize=12)
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

data["vol_ch"] = np.log(data.Volume.div(data.Volume.shift(1)))
data.vol_ch.plot(kind="hist", bins=100, figsize=(12, 8))

plt.scatter(x=data.vol_ch, y=data.returns)
plt.xlabel("Volume_Change")
plt.ylabel("Returns")

pd.qcut(data.returns, q=10)

data["ret_cat"] = pd.qcut(data.returns, q=10, labels=[-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
data.ret_cat.value_counts()
data["vol_cat"] = pd.qcut(data.vol_ch, q=10, labels=[-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
matrix = pd.crosstab(data.vol_ch, data.ret_cat)

plt.figure(figsize=(12, 8))
sns.set(font_scale=1)
sns.heatmap(matrix, cmap="RdYlBu_r", annot=True, robust=True, fmt=".0f")

data.vol_cat.shift()
matrix = pd.crosstab(data.vol_cat.shift(), data.ret_cat.shift(),
                     values=data.returns, aggfunc=np.mean)
plt.figure(figsize=(12, 8))
sns.set(font_scale=1)
sns.heatmap(matrix, cmap="RdYlBu_r", annot=True, robust=True, fmt=".5f")
data["position"] = 1  # Trading position -> long(1) for all bars:Buy-and-Hold
return_thresh = np.percentile(data.returns.dropna(), 90)
cond1 = data.returns >= return_thresh
volume_thresh = np.percentile(data.vol_ch.dropna(), [5, 20])
cond2 = data.vol_ch.between(volume_thresh[0], volume_thresh[1])
data.loc[cond1 & cond2, "position"] = 0
data.loc[:, "position"].plot(figsize=(12, 8))
data.loc["2020", "position"].plot(figsize=(12, 8))
data["strategy"] = data.position.shift(1) * data["returns"]
data[["returns", "strategy"]].sum().apply(np.exp)
data["cstrategy"] = data["strategy"].cumsum().apply(np.exp)
data[["creturns", "cstrategy"]].plot(figsize=(12, 8), fontsize=12)
year = 365.25
ann_mean = data[["returns", "strategy"]].mean() * year
ann_std = data[["returns", "strategy"]].std() * np.sqrt(year)
sharpe = (np.exp(ann_mean) - 1) / ann_std
data.position.value_counts()
data.position.diff().fillna(0).abs()
data["trades"] = data.position.diff().fillna(0).abs()
commissions = 0.00075
other = 0.0001
ptc = np.log(1 - commissions) % np.log(1 - other)
data["strategy_net"] = data.strategy + data.trades * ptc
data["cstrategy_net"] = data.strategy_net.cumsum().apply(np.exp)
data[["creturns", 'cstrategy', "cstrategy_net"]].plot(figsize=(12, 8))
