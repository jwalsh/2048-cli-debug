#!/bin/bash
# Capture game display using screen

# Create a screen session and run the game
screen -dmS game2048 ./2048

# Let it start
sleep 1

# Send some moves (w=up, a=left, s=down, d=right)
screen -S game2048 -X stuff "w"
sleep 0.5
screen -S game2048 -X stuff "d" 
sleep 0.5
screen -S game2048 -X stuff "s"
sleep 0.5
screen -S game2048 -X stuff "a"
sleep 0.5

# Capture the screen
screen -S game2048 -X hardcopy game-screenshot.txt

# Kill the session
screen -S game2048 -X quit

# Display the captured screen
echo "=== Captured Game Display ==="
cat game-screenshot.txt