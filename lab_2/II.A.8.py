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


    time_price_spline = make_interp_spline(time, price)

    time2 = np.linspace(time.min(), time.max(), 500)
    price2 = time_price_spline(time2)

    plt.figure(figsize=(10,6))
    plt.plot(time2, price2, marker='o', linestyle='-')
    plt.title('task II.A.8')
    plt.xlabel('Time')
    plt.ylabel('Price')

    plt.grid(False)
    plt.show()


def quality_time_simulation(file):
    df =pd.read_csv(file)

    time = df['time']
    quality = df['quality']

    plt.figure(figsize=(10,6))
    # plt.plot(time, quality, marker='o', linestyle='-')
    plt.plot(time, quality)
    plt.title('task II.A.8')
    plt.xlabel('Time')
    plt.ylabel('Quality')

    plt.grid(False)
    plt.show()





if __name__ == "__main__":

    # price_time_simulation('price_time.csv')

    quality_time_simulation('quality-time.csv')

