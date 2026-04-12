#!/usr/bin/env bash

FILE="c_latest.log"
TOTAL_TIME=$(cat $FILE | grep "total time:" | awk '{print $3}')
SEQ_TIME=$(cat $FILE | grep "sequential time:" | awk '{print $3}')

echo "$TOTAL_TIME"
echo "$SEQ_TIME"

SEQ_PORTION=$(echo "scale=5; $SEQ_TIME / $TOTAL_TIME" | bc)
PAR_PORTION=$(echo "scale=5; 1.0 - $SEQ_PORTION" | bc)
THEO_SPEEDUP=$(echo "scale=4; 1 / $SEQ_PORTION" | bc)

echo "seq portion: $SEQ_PORTION"
echo "par portion: $PAR_PORTION"
echo "Max theoretical speedup: ${THEO_SPEEDUP}x"
