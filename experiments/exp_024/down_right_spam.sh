#!/bin/bash
# The "academic" strategy: just spam down and right!

echo "🎯 2048 Down-Right Strategy"
echo "Based on actual heuristics papers!"
echo "Target: 1000+ points"
echo ""

# Generate a long sequence of down (s) and right (d) moves
# Throw in occasional left/up when stuck
MOVES=""
for i in {1..500}; do
    # 80% down/right, 20% recovery moves
    RAND=$((RANDOM % 10))
    if [ $RAND -lt 4 ]; then
        MOVES="${MOVES}s"  # down
    elif [ $RAND -lt 8 ]; then
        MOVES="${MOVES}d"  # right  
    elif [ $RAND -lt 9 ]; then
        MOVES="${MOVES}a"  # left (recovery)
    else
        MOVES="${MOVES}w"  # up (last resort)
    fi
done

echo "Strategy: $(echo $MOVES | head -c 50)..."
echo "Total moves: ${#MOVES}"
echo ""

# Run the game
echo "$MOVES" | tr -d '\n' | (
    cat
    sleep 0.5
    echo "q"
) | 2048-cli-0.9.1/2048 | tee /tmp/2048_downright.txt

# Check final score
echo ""
if grep -E "Score:.*[0-9]+" /tmp/2048_downright.txt > /tmp/scores_dr.txt; then
    HIGHEST=$(grep -oE "[0-9]+" /tmp/scores_dr.txt | sort -n | tail -1)
    echo "Final score: $HIGHEST"
    
    if [ "$HIGHEST" -ge 1000 ]; then
        echo "🎉 SUCCESS! The academic heuristic works: $HIGHEST points!"
    else
        echo "Score: $HIGHEST - Need more down-right power!"
    fi
fi