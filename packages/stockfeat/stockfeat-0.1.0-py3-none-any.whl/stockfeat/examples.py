# %%
from stockfeat import stockfeat
print(dir(stockfeat))
# import stockfeat
# print(stockfeat.__version__)

# %%
sf = stockfeat(col_open='Open', col_close='Close', col_volume='Volume', col_high='High', col_low='Low')
df = sf.download_example()
df = df.resample('D').mean()

# %% Collect features
X = sf.fit(df)
