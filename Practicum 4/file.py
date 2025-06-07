import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.animation as animation

# -----------------------------------------
#  STEP 1 - Initialize
# -----------------------------------------

# G[i, j] — провідність між вузлом i та j
G = np.array([
    [0.0, 1.0, 0.5],
    [1.0, 0.0, 1.0],
    [0.5, 1.0, 0.0]
])

# Початкові значення — напруга у вузлах
V0 = [0.0, 0.0, 0.0]  # Початково всі вузли мають 0 В

# Потужність генерації/споживання
def P(t):
    # Потужність у кожному вузлі
    return np.array([
        2.0,   # Генератор
        -1.0,  # Споживач
        0.2    # Буфер
    ])

# Ємність вузлів (впливає на швидкість зміни напруги)
C = np.array([1.0, 1.0, 1.0])  # Для спрощення

# -----------------------------------------
# КРОК 2: Диференціальні рівняння
# -----------------------------------------

def dV_dt(t, V, G):
    V = np.array(V)
    dV = np.zeros_like(V)
    P_val = P(t)
    for i in range(len(V)):
        # Сумарний струм у вузол i
        net_current = sum(G[i, j] * (V[j] - V[i]) for j in range(len(V)) if i != j)
        # Зміна напруги через баланс потужності: dV/dt = (P - V * I) / C
        dV[i] = (P_val[i] - V[i] * net_current) / C[i]
    return dV



# -----------------------------------------
# КРОК 3: Симуляція
# -----------------------------------------
t_span = (0, 20)
t_eval = np.linspace(*t_span, 300)

# solution = solve_ivp(dV_dt, t_span, V0, t_eval=t_eval)

# Параметри експерименту
G01_values = [0.1, 0.5, 1.0, 2.0, 5.0]
colors = ['b', 'g', 'r', 'm', 'orange']
plt.figure(figsize=(10, 6))
for idx, G01 in enumerate(G01_values):
    # Створюємо провідністьну матрицю з змінним G01
    G = np.array([
        [0.0, G01, 0.5],
        [G01, 0.0, 1.0],
        [0.5, 1.0, 0.0] # [0.1, 0.3, 0.0]  # Менші значення — інше навантаження
    ])
    
    # Функція для інтегрування з фіксованою G
    def system(t, V): return dV_dt(t, V, G)
    
    sol = solve_ivp(system, t_span, V0, t_eval=t_eval)
    

# -----------------------------------------
# КРОК 4: Результати
# -----------------------------------------
    print(f"== Results {idx+1} ==")
    times = sol.t
    voltages = sol.y

    for i, V in enumerate(voltages):
        print(f"Вузол {i}: напруга в кінці = {V[-1]:.2f} В")

        
    # Візуалізуємо напругу на споживачі (вузол 1)
    plt.plot(sol.t, sol.y[1], color=colors[idx], label=f"G₀₁ = {G01}")


G_graph = nx.Graph()
G_graph.add_nodes_from([0, 1, 2])
G_graph.add_weighted_edges_from([
    (0, 1, G01),
    (0, 2, 0.5),
    (1, 2, 1.0)
])

pos = nx.spring_layout(G_graph, seed=42)  # фиксированная раскладка

fig, ax = plt.subplots(figsize=(6, 6))

def update(frame):
    ax.clear()
    voltages_frame = sol.y[:, frame]
    colors = [plt.cm.viridis((v - min(voltages_frame)) / (max(voltages_frame) - min(voltages_frame) + 1e-6)) for v in voltages_frame]
    nx.draw(G_graph, pos, ax=ax, with_labels=True, node_color=colors, node_size=500, font_size=16)
    ax.set_title(f"Час: {sol.t[frame]:.2f} c")
    sm = plt.cm.ScalarMappable(cmap='viridis', norm=plt.Normalize(vmin=min(voltages_frame), vmax=max(voltages_frame)))
    plt.colorbar(sm, ax=ax, label='Напруга (В)')

ani = animation.FuncAnimation(fig, update, frames=len(sol.t), interval=100)
plt.show()



plt.xlabel("Час (с)")
plt.ylabel("Напруга (В)")
plt.title("Динаміка напруги у вузлах мережі")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

def simulate_statistical(times, P_func, C):
    P_avg = P_func(0)  # якщо P не змінюється
    return np.outer(P_avg / C, times)

energy_stat = simulate_statistical(times, P, C)

# RMSE порівняння
print("Порівняння з простою статистичною моделлю:")
for i in range(3):
    rmse = np.sqrt(np.mean((voltages[i] - energy_stat[i])**2))
    print(f"  Вузол {i}: RMSE = {rmse:.4f}")

# Графіки для порівняння
plt.figure(figsize=(10, 6))
for i in range(3):
    plt.plot(times, voltages[i], label=f'Вузол {i} (ODE)', linestyle='-')
    plt.plot(times, energy_stat[i], label=f'Вузол {i} (стат)', linestyle='--')
plt.xlabel("Час (с)")
plt.ylabel("Напруга / Енергія (відн.)")
plt.title(f"Порівняння ODE vs статистичної моделі (G₀₁ = {G01})")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()