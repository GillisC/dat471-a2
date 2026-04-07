#!/usr/bin/env bash

speedup () {
    s=$(echo "scale=5; 1.0 / ((1.0 - 0.7) + (0.7 / $1))" | bc)
    echo "$s"
}

declare -a arr=( 2 4 8 16 32 64 )

for i in "${arr[@]}"
do
    val=$(speedup $i)
    echo "speedup using $i processes: $val"
done

lim=$(echo "scale=5; 1.0 / (1.0 - 0.7)" | bc)
echo "theoretical limit of speedup using infinite processors: $lim"
