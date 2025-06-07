import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# -----------------------------------------
#  STEP 1: Initialize
# -----------------------------------------
print("== STEP 1: Initialize ==")

G = np.array([
    [0.0, 1.0, 0.5],
    [1.0, 0.0, 1.0],
    [0.5, 1.0, 0.0]
])

V0 = [0.0, 0.0, 0.0] 

def P(t):
    return np.array([
        2.0, # Generator
        -1.0, # Consumer
        0.2 # Buffer
    ])

C = np.array([1.0, 1.0, 1.0]) 

# -----------------------------------------
# STEP 2: Differential equations
# -----------------------------------------
print("== STEP 2: Differential equations ==")

def dV_dt(t, V, G):
    V = np.array(V)
    dV = np.zeros_like(V)
    P_val = P(t)
    for i in range(len(V)):
        net_current = sum(G[i, j] * (V[j] - V[i]) for j in range(len(V)) if i != j)
        dV[i] = (P_val[i] - V[i] * net_current) / C[i]
    return dV



# -----------------------------------------
# STEP 3: Simulation
# -----------------------------------------
print("== STEP 3: Simulation ==")
t_span = (0, 20)
t_eval = np.linspace(*t_span, 300)


G01_values = [0.1, 0.5, 1.0, 2.0, 5.0]
colors = ['b', 'g', 'r', 'm', 'orange']
plt.figure(figsize=(10, 6))
for idx, G01 in enumerate(G01_values):
    G = np.array([
        [0.0, G01, 0.5],
        [G01, 0.0, 1.0],
        [0.5, 1.0, 0.0] 
    ])
    
    def system(t, V): return dV_dt(t, V, G)
    sol = solve_ivp(system, t_span, V0, t_eval=t_eval)
    

# -----------------------------------------
# STEP 4: Results
# -----------------------------------------
    print(f"== Results {idx+1} ==")
    times = sol.t
    voltages = sol.y

    for i, V in enumerate(voltages):
        print(f"Node {i}: end voltage = {V[-1]:.2f} V")

        
    plt.plot(sol.t, sol.y[1], color=colors[idx], label=f"G₀₁ = {G01}")




plt.xlabel("Time (s)")
plt.ylabel("Voltage (V)")
plt.title("Voltage dynamics in the network nodes")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

def simulate_statistical(times, P_func, C):
    P_avg = P_func(0)  
    return np.outer(P_avg / C, times)

energy_stat = simulate_statistical(times, P, C)

# RMSE comparison
print("Comparison with a simple statistical model:")
for i in range(3):
    rmse = np.sqrt(np.mean((voltages[i] - energy_stat[i])**2))
    print(f"  Вузол {i}: RMSE = {rmse:.4f}")

#  Graph Comparison
plt.figure(figsize=(10, 6))
for i in range(3):
    plt.plot(times, voltages[i], label=f'Node {i} (ODE)', linestyle='-')
    plt.plot(times, energy_stat[i], label=f'Node {i} (стат)', linestyle='--')
plt.xlabel("Time (s)")
plt.ylabel("Voltage / Energy (relative)")
plt.title(f"Comparison of ODE vs. statistical model (G₀₁ = {G01})")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()