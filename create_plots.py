import matplotlib.pyplot as plt
import pandas as pd


df = pd.read_csv("results_parallel_huge.csv")

df["sequential_time"] = df["total_time"] - df["parallel_time"]
df["parallel_portion"] = df["parallel_time"] - df["total_time"]
df["sequential_portion"] = df["sequential_time"] - df["total_time"]

t_1 = df.loc[df["workers"] == 1, "total_time"].values[0]
df["speedup"] = t_1 / df["total_time"]

s_time = df.loc[df["workers"] == 1, "sequential_time"].values[0]
s_portion = s_time / t_1

max_theo_speedup = 1 / s_portion

plt.figure(figsize=(12, 6)
plt.plot(df['workers'], df['speedup'], marker='s', color='green', label='Actual Speedup')
plt.axhline(y=max_theo_speedup, color='red', linestyle='--', 
            label=f'Amdahl Limit ({max_theo_speedup:.2f}x)')

plt.xlabel('Number of Workers')
plt.ylabel('Speedup Factor')
plt.title('Performance Scaling (Speedup)')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()

plt.tight_layout()
plt.savefig('part_d_plot.png')
