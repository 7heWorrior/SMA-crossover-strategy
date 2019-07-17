# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 23:45:34 2019

@author: Manas
"""

import quandl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


SO = quandl.get("NSE/MRF")

t= SO.tail()

SO['Close'].plot(grid=True)
plt.title("NSE MRF - (Closing prices in ₹)")
plt.show

#Making short and long windows
short_window = 40 
long_window = 100
signals = pd.DataFrame(index=SO.index)
signals['signal'] = 0.0
#SMA of short window
signals['short_mavg'] = SO['Close'].rolling (window=short_window, min_periods=1, center=False).mean()
#SMA for long Window4
signals['long_mavg'] = SO['Close'].rolling (window=long_window, min_periods=1, center=False).mean()
#Create signals
signals['signal'][short_window:] = np.where(signals['short_mavg'][short_window:]>signals['long_mavg'][short_window:],1.0,0.0)


signals['positions'] = signals['signal'].diff()
print(signals)

fig = plt.figure(figsize=(20,15))

ax1 = fig.add_subplot(111, ylabel='Price in ₹')
SO['Close'].plot(ax=ax1, color='black', lw=2.)

signals[['short_mavg', 'long_mavg']].plot(ax=ax1, lw=2.)

ax1.plot(signals.loc[signals.positions == 1.0].index, signals.short_mavg[signals.positions == 1.0],'^', markersize=10, color='g')

ax1.plot(signals.loc[signals.positions == -1.0].index, signals.short_mavg[signals.positions == -1.0],'v', markersize=10, color='r')

plt.show()

#set the intial capital
intial_capital = float (100000)

#create a dataframe 'positions'
positions = pd.DataFrame(index=signals.index).fillna(0.0)

#buy a 1000 shares
positions['positions in NSE'] = 1000*signals['signal']

#Intialize the portfolio with value owned
portfolio = positions.multiply(SO['Close'], axis=0)

#Store the difference in shares owned
pos_diff = positions.diff()

#Add 'holdings' to portfolio
portfolio['holdings'] = (positions.multiply(SO['Close'],axis=0)).sum(axis=1)

#add 'cash' to portfolio
portfolio['cash'] = intial_capital - (pos_diff.multiply(SO['Close'], axis=0)).sum(axis=1).cumsum()
#add 'total' to portfolio
portfolio['total'] = portfolio['cash'] + portfolio['holdings']

#add 'returns' to portfolio
portfolio['returns'] = portfolio['total'].pct_change()

del portfolio['positions in NSE']
#print the first lines of 'portfolio'
print(portfolio)



fig = plt.figure(figsize=(20,15))

ax1 = fig.add_subplot(111, ylabel='portfolio value in INR')
SO['Close'].plot(ax=ax1, color='black', lw=2.)

portfolio['total'].plot(ax=ax1, lw=2.)

ax1.plot(portfolio.loc[signals.positions == 1.0].index, portfolio.total[signals.positions == 1.0],'^', markersize=20, color='g')

ax1.plot(portfolio.loc[signals.positions == -1.0].index, portfolio.total[signals.positions == -1.0],'v', markersize=20, color='r')

plt.show()