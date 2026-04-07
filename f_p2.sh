#!/usr/bin/env bash

#SBATCH -c 64
#SBATCH -o latest.log

container="/data/courses/2026_dat471_dit066/containers/assignment2.sif"

assignment_root="$HOME/a2-multiprocessing"
dataset="/data/courses/2026_dat471_dit066/datasets/gutenberg"

apptainer exec \
    --bind "$HOME" \
    --bind "$dataset:$HOME/a2-multiprocessing/data" \
    $container \
    python3 assignment2_problem2f.py data/tiny

