import matplotlib.pyplot as plt
import pandas as pd

df_d = pd.read_csv("results_d.csv")
df_e = pd.read_csv("results_e.csv")
df_f = pd.read_csv("results_f.csv")

# gotten from problem 2 c)
max_theo_speedup = 5.53

def gen_plot(df, title: str, max_speedup):
    t_1 = 687.3612148761749
    df["speedup"] = t_1 / df["total_time"]

    plt.figure(figsize=(10, 6.18))
    plt.plot(df['workers'], df['speedup'], marker='s', label='Actual Speedup')
    plt.axhline(y=max_theo_speedup, linestyle='--', 
                label=f'Amdahl Limit ({max_theo_speedup:.2f}x)')

    plt.xlabel('Number of Workers')
    plt.ylabel('Speedup Factor')
    plt.title('Performance Scaling (Speedup)')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()

    plt.tight_layout()
    plt.savefig(f"{title}_plot.pdf")

# PLOT E
gen_plot(df_d, "part_d", max_theo_speedup)
gen_plot(df_e, "part_e", max_theo_speedup)
gen_plot(df_f, "part_f", max_theo_speedup)
