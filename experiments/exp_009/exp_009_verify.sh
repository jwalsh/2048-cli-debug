#!/bin/bash
# Single run to verify direct input works
cd /Users/jasonwalsh/projects/jwalsh/2048/2048-cli-0.9.1

echo "=== Direct Input Verification (20 moves + quit) ==="

# Generate move sequence: 20 moves then quit
MOVES="sdsdsdsdsdsdsdsdsdsdq"

# Time single run
START=$(date +%s.%N)
OUTPUT=$(echo "$MOVES" | ./2048-debug 2>&1)
END=$(date +%s.%N)
TIME=$(echo "$END - $START" | bc)

# Extract final score
SCORE=$(echo "$OUTPUT" | grep "Score:" | tail -1 | awk '{print $2}')
echo "Final Score: $SCORE"
echo "Time: ${TIME}s"

# Show final board state
echo -e "\nFinal Board:"
echo "$OUTPUT" | grep -A 10 "Score:" | tail -11
