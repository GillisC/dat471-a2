#!/usr/bin/env bash

FILE="c_latest.log"
TOTAL_TIME=$(cat $FILE | grep "total time:" | awk '{print $3}')
SEQ_TIME=$(cat $FILE | grep "sequential time:" | awk '{print $3}')

echo "$TOTAL_TIME"
echo "$SEQ_TIME"

SEQ_PORTION=$(echo "scale=5; $SEQ_TIME / $TOTAL_TIME" | bc)
THEO_SPEEDUP=$(echo "scale=4; 1 / $SEQ_PORTION" | bc)

echo "Max theoretical speedup: ${THEO_SPEEDUP}x"
