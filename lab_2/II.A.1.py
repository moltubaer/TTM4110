# ----- Lab II ----- #
# ----- II.A.1 ----- #

import simpy
import numpy as np

env = simpy.Environment()

SIM_TIME = 60*24 # 24 hours in minutes
lambda_rate = 60

def user3_generator(env, lambda_rate):
    inter_arrival_time = np.random.exponential(scale=1/lambda_rate)
    i = 0
    while True:
        yield env.timeout(inter_arrival_time)
        i += 1
        # print(f"Generated User3 Request {i} at time {env.now}")
    
env.process(user3_generator(env, lambda_rate))
env.run(until=SIM_TIME)



