# ----- Lab II ----- #
import simpy
import numpy as np

env = simpy.Environment()

# ----- II.A.1 ----- #
SIM_TIME = 60*24 # 24 hours in minutes
lambda_rate = 0.5

def user3_generator(env, lambda_rate):
    inter_arrival_time = np.random.exponential(scale=1/lambda_rate)
    i = 0
    while True:
        yield env.timeout(inter_arrival_time)
        i += 1
        # print(f"Generated User3 Request {i} at time {env.now}")
    
# Start the user3 generator process
env.process(user3_generator(env, lambda_rate))
env.run(until=SIM_TIME)




# ----- II.A.2 ----- #
def calculate_mos_score(bandwidth):
    # Define the MOS step function thresholds and corresponding values
    thresholds = [0, 0.2, 0.5, 0.7, 1]
    mos_values = [1, 2, 3, 4, 5]

    mos_score = None
    for i in range(len(thresholds)):
        if bandwidth <= thresholds[i]:
            if i == 0:
                mos_score = mos_values[0]
            else:
                mos_score = mos_values[i-1]
            break

    return mos_score



bandwidth = 0.9  # Adjust the bandwidth value as needed
mos = calculate_mos_score(bandwidth)
print(f"MOS Score: {mos}")

# (m*n)/k <= 1
# n servers
# m resource allocations
# k users



