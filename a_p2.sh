#!/usr/bin/env bash

#SBATCH -c 64
#SBATCH -o latest.log

container="/data/courses/2026_dat471_dit066/containers/assignment2.sif"

assignment_root="$HOME/a2-multiprocessing"
dataset="/data/courses/2026_dat471_dit066/datasets/gutenberg"

echo "running with num_workers: $NUM_WORKERS, using batch_size: $BATCH_SIZE"

apptainer exec \
    --bind "$HOME" \
    --bind "$dataset:$HOME/a2-multiprocessing/data" \
    $container \
    python3 assignment2_problem2a.py data/small -w 4 -b 32
