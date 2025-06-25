#!/bin/bash
# Start game and capture initial state

# Use script to capture TTY output
script -q /tmp/game_session.txt <<EOF
2048-cli-0.9.1/2048 <<GAME
q
GAME
EOF

# Show the game board
echo "Current game state:"
cat /tmp/game_session.txt | grep -A 10 "Score:" | tail -8