#!/bin/bash
# Compare direct input vs tmux approach (5 runs each for quick test)
cd /Users/jasonwalsh/projects/jwalsh/2048/2048-cli-0.9.1

echo "=== Speed Comparison: Direct vs tmux (5 runs each, 20 moves) ==="

# Direct input test
echo -e "\n--- Direct Input ---"
DIRECT_START=$(date +%s.%N)
MOVES="sdsdsdsdsdsdsdsdsdsdq"

for run in {1..5}; do
    echo "$MOVES" | ./2048-debug > /dev/null 2>&1
done
DIRECT_END=$(date +%s.%N)
DIRECT_TIME=$(echo "$DIRECT_END - $DIRECT_START" | bc)
echo "5 runs in ${DIRECT_TIME}s"
echo "Average: $(echo "scale=3; $DIRECT_TIME / 5" | bc)s per run"

# tmux test
echo -e "\n--- tmux Approach ---"
TMUX_START=$(date +%s.%N)
for run in {1..5}; do
    tmux new-session -d -s "speed_$run" -c "$(pwd)" "./2048-debug"
    sleep 0.5
    for i in {1..10}; do
        tmux send-keys -t "speed_$run" "s"
        sleep 0.05
        tmux send-keys -t "speed_$run" "d"
        sleep 0.05
    done
    tmux send-keys -t "speed_$run" "q"
    sleep 0.2
    tmux kill-session -t "speed_$run" 2>/dev/null
done
TMUX_END=$(date +%s.%N)
TMUX_TIME=$(echo "$TMUX_END - $TMUX_START" | bc)
echo "5 runs in ${TMUX_TIME}s"
echo "Average: $(echo "scale=3; $TMUX_TIME / 5" | bc)s per run"

# Calculate speedup
SPEEDUP=$(echo "scale=1; $TMUX_TIME / $DIRECT_TIME" | bc)
echo -e "\n=== SPEEDUP: ${SPEEDUP}x faster with direct input ==="
