#!/bin/bash
# Test if board density affects timing
cd /Users/jasonwalsh/projects/jwalsh/2048/2048-cli-0.9.1

echo "=== Board Density Impact Test ==="
echo "strategy,density_estimate,moves,time_s,tiles" > /Users/jasonwalsh/projects/jwalsh/2048/experiments/exp_011_density.csv

# Strategy 1: Corner packing (down-left spam) - high density
echo "Testing corner packing strategy..."
CORNER_MOVES=""
for i in {1..50}; do CORNER_MOVES="${CORNER_MOVES}sa"; done
CORNER_MOVES="${CORNER_MOVES}q"

START=$(date +%s.%N)
OUTPUT=$(echo "$CORNER_MOVES" | ./2048-debug 2>&1)
END=$(date +%s.%N)
TIME_S=$(echo "$END - $START" | bc)
TILES=$(echo "$OUTPUT" | grep -E "^\|" | grep -oE "[0-9]+" | wc -l | tr -d ' ')
echo "corner,high,100,$TIME_S,$TILES" >> /Users/jasonwalsh/projects/jwalsh/2048/experiments/exp_011_density.csv

# Strategy 2: Spread moves (alternating all directions) - low density
echo "Testing spread strategy..."
SPREAD_MOVES=""
for i in {1..25}; do SPREAD_MOVES="${SPREAD_MOVES}wasd"; done
SPREAD_MOVES="${SPREAD_MOVES}q"

START=$(date +%s.%N)
OUTPUT=$(echo "$SPREAD_MOVES" | ./2048-debug 2>&1)
END=$(date +%s.%N)
TIME_S=$(echo "$END - $START" | bc)
TILES=$(echo "$OUTPUT" | grep -E "^\|" | grep -oE "[0-9]+" | wc -l | tr -d ' ')
echo "spread,low,100,$TIME_S,$TILES" >> /Users/jasonwalsh/projects/jwalsh/2048/experiments/exp_011_density.csv

# Strategy 3: Our standard down-right - medium density
echo "Testing standard strategy..."
STANDARD_MOVES=""
for i in {1..50}; do STANDARD_MOVES="${STANDARD_MOVES}sd"; done
STANDARD_MOVES="${STANDARD_MOVES}q"

START=$(date +%s.%N)
OUTPUT=$(echo "$STANDARD_MOVES" | ./2048-debug 2>&1)
END=$(date +%s.%N)
TIME_S=$(echo "$END - $START" | bc)
TILES=$(echo "$OUTPUT" | grep -E "^\|" | grep -oE "[0-9]+" | wc -l | tr -d ' ')
echo "standard,medium,100,$TIME_S,$TILES" >> /Users/jasonwalsh/projects/jwalsh/2048/experiments/exp_011_density.csv

echo "=== Density test complete ==="
