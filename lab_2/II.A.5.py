# ----- Lab II ----- #
# ----- II.A.5 ----- #

import simpy    
import numpy as np

env = simpy.Environment()

# Simulation variables
n = 2   # min 2, max 10
m = 5
k = 0
used_blocks = 0
Qmin = 0.5

# Statistics variables
user_id = 0
rejects = 0
successes = 0

# Timing variables
SIM_TIME = 60*24 # 24 hours in minutes
lambda_rate = 60

def get_bandwidth():
    return np.random.random()

def scale_up():
    global n, m, k, used_blocks
    if n < 10:
        n += 1
    return

def scale_down():
    global n, m, k, used_blocks    
    if n > 2:
        free_blocks = n*m - used_blocks            
        if free_blocks >= 5:
            n -= 1
    return

def allocate_resources():
    global k, n, m, used_blocks
    k += 1
    blocks_per_user = (n*m) // k
    used_blocks = blocks_per_user * k

def calculate_resources():
    global k, n, m, used_blocks

    if (k+1) == n*m:
        allocate_resources()        
        return True
    elif (k+1) > n*m:
        if n < 10:
            scale_up()
            allocate_resources()        
            return True
        else:
            return False
    elif (k+1) < n*m:
        if n > 2:
            scale_down()
            allocate_resources()        
            return True
        else:
            allocate_resources()        
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
    global rejects, successes, k, n, m, used_blocks

    # ----- Check quality ----- #
    if bandwidth < Qmin:
        # ----- Reject user ----- #
        rejects += 1
        # print(f"User {id} was rejected")
        return

    # ----- Check available resources ----- #
    if calculate_resources():
        # ----- Streaming ----- #
        stream_start = env.now
        yield env.timeout(np.random.exponential(60))
        time_active = env.now - stream_start
        # print(f"\t\t\t\t\t\t User {id} leaved after streaming for {time_active} minutes \t")
        successes += 1
        k -= 1
        used_blocks -= 1
        return

    else:
        # ----- Reject user ----- #
        # print(f"User {id} was rejected")
        rejects += 1
        return

env.process(user3_generator(env, lambda_rate, Qmin))
env.run(until=SIM_TIME)

checksum = user_id - rejects - successes - k

print()
print(f"Generated User3 processes: \t {user_id}")
print(f"Rejected users: \t\t {rejects}")
print(f"Succesfull streams: \t\t {successes}")
print(f"Active streams: \t\t {k}")
print(f"Checksum: \t\t\t {checksum}")
