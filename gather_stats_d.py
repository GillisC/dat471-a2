import subprocess
import re
import csv

"""
For each run configuration
    run the script
    grab the total time and number of workers used
    store in a dict

convert dict to a csv
"""

workers = [1, 2, 4, 8, 16, 32, 64]
batch_size = 128
results = []

for w in workers:
    cmd = ["python3", "assignment2_problem2d.py", "data/medium", "-w", str(w), "-b", str(batch_size)]
    process = subprocess.run(cmd, capture_output=True, text=True)
    output = process.stdout

    total_time = re.search(r"total time: ([\d.]+)", output).group(1)
    parallel_time = re.search(r"parallel time: ([\d.]+)", output).group(1)

    results.append({
        "workers": w,
        "total_time": total_time,
        "parallel_time": parallel_time,
    })

with open("results_parallel_huge.csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames=["workers", "total_time", "parallel_time"])
    writer.writeheader()
    writer.writerows(results)
    
