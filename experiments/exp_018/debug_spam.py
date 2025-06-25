#!/usr/bin/env python3
"""
Debug why spam isn't working
"""

import time
from tty_manual.tty_reader import TTYReader

reader = TTYReader()
reader.start_game()
time.sleep(0.5)

output = reader.read_output()
reader.parse_board_state()

print("Initial board:")
for row in reader.current_board:
    print(row)
print(f"Score: {reader.current_score}\n")

# Try specific moves and see what happens
moves = ['s', 's', 'd', 'd', 's', 'd', 'a', 's', 'd', 's']

for i, move in enumerate(moves):
    print(f"Move {i+1}: {move}")
    reader.send_move(move)
    time.sleep(0.2)
    
    output = reader.read_output()
    if reader.parse_board_state():
        print("Board after move:")
        for row in reader.current_board:
            print(row)
        print(f"Score: {reader.current_score}")
        print(f"Output snippet: {output[:100] if output else 'No output'}")
        print("-" * 40)
    else:
        print("Failed to parse board!")
        print(f"Raw output: {output[:200]}")
        
reader.cleanup()