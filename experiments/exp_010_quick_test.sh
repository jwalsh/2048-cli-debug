#!/bin/bash
# Quick test: 3 runs to verify setup before full experiment
cd /Users/jasonwalsh/projects/jwalsh/2048/2048-cli-0.9.1

echo "=== Quick Sanity Check: 3 runs of 150 moves ==="
MOVES=""
for i in {1..75}; do MOVES="${MOVES}sd"; done
MOVES="${MOVES}q"

for run in {1..3}; do
    echo -n "Run $run: "
    START=$(date +%s.%N)
    echo "$MOVES" | ./2048-debug > /dev/null 2>&1
    END=$(date +%s.%N)
    TIME=$(echo "$END - $START" | bc)
    echo "${TIME}s"
done
