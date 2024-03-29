# ----- Lab II ----- #
# ----- II.A.4 ----- #

import simpy    
import numpy as np

env = simpy.Environment()

# Simulation variables
n = 5
m = 5
k = 0
used_blocks = 0
Qmin = 0.6

# Statistics variables
user_id = 0
rejects = 0
successes = 0

# Timing variables
SIM_TIME = 60*24 # 24 hours in minutes
lambda_rate = 60

def get_bandwidth():
    return np.random.random()

def allocate_resources():
    global n, m, k, used_blocks

    if k > n*m:
        return False

    blocks_per_user = (n*m) // k
    used_blocks = blocks_per_user * k
    
    return True

def user3_generator(env, lambda_rate, Qmin):
    streaming_duration = np.random.exponential(1/lambda_rate)
    global user_id
    while True:
        yield env.timeout(streaming_duration)
        env.process(user3(env, user_id, Qmin, get_bandwidth()))
        user_id += 1
        # print(f"Generated User3 Request {user_id} at time {env.now}")

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

checksum = user_id - rejects - successes

print()
print(f"Generated User3 processes: \t {user_id}")
print(f"Rejected users: \t\t {rejects}")
print(f"Succesfull streams: \t\t {successes}")
print(f"Checksum: \t\t\t {checksum}")
