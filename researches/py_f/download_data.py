import yfinance as yf
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd

# Получение данных о ценах закрытия акций AAPL за последние три года
paper = 'tsla'
interval = '1d'
end_date = datetime.today()
if interval in ['1h']:
    start_date = end_date - timedelta(days=729)
elif interval in ['1d']:
    start_date = end_date - timedelta(days=3*365)
data = yf.download(paper, start=start_date, end=end_date, interval=interval)

# Расчет индикаторов
data['Moving Average'] = data['Adj Close'].rolling(window=100).mean()
data['Donchian High'] = data['High'].rolling(window=100).max()
data['Donchian Low'] = data['Low'].rolling(window=100).min()
data['Donchian Mid'] = (data['Donchian High'] + data['Donchian Low']) / 2

last_close = data['Close'].iloc[-1]
last_donchian_mid = data['Donchian Mid'].iloc[-1]

percent_change = ((last_close - last_donchian_mid) / last_close) * 100
print(f"Процентное изменение от последнего Close до Donchian Mid: {percent_change:.2f}%")


# Построение графика
plt.figure(figsize=(12, 6))
plt.plot(data['Adj Close'], label='AAPL Close Price')
plt.plot(data['Moving Average'], label='100-day Moving Average')
plt.plot(data['Donchian High'], label='Donchian High', linestyle='--')
plt.plot(data['Donchian Low'], label='Donchian Low', linestyle='--')
plt.plot(data['Donchian Mid'], label='Donchian Mid', linestyle=':')
plt.title('AAPL Stock Price with Indicators')
plt.legend()
plt.savefig(r'C:\py_projects\pairs_flask\app\static\img\aapl_chart.png')
