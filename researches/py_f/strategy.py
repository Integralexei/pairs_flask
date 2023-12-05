import pandas as pd
import plotly.graph_objects as go

# Загрузка и подготовка данных
data_df = pd.read_json('h_data.json')
data_df['date'] = pd.to_datetime(data_df['timestamp'], unit='ms')
data_df.set_index('date', inplace=True)

# Выбор данных за последние три года
latest_date = data_df.index.max()
three_years_ago = latest_date - pd.DateOffset(years=3)
three_years_data = data_df[data_df.index >= three_years_ago]
three_years_data.drop('timestamp', axis=1, inplace=True)



# Расчет канала Дончиана
donchian_period = 100
three_years_data['high_100'] = three_years_data['high'].rolling(window=donchian_period).max()
three_years_data['low_100'] = three_years_data['low'].rolling(window=donchian_period).min()
three_years_data['mid_ch'] = (three_years_data['high_100'] + three_years_data['low_100']) / 2
three_years_data = three_years_data.sort_values(by='date')



# Определение точек входа
three_years_data['entry_signal'] = (
    (three_years_data['close'] > three_years_data['mid_ch']) &
    (three_years_data['close'].shift(1) < three_years_data['mid_ch'].shift(1)) & 
    (three_years_data['close'].shift(2) < three_years_data['mid_ch'].shift(2))
)
three_years_data.dropna(inplace=True)

# Расчет стоп-лосса и тейк-профита
three_years_data['stop_loss'] = three_years_data['low'] * (1 - 0.001)
three_years_data['take_profit'] = three_years_data['open'] + (three_years_data['open'] - three_years_data['stop_loss'])
three_years_data['shifted_entry_signal'] = three_years_data['entry_signal'].shift(1) #сохдаем строку что бы входить по не на следующем open  а не по close


# Функция для тестирования торговой стратегии
def test_trading_strategy(data):
    in_position = False
    entry_price = None
    stop_loss_price = None
    take_profit_price = None
    trades = []

    for index, row in data.iterrows():
        if in_position:
            if row['close'] <= stop_loss_price or row['close'] >= take_profit_price:
                trades.append({'date': index, 'price': row['close'], 'type': 'sell'})
                in_position = False
        else:
            if row['shifted_entry_signal']:
                entry_price = row['open']
                stop_loss_price = row['stop_loss']
                take_profit_price = row['take_profit']
                trades.append({'date': index, 'price': entry_price, 'type': 'buy', 'sl': stop_loss_price, 'tp': take_profit_price})
                in_position = True
    for i in trades:
        print(i)
    return trades

# Применение стратегии и получение сделок
trades = test_trading_strategy(three_years_data)


# Создание графика
fig = go.Figure()

# Добавление линии цены закрытия
fig.add_trace(go.Scatter(x=three_years_data.index, y=three_years_data['close'], mode='lines', name='Close Price'))
# Добавление средней линии канала Дончиана
fig.add_trace(go.Scatter(x=three_years_data.index, y=three_years_data['mid_ch'], mode='lines', name='Donchian Mid Channel', line=dict(color='orange', width=2)
))

# Добавление точек сделок
for trade in trades:
    fig.add_trace(go.Scatter(
        x=[trade['date']], y=[trade['price']], mode='markers', 
        marker_symbol='circle', marker_line_color='black', 
        marker_color='green' if trade['type'] == 'buy' else 'red', 
        marker_line_width=2, marker_size=10, 
        name=f"{trade['type'].title()} @ {trade['price']}"
    ))



# Настройки графика
fig.update_layout(
    title='SPY Trading Strategy Performance', 
    xaxis_title='Date', 
    yaxis_title='Price', 
    legend_title='Legend', 
    template='plotly_dark',
    autosize=False,
    width=1500,
    height=800,
    margin=dict(
        l=10,
        r=10,
        b=20,
        t=20,
        pad=1
    ),
)

# fig.show()

plot_file_path = 'plot_strat.html'
fig.write_html(plot_file_path)