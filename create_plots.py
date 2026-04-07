import matplotlib.pyplot as plt
import pandas as pd


df_d = pd.read_csv("results_parallel_huge.csv")
df_e = pd.read_csv("results_e.csv")

max_theo_speedup = 6.135

# PLOT E
df_d["sequential_time"] = df_d["total_time"] - df_d["parallel_time"]
df_d["parallel_portion"] = df_d["parallel_time"] - df_d["total_time"]
df_d["sequential_portion"] = df_d["sequential_time"] - df_d["total_time"]

t_1 = df_d.loc[df_d["workers"] == 1, "total_time"].values[0]
df_d["speedup"] = t_1 / df_d["total_time"]
s_time = df_d.loc[df_d["workers"] == 1, "sequential_time"].values[0]
s_portion = s_time / t_1


plt.figure(figsize=(10, 6.18))
plt.plot(df_d['workers'], df_d['speedup'], marker='s', color='green', label='Actual Speedup')
plt.axhline(y=max_theo_speedup, color='red', linestyle='--', 
            label=f'Amdahl Limit ({max_theo_speedup:.2f}x)')

plt.xlabel('Number of Workers')
plt.ylabel('Speedup Factor')
plt.title('Performance Scaling (Speedup)')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()

plt.tight_layout()
plt.savefig('part_d_plot.png')

#PLOT D
df_e["sequential_time"] = df_e["total_time"] - df_e["parallel_time"]
df_e["parallel_portion"] = df_e["parallel_time"] - df_e["total_time"]
df_e["sequential_portion"] = df_e["sequential_time"] - df_e["total_time"]

t_1 = df_e.loc[df_e["workers"] == 1, "total_time"].values[0]
df_e["speedup"] = t_1 / df_e["total_time"]

plt.figure(figsize=(10, 6.18))
plt.plot(df_e['workers'], df_e['speedup'], marker='s', color='green', label='Actual Speedup')
plt.axhline(y=max_theo_speedup, color='red', linestyle='--', 
            label=f'Amdahl Limit ({max_theo_speedup:.2f}x)')

plt.xlabel('Number of Workers')
plt.ylabel('Speedup Factor')
plt.title('Performance Scaling (Speedup)')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()

plt.tight_layout()
plt.savefig('part_e_plot.png')
