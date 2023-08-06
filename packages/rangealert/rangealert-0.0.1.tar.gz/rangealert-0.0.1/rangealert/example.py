import pandas as pd
import pandas_datareader as pdr
from ralert import *
# import plotly.graph_objects as go
# import ta

rs = range_screen()

tickers = ['AAPL', 'CAT', 'GE']
start_date = '2020-01-01'
end_date = '2021-12-31'

panel_data = pdr.DataReader(tickers, 'yahoo', start_date, end_date)
df = panel_data.stack().reset_index()
df['Date'] = pd.to_datetime(df['Date'])
df['Close'] = df['Close'] * df['Adj Close'] / df['Close']
df['Open'] = df['Open'] * df['Adj Close'] / df['Close']
df['High'] = df['High'] * df['Adj Close'] / df['Close']
df['Low'] = df['Low'] * df['Adj Close'] / df['Close']
df = df.set_index('Date')

symbol = 'CAT'
df1 = df[df['Symbols']==symbol]


signal, fig = rs.range_trading(df1, symbol, atr_window=14, range_periods=55, atrmultiple_test=1.5, create_chart=True)
signal, fig = rs.range_trading(df1, symbol, atr_window=14, range_periods=5, atrmultiple_test=1.5, create_chart=True)
fig.show()
rs.last_open
rs.last_high
rs.last_low
rs.last_close
rs.last_tradingDay
rs.last_atr
rs.avelow
rs.avehigh
rs.avemidprice
rs.rangemaxprice
rs.rangeminprice
rs.last_maxprice
rs.last_minprice
rs.last_upb
rs.last_lpb
rs.last_atr
rs.upb
rs.lpb

fig = rs.get_range_plot(df1, symbol, rs.upb, rs.lpb, rs.rangemaxprice, rs.rangeminprice)
fig.show()

fig = go.Figure()
trace1=go.Candlestick(x=df1.index, open=df1['Open'], high=df1['High'], low=df1['Low'], close=df1['Close'], name=symbol)
trace2 = go.Scatter(x=rs.upb.index, y=rs.upb.values, mode='lines', line_color='blue', name='Upper price band')
trace3 = go.Scatter(x=rs.lpb.index, y=rs.lpb.values, mode='lines', line_color='blue', name='Lower price band')
trace4 = go.Scatter(x=rs.rangemaxprice.index, y=rs.rangemaxprice.values, mode='lines', line_color='black', name='Max price')
trace5 = go.Scatter(x=rs.rangeminprice.index, y=rs.rangeminprice.values, mode='lines', line_color='black', name='Min price')

fig.add_trace(trace1)
fig.add_trace(trace2)
fig.add_trace(trace3)
fig.add_trace(trace4)
fig.add_trace(trace5)

fig.update(layout_xaxis_rangeslider_visible=False)
fig.update_layout(
title='Range Trading Analysis: ' + symbol,
xaxis_title="Date",
yaxis_title="Price")
fig.show()
