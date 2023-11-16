# ----- Lab IV ----- #
# ----- IV.A.6 ----- #

# Assume a serial system.
# 6. (*) From the model in IV.A.1, estimate the Mean Down Time (MDT) for the system and compare with the simulated results from IV.A.5.
# 	- Change the repair time distribution in the simulator from n.e.d to deterministic (with the same expectation). Rerun the simulations until you have observed 100 system failures. 
# 	- Plot and compare with the analytic solution again and comment the observations. 

import simpy
import numpy as np

def server(env, repair_resources, n, lambda_srv, mu_srv, system_type, failures_count):
    global server_mdt, system_mdt, rng
    working_servers = n
    server_downtime_accumulator = 0
    system_downtime_accumulator = 0
    
    while failures_count[0] < 100:
        # Time to next failure
        time_to_failure = rng.exponential(lambda_srv)
        yield env.timeout(time_to_failure)
        
        # Server failure
        working_servers -= 1
        failure_time = env.now
        
        # Time to repair (deterministic)
        repair_time = rng.exponential(mu_srv)
                
        # Request repair resources
        with repair_resources.request() as req:
            yield req
            yield env.timeout(repair_time)

            
        if system_type == 'serial':
            if working_servers < n:
                system_downtime_accumulator += env.now - failure_time
        elif system_type == 'parallel':
            if working_servers == 0:
                system_downtime_accumulator += env.now - failure_time
        else:
            raise ValueError("Invalid system type")

        # Server repair
        working_servers += 1
        server_downtime_accumulator += env.now - failure_time
        failures_count[0] += 1
    
    else:
        server_mdt = server_downtime_accumulator / failures_count[0]
        system_mdt = system_downtime_accumulator / failures_count[0]

    return

def run_simulation(repairmen, system_type):
    n = 14
    lambda_srv = 0.05   # Failure rate
    mu_srv = 0.5        # Repair rate
    
    global server_mdt, system_mdt

    env = simpy.Environment()
    repair_resources = simpy.Resource(env, capacity=repairmen)
    
    failures_count = [0]  # Use a mutable object to share the count between processes
    
    # Start the simulation process
    env.process(server(env, repair_resources, n, lambda_srv, mu_srv, system_type, failures_count))

    # Run the simulation
    env.run(until=24*60)    # minutes

    return

rng = np.random.default_rng(69420)

server_mdt = 0
system_mdt = 0

# Save results to txt file
def save_results_to_txt(filename, txt):
    with open(filename, 'a') as txt_file:
        txt_file.write(f"{txt}\n")

def serial():
    for i in range(1,4):
        filename_server = f'serial_{i}_server'
        filename_system = f'serial_{i}_system'
        for j in range(100):
            run_simulation(repairmen=i, system_type='serial')

            save_results_to_txt(filename_server, server_mdt)
            # save_results_to_txt(filename_system, system_mdt)

def parallel():
    for i in range(1,4):
        filename_server = f'parallel_{i}_server'
        filename_system = f'parallel_{i}_system'
        for j in range(100):
            run_simulation(repairmen=i, system_type='parallel')
            save_results_to_txt(filename_server, server_mdt)
            # save_results_to_txt(filename_system, system_mdt)

parallel()
