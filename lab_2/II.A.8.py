import matplotlib.pyplot as plt
import pandas as pd

# qulity level over time
# price over time
# and the price vs qulity level

# simulation time = 24 hours



df =pd.read_csv('output.csv')

time = df['time']
price = df['price']

plt.figure(figsize=(10,6))
plt.plot(time, price, marker='o', linestyle='-')
plt.title('task II.A.8')
plt.xlabel('Time')
plt.ylabel('Price')

plt.grid(False)
plt.show()

