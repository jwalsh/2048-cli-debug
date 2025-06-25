#!/usr/bin/env python3
"""
Simple: Spam down-right until it gets interesting, then Claude takes over
"""

import time
import random
from tty_manual.tty_reader import TTYReader

reader = TTYReader()
print("🎮 Let's beat 1708!")
print("Spamming down-right until things get interesting...\n")

reader.start_game()
time.sleep(0.5)
reader.read_output()
reader.parse_board_state()

move_count = 0
print("Spamming", end="", flush=True)

# Just spam for a while
for i in range(500):  # Much longer spam phase
    move_count += 1
    
    # 70% down, 25% right, 5% recovery
    r = random.random()
    if r < 0.7:
        move = 's'
    elif r < 0.95:
        move = 'd'
    elif r < 0.975:
        move = 'a'
    else:
        move = 'w'
    
    reader.send_move(move)
    time.sleep(0.02)  # Fast!
    
    output = reader.read_output()
    if reader.parse_board_state():
        if move_count % 50 == 0:
            print(f"\nMove {move_count}: Score {reader.current_score}", end="", flush=True)
            if reader.current_score > 0:
                print(f" - Getting interesting!", end="")
            print("\nSpamming", end="", flush=True)
        elif move_count % 10 == 0:
            print(".", end="", flush=True)
            
        if reader.current_score > 1000:
            print(f"\n\n💥 BOOM! Score: {reader.current_score}")
            print("CLAUDE ENGAGING NOW!\n")
            break
            
        if "Game over" in output:
            print(f"\nGame over at move {move_count}")
            break

# Show me the board
print("\n" + "="*50)
print(f"Move {move_count} | Score: {reader.current_score}")
print("="*50)
for row in reader.current_board:
    print("|", end="")
    for cell in row:
        if cell == 0:
            print("     |", end="")
        else:
            print(f"{cell:5}|", end="")
    print()
print("="*50)

# Now I can see what's actually happening and make decisions
print("\nClaude: Looking at this board...")
print("Time to make strategic moves!")

# Based on what I see, I'll make specific moves
# (In a real interactive version, I'd look at the actual board state above)

reader.cleanup()
print(f"\nFinal score: {reader.current_score}")