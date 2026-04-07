#!/usr/bin/env bash

#SBATCH -c 1
#SBATCH -o latest_plots.log

container="/data/courses/2026_dat471_dit066/containers/assignment2.sif"
assignment_root="$HOME/a2-multiprocessing"

apptainer exec \
    --bind "$HOME" \
    $container \
    python3 create_plots.py
