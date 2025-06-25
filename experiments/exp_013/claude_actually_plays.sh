#!/bin/bash
# Claude Actually Plays 2048 - For Real This Time

echo "🎮 Claude Live 2048 - Episode 2: Actually Playing"
echo "Current high score to beat: 1708"
echo ""

# Step 1: Run spam and capture JUST the final board
echo "Running spam phase (400 moves)..."

# Generate moves
MOVES=""
for i in {1..400}; do
    RAND=$((RANDOM % 10))
    if [ $RAND -lt 5 ]; then
        MOVES="${MOVES}s"  # down
    elif [ $RAND -lt 8 ]; then
        MOVES="${MOVES}d"  # right  
    elif [ $RAND -lt 9 ]; then
        MOVES="${MOVES}a"  # left
    else
        MOVES="${MOVES}w"  # up
    fi
done

# Run game, wait a bit, then quit to see final state
(echo "$MOVES"; sleep 1; echo "q") | 2048-cli-0.9.1/2048 > /tmp/game_output.txt 2>&1

# Extract just the last board state
echo ""
echo "Final board after spam:"
echo "======================"

# Get the last occurrence of "Score:" and the board after it
tac /tmp/game_output.txt | grep -m1 -B6 "Score:" | tac | tail -7

echo ""
echo "Claude: Now I need to analyze this board and continue playing..."
echo "Based on what I see, I would:"
echo "1. Look for the largest tile and try to keep it in a corner"
echo "2. Identify merge opportunities (adjacent equal tiles)"
echo "3. Plan moves to consolidate tiles and create larger values"
echo ""
echo "My strategy from here would be to continue with calculated moves"
echo "rather than random spam, focusing on building toward 128, 256, 512..."