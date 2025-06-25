#!/bin/bash
# Simple statistics for exp_009 deep results

echo "=== DEEP RUN STATISTICS (92 runs, 40 moves) ==="

# Score stats
echo -e "\n--- SCORE STATISTICS ---"
awk -F, 'NR>1 {
    sum+=$2; 
    if($2>max || NR==2)max=$2; 
    if($2<min || NR==2)min=$2;
    scores[NR-1]=$2
} END {
    avg=sum/(NR-1);
    print "Mean: " avg;
    print "Min: " min;
    print "Max: " max;
    print "Range: " max-min;
}' exp_009_deep_results.csv

# Timing stats  
echo -e "\n--- TIMING STATISTICS ---"
awk -F, 'NR>1 {
    sum+=$3;
    if($3>max || NR==2)max=$3;
    if($3<min || NR==2)min=$3;
} END {
    avg=sum/(NR-1);
    print "Mean: " avg "s";
    print "Min: " min "s"; 
    print "Max: " max "s";
}' exp_009_deep_results.csv

# Max tile distribution
echo -e "\n--- MAX TILE DISTRIBUTION ---"
awk -F, 'NR>1 {tiles[$4]++} END {
    for (t in tiles) {
        pct = tiles[t] * 100 / (NR-1);
        printf "%d: %d runs (%.1f%%)\n", t, tiles[t], pct;
    }
}' exp_009_deep_results.csv | sort -n

# Score distribution by bins
echo -e "\n--- SCORE DISTRIBUTION (bins of 50) ---"
awk -F, 'NR>1 {
    bin = int($2/50)*50;
    bins[bin]++;
} END {
    for (b in bins) {
        printf "%d-%d: %d runs\n", b, b+49, bins[b];
    }
}' exp_009_deep_results.csv | sort -n