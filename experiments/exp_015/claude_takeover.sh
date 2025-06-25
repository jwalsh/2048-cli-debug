#!/bin/bash
# Run down-right spam then show board for Claude to take over

echo "🎮 Claude's Turn to Beat 1708!"
echo "Running down-right spam first..."

# Generate moves: 400 spam moves then pause
SPAM_MOVES=""
for i in {1..400}; do
    RAND=$((RANDOM % 10))
    if [ $RAND -lt 5 ]; then
        SPAM_MOVES="${SPAM_MOVES}s"  # down
    elif [ $RAND -lt 8 ]; then
        SPAM_MOVES="${SPAM_MOVES}d"  # right  
    elif [ $RAND -lt 9 ]; then
        SPAM_MOVES="${SPAM_MOVES}a"  # left (recovery)
    else
        SPAM_MOVES="${SPAM_MOVES}w"  # up (recovery)
    fi
done

# Add a quit at the end to capture final state
SPAM_MOVES="${SPAM_MOVES}q"

# Run game and capture output
echo "$SPAM_MOVES" | 2048-cli-0.9.1/2048 | tee /tmp/claude_game.txt

# Extract final board state
echo ""
echo "="*60
echo "BOARD STATE AFTER SPAM:"
echo "="*60

# Show the last board state
tail -20 /tmp/claude_game.txt | grep -A 10 "Score:" | head -10

echo ""
echo "Claude: Now I need to see this board and plan my moves..."
echo "Based on the board above, I would continue with strategic moves"