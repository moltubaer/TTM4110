# ----- Lab II ----- #
# ----- II.A.5 ----- #

import simpy    
import numpy as np
import pandas as pd

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

# Elprice variables
pm_h = 0.6
lambda_low = 1.0 / 60 
lambda_medium = 1.0 / 60
lambda_high = 1.0 / 60*2
bandwidth_modifier = None
total_bandwidth = 0
total_mos = 0
mos = None

# Power statistic variable
e_server = 1000
e_resource = e_server/m
e_active_user = e_resource/60
p_low = 0.1/60     # per kWH
p_medium = 1/60    # per kWH
p_high = 5/60      # per kWH
e_total = 0
p_total = 0

times = []
prices = []


def get_bandwidth():
    return np.random.random()

def calculate_mos(bandwidth):
    thresholds = [0.0, 0.5, 0.6, 0.8, 0.9, 1.0]
    mos_values = [1, 2, 3, 4, 5]

    mos_score = None
    for i in range(len(thresholds)):
        if bandwidth < thresholds[i]:
            if i == 0:
                mos_score = mos_values[0]
            else:
                mos_score = mos_values[i-1]
            break
        elif bandwidth >= thresholds[-1]:
            mos_score = mos_values[-1]
            break

    return mos_score

def scale_up():
    global n, m, k
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
    global rejects, successes, k, n, m, used_blocks, bandwidth_modifier, e_total, e_active_user, total_bandwidth, mos, total_mos

    # ----- Check quality ----- #
    if bandwidth < Qmin:
        rejects += 1
        # print(f"User {id} was rejected")
        return

    # ----- Check available resources ----- #
    if calculate_resources():
        # ----- Streaming ----- #
        stream_start = env.now
        yield env.timeout(np.random.exponential(1))
        time_active = env.now - stream_start
        # print(f"\t\t\t\t\t\t User {id} leaved after streaming for {time_active} minutes \t")
        energy = used_blocks*e_active_user
        e_total += energy
        total_bandwidth += bandwidth * bandwidth_modifier
        mos = calculate_mos(bandwidth * bandwidth_modifier)     # MOS for a specific user
        total_mos += mos
        successes += 1
        k -= 1
        used_blocks -= 1
        return
    else:
        # print(f"User {id} was rejected")
        rejects += 1
        return

def el_price_simulation(env, pm_h):
    global bandwidth_modifier, e_total, p_total, p_low, p_medium, p_high
    current_level = 'medium'

    while True:
        start = env.now

        match current_level:
            case 'low':
                bandwidth_modifier = 1.0
                time_in_current_level = np.random.exponential(1.0 / lambda_low)
            case 'medium':
                bandwidth_modifier = 0.9
                time_in_current_level = np.random.exponential(1.0 / lambda_medium)
            case 'high':
                bandwidth_modifier = 0.8
                time_in_current_level = np.random.exponential(1.0 / lambda_high)

        
        yield env.timeout(time_in_current_level)
        
        match current_level:
            case 'low' | 'high':
                next_level = np.random.choice(['medium'])
            case 'medium':
                next_level = np.random.choice(['low', 'high'], p=[1.0 - pm_h, pm_h])    

        end = env.now

        match current_level:
            case 'low':
                price = p_low * (end-start)
                # print(f"{p_low:.4f} \t  {(end-start):.4f} \t {price:.4f}")
            case 'medium':
                price = p_medium * (end-start)
                # print(f"{p_medium:.4f} \t {(end-start):.4f} \t {price:.4f}")
            case 'high':
                price = p_high * (end-start)
                # print(f"{p_high:.4f} \t {(end-start):.4f} \t {price:.4f}")

        currentTime: float = float(env.now)
        times.append(round(currentTime, 2))
        prices.append(round(price, 2))

        p_total += price*n
        current_level = next_level
        # print(f"Time: {env.now:.2f}, Price Level: {current_level}")

def quality_simulation(env):
    global mos
    mos_scores = []
    times = []
    while True:
        start = env.now
        mos_scores.append(mos)

        current_time = float(env.now)
        times.append(round(current_time, 2))

        print(f"Mos: {mos}, Time: {round(current_time, 2)}")




    
env.process(el_price_simulation(env, pm_h))
env.process(user3_generator(env, lambda_rate, Qmin))
env.process(quality_simulation(env)) # ?? need to look into this shit
env.run(until=SIM_TIME)

checksum = user_id - rejects - successes - k
mean_bandwidth = total_bandwidth/(successes + k)
mean_mos = total_mos/(successes + k)

data = {"time": times, "price": prices}
df = pd.DataFrame(data)
df.to_csv('output.csv', index=False)

print()
print(f"Price total: \t\t\t {p_total:.2f} NOK")
print(f"Energy total: \t\t\t {e_total:.0f} kW")
print(f"Mean bandwidth: \t\t {mean_bandwidth:.2f}")
print(f"Mean MOS: \t\t\t {mean_mos:.2f} : {calculate_mos(mean_bandwidth)}")
print()
print(f"Generated User3 processes: \t {user_id}")
print(f"Rejected users: \t\t {rejects}", f"{(rejects/user_id)*100:.4f}%")
print(f"Succesfull streams: \t\t {successes + k}", f"{((successes+k)/user_id)*100:.4f}%")
print()
