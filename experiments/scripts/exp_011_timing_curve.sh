#!/bin/bash
# Test multiple move counts to map the timing curve
cd /Users/jasonwalsh/projects/jwalsh/2048/2048-cli-0.9.1

echo "=== Timing Curve Analysis ==="
echo "moves,run,time_s,score,max_tile" > /Users/jasonwalsh/projects/jwalsh/2048/experiments/exp_011_timing_curve.csv

# Test points: 10, 20, 40, 60, 80, 100, 120, 150, 200 moves
MOVE_COUNTS=(10 20 40 60 80 100 120 150 200)

for MOVES in "${MOVE_COUNTS[@]}"; do
    echo -e "\n=== Testing $MOVES moves (5 runs) ==="
    
    # Generate move sequence
    MOVE_SEQ=""
    for ((i=1; i<=MOVES/2; i++)); do
        MOVE_SEQ="${MOVE_SEQ}sd"
    done
    # Add single 's' if odd number
    if (( MOVES % 2 == 1 )); then
        MOVE_SEQ="${MOVE_SEQ}s"
    fi
    MOVE_SEQ="${MOVE_SEQ}q"
    
    # Run 5 times for each move count
    for run in {1..5}; do
        START=$(date +%s.%N)
        OUTPUT=$(echo "$MOVE_SEQ" | ./2048-debug 2>&1)
        END=$(date +%s.%N)
        
        TIME_S=$(echo "$END - $START" | bc)
        SCORE=$(echo "$OUTPUT" | grep "Score:" | tail -1 | awk '{print $2}')
        MAX_TILE=$(echo "$OUTPUT" | grep -E "^\|" | grep -oE "[0-9]+" | sort -nr | head -1)
        
        echo "$MOVES,$run,$TIME_S,$SCORE,$MAX_TILE" >> /Users/jasonwalsh/projects/jwalsh/2048/experiments/exp_011_timing_curve.csv
        echo "  Run $run: ${TIME_S}s ($(echo "scale=3; $TIME_S / $MOVES * 1000" | bc)ms/move)"
    done
done

echo -e "\n=== Curve mapping complete ==="
