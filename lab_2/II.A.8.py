import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import make_interp_spline
import numpy as np

# qulity level over time
# price over time
# and the price vs qulity level

# simulation time = 24 hours

def price_time_simulation(file):
    df =pd.read_csv(file)

    time = df['time']
    price = df['price']

    plt.figure(figsize=(10,6))
    plt.plot(time, price, linestyle='-')
    plt.title('task II.A.8')
    plt.xlabel('Time (minutes)')
    plt.ylabel('Price (NOK)')

    plt.grid(False)
    plt.show()


def quality_time_simulation(file):
    df = pd.read_csv(file)

    df_median = df.groupby('time')['quality'].median().reset_index()
    # print(quality_collumn)
    df_median.to_csv('result.csv', index=False)

    df_2 = pd.read_csv('result.csv')

    time = df_2['time']
    quality = df_2['quality']


    plt.figure(figsize=(16,6))
    plt.plot(time, quality, linestyle='-')
    plt.title('task II.A.8')
    plt.xlabel('Time (minutes)')
    plt.ylabel('Quality (MOS-score)')

    plt.grid(False)
    plt.show()





if __name__ == "__main__":

    price_time_simulation('price-time.csv')

    quality_time_simulation('quality-time.csv')

