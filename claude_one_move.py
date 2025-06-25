#!/usr/bin/env python3
"""
Claude makes just ONE move from initial state
"""

import time
from tty_manual.tty_reader import TTYReader

def main():
    print("🎮 Claude: One Move Test")
    print("="*40)
    
    reader = TTYReader()
    
    # Start the game
    print("\n1. Starting game...")
    reader.start_game()
    time.sleep(0.5)
    
    # Read initial state
    print("\n2. Reading initial board...")
    output = reader.read_output()
    reader.parse_board_state()
    
    print(f"\nInitial Score: {reader.current_score}")
    print("Initial Board:")
    for row in reader.current_board:
        print(row)
    
    # Make ONE move
    print("\n3. Making one move: DOWN (s)")
    reader.send_move('s')
    time.sleep(0.5)
    
    # Read result
    print("\n4. Reading result...")
    output = reader.read_output()
    reader.parse_board_state()
    
    print(f"\nScore after move: {reader.current_score}")
    print("Board after move:")
    for row in reader.current_board:
        print(row)
    
    # Clean up
    print("\n5. Cleaning up...")
    reader.cleanup()
    
    print("\n✅ Test complete!")

if __name__ == "__main__":
    main()