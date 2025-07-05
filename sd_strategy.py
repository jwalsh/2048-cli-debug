#!/usr/bin/env python3

import subprocess
import time

# Better strategy: alternate between sd sequences and recovery
moves = []

# Build move sequence
for i in range(50):
    # 10 sd moves
    moves.append('sd' * 10)
    # Recovery: try different directions
    moves.append('wa')  # up-left to consolidate

# Send all moves
all_moves = ''.join(moves)
subprocess.run(['tmux', 'send-keys', '-t', 'game2048', all_moves])

# Wait for completion
time.sleep(5)

# Capture result
result = subprocess.run(['tmux', 'capture-pane', '-t', 'game2048', '-p'], 
                      capture_output=True, text=True)

print("Game result:")
print(result.stdout)

# Save for screenshot
with open('sd_high_score.txt', 'w') as f:
    f.write(result.stdout)