#!/usr/bin/env python3
"""
Claude just plays 2048 - simple and direct
"""

import time
import subprocess

def main():
    print("🎮 Claude plays 2048 - Let's beat 1708!")
    
    # First, run spam to get a complex board
    print("\n1️⃣ Running spam phase...")
    spam_result = subprocess.run(['./claude_takeover.sh'], capture_output=True, text=True)
    
    # Extract the board from output
    output_lines = spam_result.stdout.split('\n')
    
    # Find the last board state
    board_lines = []
    score = 0
    for i, line in enumerate(output_lines):
        if "Score:" in line and i < len(output_lines) - 10:
            # Extract score
            try:
                score = int(line.split("Score:")[1].split()[0])
            except:
                pass
            # Get the board
            for j in range(i+2, min(i+6, len(output_lines))):
                if "|" in output_lines[j]:
                    board_lines.append(output_lines[j])
    
    if not board_lines:
        print("Failed to get board state!")
        return
    
    print(f"\n2️⃣ Got board with score {score}:")
    for line in board_lines:
        print(line)
    
    print("\n3️⃣ Claude's Analysis:")
    
    # Parse the board to understand it
    board = []
    for line in board_lines:
        row = []
        cells = line.split("|")[1:-1]  # Skip first and last empty
        for cell in cells:
            try:
                val = int(cell.strip())
                row.append(val)
            except:
                row.append(0)
        if len(row) == 4:
            board.append(row)
    
    if len(board) != 4:
        print("Failed to parse board!")
        return
    
    # Find key info
    max_tile = max(max(row) for row in board)
    empty_count = sum(1 for row in board for cell in row if cell == 0)
    
    print(f"Max tile: {max_tile}")
    print(f"Empty cells: {empty_count}")
    
    # Strategy based on this specific board
    if empty_count == 0:
        print("❗ CRITICAL - No empty cells! Emergency moves needed")
        moves = "asdw"  # Try all directions
    elif empty_count == 1:
        print("⚠️  Only 1 empty cell - careful consolidation")
        moves = "sdas" * 5  # Down-right with left recovery
    elif max_tile >= 64:
        print("🎯 Building big tiles - focus on merging")
        moves = "ssddssddassddssdd"
    else:
        print("📈 Standard strategy - build in corner")
        moves = "sdsdsdasdsdsdsdasdsd"
    
    print(f"\n4️⃣ My move sequence: {moves}")
    
    # Now continue playing with these moves
    print("\n5️⃣ Executing moves...")
    
    # Create a new game and send our moves
    game_cmd = f"echo '{moves}q' | 2048-cli-0.9.1/2048"
    result = subprocess.run(game_cmd, shell=True, capture_output=True, text=True)
    
    # Find final score
    final_score = 0
    for line in result.stdout.split('\n'):
        if "Score:" in line:
            try:
                final_score = int(line.split("Score:")[1].split()[0])
            except:
                pass
    
    print(f"\n📊 Final Score: {final_score}")
    if final_score > 1708:
        print(f"🎉 BEAT HIGH SCORE by {final_score - 1708} points!")
    else:
        print(f"Need {1708 - final_score} more points")
        print("\nLet me think harder about the strategy...")

if __name__ == "__main__":
    main()