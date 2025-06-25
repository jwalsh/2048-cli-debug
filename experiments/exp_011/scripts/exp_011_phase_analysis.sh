#!/bin/bash
# Analyze timing of different game phases
cd ../../2048-cli-0.9.1

echo "=== Game Phase Analysis ==="
echo "phase,moves,time_s,tiles_on_board,score" > ../experiments/exp_011/exp_011_phases.csv

# Function to count tiles in output
count_tiles() {
    echo "$1" | grep -E "^\|" | grep -oE "[0-9]+" | wc -l | tr -d ' '
}

# Test early game (first 20 moves)
echo "Testing early game..."
EARLY_MOVES="sdsdsdsdsdsdsdsdsdsdq"
START=$(date +%s.%N)
OUTPUT=$(echo "$EARLY_MOVES" | ./2048-debug 2>&1)
END=$(date +%s.%N)
TIME_S=$(echo "$END - $START" | bc)
TILES=$(count_tiles "$OUTPUT")
SCORE=$(echo "$OUTPUT" | grep "Score:" | tail -1 | awk '{print $2}')
echo "early,20,$TIME_S,$TILES,$SCORE" >> ../experiments/exp_011/exp_011_phases.csv

# Test mid game (moves 21-60)
echo "Testing mid game..."
MID_MOVES=""
for i in {1..20}; do MID_MOVES="${MID_MOVES}sd"; done
# Continue from early game state
CONT_MOVES="sdsdsdsdsdsdsdsdsdsd${MID_MOVES}q"
START=$(date +%s.%N)
OUTPUT=$(echo "$CONT_MOVES" | ./2048-debug 2>&1)
END=$(date +%s.%N)
TIME_S=$(echo "$END - $START" | bc)
TILES=$(count_tiles "$OUTPUT")
SCORE=$(echo "$OUTPUT" | grep "Score:" | tail -1 | awk '{print $2}')
# Calculate just the mid-game time
TOTAL_TIME=$TIME_S
echo "mid,40,$TIME_S,$TILES,$SCORE" >> ../experiments/exp_011/exp_011_phases.csv

# Test late game (moves 61-100)
echo "Testing late game..."
LATE_MOVES=""
for i in {1..50}; do LATE_MOVES="${LATE_MOVES}sd"; done
FULL_MOVES="${LATE_MOVES}q"
START=$(date +%s.%N)
OUTPUT=$(echo "$FULL_MOVES" | ./2048-debug 2>&1)
END=$(date +%s.%N)
TIME_S=$(echo "$END - $START" | bc)
TILES=$(count_tiles "$OUTPUT")
SCORE=$(echo "$OUTPUT" | grep "Score:" | tail -1 | awk '{print $2}')
echo "late,100,$TIME_S,$TILES,$SCORE" >> ../experiments/exp_011/exp_011_phases.csv

echo "=== Phase analysis complete ==="
