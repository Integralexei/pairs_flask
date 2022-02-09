import matplotlib.pyplot as plt
from pairs_data import get_data

# print(get_data('AAPL')['Close'].values)
aapl = get_data('AAPL')['Close']
msft = get_data('MSFT')['Close']
# create data
first_x = aapl.index
first_y = aapl.values

second_x = msft.index
second_y = msft.values

# # plot liness
plt.plot(first_x, first_y, label = "line 1")
plt.plot(second_x, second_y, label = "line 2")
plt.legend()
plt.grid()
plt.savefig('app\static\img\chart1.png')