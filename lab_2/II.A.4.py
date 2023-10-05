import simpy    
import numpy as np

env = simpy.Environment()

# Simulation variables
n = 5
m = 5
total_blocks = n*m
k = 0
used_blocks = 0
Qmin = 0.6

# Statistics variables
i = 0
rejects = 0
successes = 0

# Timing variables
SIM_TIME = 60*24 # 24 hours in minutes
lambda_rate = 60

def get_bandwidth():
    return np.random.random()

def allocate_resources():
    global total_blocks, k, used_blocks

    if k > total_blocks:
        return False

    blocks_per_user = total_blocks // k
    used_blocks = blocks_per_user * k
    
    return True

def user3_generator(env, lambda_rate, Qmin):
    streaming_duration = np.random.exponential(scale=1/lambda_rate)
    global i
    while True:
        yield env.timeout(streaming_duration)
        env.process(user3(env, i, Qmin, get_bandwidth()))
        i += 1
        # print(f"Generated User3 Request {i} at time {env.now}")

def user3(env, id, Qmin, bandwidth):
    global rejects, successes, k
    k += 1

    # ----- Check quality ----- #
    if bandwidth < Qmin:
        # ----- Reject user ----- #
        rejects += 1
        # print(f"User {id} was rejected")
        k -= 1
        return

    # ----- Check resources ----- #
    if allocate_resources():
        # ----- Streaming ----- #
        successes += 1
        stream_start = env.now
        yield env.timeout(np.random.exponential(60))
        time_active = env.now - stream_start
        # print(f"User {id} leaved after streaming for {time_active} minutes")
        k -= 1
        return

    else:
        # ----- Reject user ----- #
        rejects += 1
        # print(f"User {id} was rejected")
        k -= 1
        return

env.process(user3_generator(env, lambda_rate, Qmin))
env.run(until=SIM_TIME)

print()
print(f"Generated User3 processes: \t {i}")
print(f"Rejected users: \t\t {rejects}")
print(f"Succesfull streams: \t\t {successes}")
