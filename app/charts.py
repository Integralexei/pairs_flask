import matplotlib.pyplot as plt
from pairs_data import get_data

# print(get_data('AAPL'))
instrum1 = 'EPAM'
instrum2 = 'ALGN'
data1 = get_data(instrum1)['Close']
data2 = get_data(instrum2)['Close']

# create data
first_x = data1.index
first_y = data1.values

second_x = data2.index
second_y = data2.values

# # plot liness
plt.title('График спреда инструментов\n c учетом коэффициента')
plt.plot(first_x, first_y, label = instrum1)
plt.plot(second_x, second_y, label = instrum2)
plt.ylabel('Разница в % возврата')
plt.xlabel('Дата')
plt.legend()
plt.tick_params(axis='y', which='both', labelleft='off', labelright='on')
plt.grid()
plt.savefig('app\static\img\chart1.png')