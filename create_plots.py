import matplotlib.pyplot as plt
import pandas as pd


df = pd.read_csv("results_parallel_huge.csv")

t_1 = df.loc[df["workers"] == 1, "total_time"].values[0]
df["speedup"] = t_1 / df["total_time"]

plt.subplot(1, 2, 2)
plt.plot(df['workers'], df['speedup'], marker='s', color='green', label='Actual Speedup')
plt.plot(df['workers'], df['workers'], color='gray', linestyle=':', label='Ideal (Linear)')
plt.xlabel('Number of Workers')
plt.ylabel('Speedup Factor')
plt.title('Performance Scaling (Speedup)')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()

plt.tight_layout()
plt.savefig('part_d_plot.png')
