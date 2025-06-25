#!/bin/bash
# Deep run: 100 runs with 40 moves each
cd ../../2048-cli-0.9.1

echo "=== Deep Run: 100 runs of 40 moves each ==="
echo "run,score,time_s,max_tile" > ../experiments/exp_009/exp_009_deep_results.csv

# Move sequence (40 moves + quit) 
MOVES="sdsdsdsdsdsdsdsdsdsdsdsdsdsdsdsdsdsdsdsdq"

# Time the entire batch
BATCH_START=$(date +%s.%N)

for run in {1..100}; do
    RUN_START=$(date +%s.%N)
    
    # Execute game with direct input
    OUTPUT=$(echo "$MOVES" | ./2048-debug 2>&1)
    
    # Extract score
    SCORE=$(echo "$OUTPUT" | grep "Score:" | tail -1 | awk '{print $2}')
    
    # Extract max tile
    MAX_TILE=$(echo "$OUTPUT" | grep -E "^\|" | grep -oE "[0-9]+" | sort -nr | head -1)
    
    # Calculate time
    RUN_END=$(date +%s.%N)
    TIME_S=$(echo "$RUN_END - $RUN_START" | bc)
    
    # Save result
    echo "$run,$SCORE,$TIME_S,$MAX_TILE" >> ../experiments/exp_009/exp_009_deep_results.csv
    
    # Progress indicator
    if (( run % 10 == 0 )); then
        echo "Progress: $run/100 runs completed"
    fi
done

BATCH_END=$(date +%s.%N)
TOTAL_TIME=$(echo "$BATCH_END - $BATCH_START" | bc)

echo -e "\n=== TIMING STATISTICS ==="
echo "Total time: ${TOTAL_TIME}s"
echo "Average time per run: $(echo "scale=3; $TOTAL_TIME / 100" | bc)s"
awk -F, 'NR>1 {sum+=$3; if($3>max)max=$3; if(min==""||$3<min)min=$3} END {
    avg=sum/(NR-1); 
    print "Min time: " min "s"; 
    print "Max time: " max "s";
    print "Avg time: " avg "s"
}' ../experiments/exp_009/exp_009_deep_results.csv

echo -e "\n=== SCORE STATISTICS ==="
awk -F, 'NR>1 {sum+=$2; if($2>max)max=$2; if(min==""||$2<min)min=$2} END {
    avg=sum/(NR-1); 
    print "Mean score: " avg; 
    print "Min score: " min; 
    print "Max score: " max
}' ../experiments/exp_009/exp_009_deep_results.csv

# Max tile distribution
echo -e "\n=== MAX TILE DISTRIBUTION ==="
awk -F, 'NR>1 {tiles[$4]++} END {for (t in tiles) print t ": " tiles[t] " (" tiles[t] "%)"}' ../experiments/exp_009/exp_009_deep_results.csv | sort -n
