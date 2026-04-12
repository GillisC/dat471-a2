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

workers = 64
batch_sizes = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]
results = []

for b in batch_sizes:
    print(f"starting for {b} batch_size")
    cmd = ["python3", "assignment2_problem2f.py", "data/big", "-w", str(workers), "-b", str(b)]
    process = subprocess.run(cmd, capture_output=True, text=True)
    output = process.stdout

    total_time = re.search(r"total time: ([\d.]+)", output).group(1)

    results.append({
        "workers": workers,
        "batch_size": b,
        "total_time": total_time,
    })
    print(f"finished run using {b} batch_size")
    print(output, "\n\n")

with open("results_batch_sizes_f.csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames=["workers", "batch_size", "total_time"])
    writer.writeheader()
    writer.writerows(results)
    
