#!/bin/bash
# Speed baseline: 10 runs with direct input
cd ../../2048-cli-0.9.1

echo "=== Speed Baseline: 10 runs of 20 moves each ==="
echo "run,score,time_s" > ../experiments/exp_009/exp_009_results.csv

# Move sequence (20 moves + quit)
MOVES="sdsdsdsdsdsdsdsdsdsdq"

# Time the entire batch
BATCH_START=$(date +%s.%N)

for run in {1..10}; do
    RUN_START=$(date +%s.%N)
    
    # Execute game with direct input
    OUTPUT=$(echo "$MOVES" | ./2048-debug 2>&1)
    
    # Extract score
    SCORE=$(echo "$OUTPUT" | grep "Score:" | tail -1 | awk '{print $2}')
    
    # Calculate time
    RUN_END=$(date +%s.%N)
    TIME_S=$(echo "$RUN_END - $RUN_START" | bc)
    
    # Save result
    echo "$run,$SCORE,$TIME_S" >> ../experiments/exp_009/exp_009_results.csv
    
    echo "Run $run: Score=$SCORE, Time=${TIME_S}s"
done

BATCH_END=$(date +%s.%N)
TOTAL_TIME=$(echo "$BATCH_END - $BATCH_START" | bc)

echo -e "\n=== RESULTS ==="
echo "Total time: ${TOTAL_TIME}s"
echo "Average time per run: $(echo "scale=3; $TOTAL_TIME / 10" | bc)s"

# Quick stats
echo -e "\n=== SCORE STATISTICS ==="
awk -F, 'NR>1 {sum+=$2; if($2>max)max=$2; if(min==""||$2<min)min=$2} END {print "Mean: " sum/(NR-1) "\nMin: " min "\nMax: " max}' ../experiments/exp_009/exp_009_results.csv

# Extrapolation
echo -e "\n=== EXTRAPOLATION ==="
AVG_TIME=$(echo "scale=3; $TOTAL_TIME / 10" | bc)
echo "For 150 moves (7.5x more): ~$(echo "scale=2; $AVG_TIME * 7.5" | bc)s per run"
echo "For 100 runs of 150 moves: ~$(echo "scale=0; $AVG_TIME * 7.5 * 100 / 60" | bc) minutes"
