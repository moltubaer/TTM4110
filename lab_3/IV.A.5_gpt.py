# ----- Lab IV ----- #
# ----- IV.A.5 ----- #

# Assume the same distributions of the time to failure and repair time as for the analytical model. 
# 5. Make a simulation model. 
# 	- Implement a simulator that can run simulations for s=1,2,or 3 to obtain the system Mean Down Time (MDT) in both a serial and parallel system .   
# 	- Run simulations until you have observed 100 system failures.  Let again n=14, and repeat for s=1,2,and 3 and for both serial and parallel system. 
# 	- Plot the average MDT with 95% confidence interval (use error bars).
# 	- Compare and comment the results for the three configurations of s and for the two alternative systems (serial and parallel).


import simpy
import numpy as np
import matplotlib.pyplot as plt
import statistics

def server(env, repair_resources, n, lambda_srv, mu_srv, system_type, failures_count):
    global server_mdt, system_mdt
    working_servers = n
    server_downtime_accumulator = 0
    system_downtime_accumulator = 0
    
    while failures_count[0] < 100:
        # Time to next failure
        time_to_failure = np.random.exponential(1/lambda_srv)
        yield env.timeout(time_to_failure)
        
        # Server failure
        working_servers -= 1
        failure_time = env.now
        
        # Time to repair
        repair_time = np.random.exponential(1/mu_srv)
        
        # Request repair resources
        with repair_resources.request() as req:
            yield req
            yield env.timeout(repair_time)
            
        
        if system_type == 'serial':
            # server_downtime_accumulator += env.now - failure_time
            if working_servers < n:
                system_downtime_accumulator += env.now - failure_time
        elif system_type == 'parallel':
            # server_downtime_accumulator += env.now - failure_time
            if working_servers == 0:
                system_downtime_accumulator += env.now - failure_time
        else:
            raise ValueError("Invalid system type")


        # Server repair
        working_servers += 1
        server_downtime_accumulator += env.now - failure_time
        failures_count[0] += 1
    
    else:
        server_mdt = server_downtime_accumulator/failures_count[0]
        system_mdt = system_downtime_accumulator/failures_count[0]
        # print(system_type)
        # print(server_mdt)
        # print(system_mdt)
        # print()

    return

def run_simulation(repairmen, system_type):
    n = 14
    lambda_srv = 0.13863
    mu_srv = 13.72431
    
    global server_mdt, system_mdt


    env = simpy.Environment()
    repair_resources = simpy.Resource(env, capacity=repairmen)
    
    failures_count = [0]  # Use a mutable object to share the count between processes
    
    # Start the simulation process
    env.process(server(env, repair_resources, n, lambda_srv, mu_srv, system_type, failures_count))

    # Run the simulation
    env.run(until=24*60)    # minutes

    if system_type == 'serial':
        downtime_server_serial.append(server_mdt)
        downtime_system_serial.append(system_mdt)
    elif system_type == 'parallel':
        downtime_server_parallel.append(server_mdt)
        downtime_system_parallel.append(system_mdt)
    else:
        raise ValueError("Invalid system type")

    print(system_type)
    print(server_mdt)
    print(system_mdt)
    print()
    
    return failures_count[0]


# Function to compute confidence interval
def confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), np.std(a)
    h = se * np.t.ppf((1 + confidence) / 2., n-1)
    return m, h

# Plotting
def plot_results(downtime_server, downtime_system, repairmen, system_type):
    x = np.arange(1, len(downtime_server) + 1)

    # Plot server downtime
    plt.errorbar(x, downtime_server, label=f'Server Downtime ({repairmen} Repairmen)', fmt='o-', capsize=5)

    # Plot system downtime
    plt.errorbar(x, downtime_system, label=f'System Downtime ({repairmen} Repairmen)', fmt='o-', capsize=5)

    plt.xlabel('Simulation Run')
    plt.ylabel('Mean Downtime (minutes)')
    plt.title(f'Mean Downtime for {system_type} System with {repairmen} Repairmen')
    plt.legend()
    plt.show()

# Run simulations for serial and parallel systems with different numbers of repairmen
downtime_server_serial = []
downtime_system_serial = []
downtime_server_parallel = []
downtime_system_parallel = []

server_mdt = 0
system_mdt = 0

serial_1 = run_simulation(repairmen=1, system_type='serial')
serial_2 = run_simulation(repairmen=2, system_type='serial')
serial_3 = run_simulation(repairmen=3, system_type='serial')

parallel_1 = run_simulation(repairmen=1, system_type='parallel')
parallel_2 = run_simulation(repairmen=2, system_type='parallel')
parallel_3 = run_simulation(repairmen=3, system_type='parallel')

print("serial")
print(downtime_server_serial)
print(downtime_server_serial)
print()
print("Parallel")
print(downtime_server_parallel)
print(downtime_system_parallel)

# Plot the results
plot_results(downtime_server_serial, downtime_system_serial, 1, 'Serial')
plot_results(downtime_server_parallel, downtime_system_parallel, 1, 'Parallel')
