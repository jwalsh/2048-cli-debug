#!/bin/bash
# Deep validation run: 50 runs with 150 moves each
cd ../../2048-cli-0.9.1

echo "=== Experiment #010: Timing Validation ==="
echo "Hypothesis: 150 moves = ~27.75s per run"
echo "Total expected time: ~23 minutes"
echo ""
echo "Starting at $(date)"
echo "run,score,time_s,max_tile,moves_per_second" > ../experiments/exp_010/exp_010_results.csv

# Generate move sequence (150 moves = 75 SD pairs + quit)
MOVES=""
for i in {1..75}; do
    MOVES="${MOVES}sd"
done
MOVES="${MOVES}q"

# Track overall timing
EXPERIMENT_START=$(date +%s.%N)

for run in {1..50}; do
    RUN_START=$(date +%s.%N)
    
    # Execute game
    OUTPUT=$(echo "$MOVES" | ./2048-debug 2>&1)
    
    # Extract score and max tile
    SCORE=$(echo "$OUTPUT" | grep "Score:" | tail -1 | awk '{print $2}')
    MAX_TILE=$(echo "$OUTPUT" | grep -E "^\|" | grep -oE "[0-9]+" | sort -nr | head -1)
    
    # Calculate timing
    RUN_END=$(date +%s.%N)
    TIME_S=$(echo "$RUN_END - $RUN_START" | bc)
    MOVES_PER_SEC=$(echo "scale=3; 150 / $TIME_S" | bc)
    
    # Save result
    echo "$run,$SCORE,$TIME_S,$MAX_TILE,$MOVES_PER_SEC" >> ../experiments/exp_010/exp_010_results.csv
    
    # Progress with timing prediction
    if (( run % 5 == 0 )); then
        ELAPSED=$(echo "$(date +%s.%N) - $EXPERIMENT_START" | bc)
        AVG_TIME=$(echo "scale=2; $ELAPSED / $run" | bc)
        REMAINING=$(echo "scale=0; $AVG_TIME * (50 - $run) / 60" | bc)
        echo "Progress: $run/50 runs. Elapsed: ${ELAPSED}s. Est. remaining: ${REMAINING} min"
    fi
done

EXPERIMENT_END=$(date +%s.%N)
TOTAL_TIME=$(echo "$EXPERIMENT_END - $EXPERIMENT_START" | bc)

echo -e "\n=== EXPERIMENT COMPLETE ==="
echo "Total time: $(echo "scale=1; $TOTAL_TIME / 60" | bc) minutes"
echo "Ended at $(date)"
