#!/usr/bin/env bash

#SBATCH --partition=long
#SBATCH -c 64
#SBATCH -o f_latest_new.log

container="/data/courses/2026_dat471_dit066/containers/assignment2.sif"
assignment_root="$HOME/a2-multiprocessing"
dataset="/data/courses/2026_dat471_dit066/datasets/gutenberg"

apptainer exec \
    --bind "$HOME" \
    --bind "$dataset:$HOME/a2-multiprocessing/data" \
    $container \
    bash -c "source .venv/bin/activate && python3 gather_stats_f.py"
