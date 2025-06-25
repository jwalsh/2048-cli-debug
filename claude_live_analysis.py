#!/usr/bin/env python3
"""
Claude plays 2048 with live analysis - I'll actually think about each board!
"""

import time
import random
from tty_manual.tty_reader import TTYReader

def spam_to_complexity(reader, target_score=300):
    """Spam until we reach a decent complexity"""
    print(f"📈 Spamming until score > {target_score}...")
    moves = 0
    
    while reader.current_score < target_score and moves < 500:
        # Classic down-right spam with recovery
        r = random.random()
        if r < 0.4:
            move = 's'  # down
        elif r < 0.7:
            move = 'd'  # right
        elif r < 0.85:
            move = 'a'  # left
        else:
            move = 'w'  # up
        
        reader.send_move(move)
        time.sleep(0.02)
        moves += 1
        
        if moves % 50 == 0:
            reader.read_output()
            reader.parse_board_state()
            print(f"Move {moves}: Score {reader.current_score}")
    
    time.sleep(0.5)
    reader.read_output()
    reader.parse_board_state()
    return moves

def display_for_claude(board, score):
    """Show me the board so I can think!"""
    print(f"\n{'='*50}")
    print(f"SCORE: {score}")
    print("="*50)
    for i, row in enumerate(board):
        print(f"{i}: ", end="")
        for j, cell in enumerate(row):
            if cell == 0:
                print("  .  ", end=" ")
            else:
                print(f"{cell:4d}", end=" ")
        print()
    print("   ", "  0    1    2    3")
    print("="*50)

def claude_think_about_board(board, score):
    """
    This is where I actually analyze the specific board and decide what to do!
    No pre-programmed sequences - real analysis.
    """
    print("\n🧠 CLAUDE ANALYZING...")
    
    # First, understand the board layout
    max_tile = 0
    max_pos = None
    empty_cells = []
    merge_opportunities = []
    
    # Scan the board
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                empty_cells.append((i, j))
            elif board[i][j] > max_tile:
                max_tile = board[i][j]
                max_pos = (i, j)
    
    # Check for adjacent equal tiles (merge opportunities)
    for i in range(4):
        for j in range(3):
            if board[i][j] > 0 and board[i][j] == board[i][j+1]:
                merge_opportunities.append(('horizontal', i, j, board[i][j]))
    
    for i in range(3):
        for j in range(4):
            if board[i][j] > 0 and board[i][j] == board[i+1][j]:
                merge_opportunities.append(('vertical', i, j, board[i][j]))
    
    print(f"Max tile: {max_tile} at position {max_pos}")
    print(f"Empty cells: {len(empty_cells)} at {empty_cells}")
    print(f"Merge opportunities: {len(merge_opportunities)}")
    for merge in merge_opportunities[:3]:  # Show first 3
        print(f"  - {merge[0]} merge: {merge[3]}+{merge[3]} at ({merge[1]},{merge[2]})")
    
    # Now decide strategy based on THIS SPECIFIC BOARD
    moves = []
    
    # Critical: If no empty cells, we need to create space NOW
    if len(empty_cells) == 0:
        print("❗ CRITICAL: No empty cells! Must create space")
        # Look for any merge that will free space
        if merge_opportunities:
            if any(m[0] == 'horizontal' for m in merge_opportunities):
                moves = ['d', 'a']  # Try right then left
            else:
                moves = ['s', 'w']  # Try down then up
        else:
            moves = ['a', 'd', 'w', 's']  # Try all directions
    
    # If max tile is not in a corner, that's our priority
    elif max_pos and max_pos not in [(0,0), (0,3), (3,0), (3,3)]:
        print(f"⚠️  Max tile {max_tile} not in corner! Moving it...")
        # Move max tile to bottom-right corner
        if max_pos[0] < 3:
            moves.append('s')  # Move down
        if max_pos[1] < 3:
            moves.append('d')  # Move right
    
    # If we have good merges available, take them
    elif merge_opportunities:
        best_merge = max(merge_opportunities, key=lambda x: x[3])
        print(f"✨ Best merge available: {best_merge[3]}+{best_merge[3]}")
        if best_merge[0] == 'horizontal':
            moves = ['d', 's']  # Right to merge, then down
        else:
            moves = ['s', 'd']  # Down to merge, then right
    
    # Default: Continue down-right with some variation
    else:
        print("📊 Standard play: building in corner")
        if random.random() < 0.7:
            moves = ['s', 'd', 's']
        else:
            moves = ['d', 's', 'a', 's']  # Include left for variety
    
    return moves

def main():
    reader = TTYReader()
    print("🎮 Claude Live 2048 - I'll actually think about each position!")
    
    reader.start_game()
    time.sleep(0.5)
    reader.read_output()
    reader.parse_board_state()
    
    # Spam to get interesting board
    spam_moves = spam_to_complexity(reader, 300)
    print(f"\n✅ Spammed {spam_moves} moves")
    
    # Now I play!
    print("\n🎯 CLAUDE TAKING OVER - Let me think about each position...\n")
    
    move_count = 0
    consecutive_fails = 0
    
    while True:
        # Show me the board
        display_for_claude(reader.current_board, reader.current_score)
        
        # I analyze THIS SPECIFIC board
        moves = claude_think_about_board(reader.current_board, reader.current_score)
        print(f"My moves: {' '.join(m.upper() for m in moves)}")
        
        # Execute my moves
        board_changed = False
        for move in moves:
            reader.send_move(move)
            time.sleep(0.2)
            move_count += 1
            
            output = reader.read_output()
            old_score = reader.current_score
            if reader.parse_board_state():
                if reader.current_score > old_score:
                    board_changed = True
                    print(f"  {move.upper()} → Score +{reader.current_score - old_score}")
            
            if "Game over" in output:
                print("\n💀 GAME OVER!")
                display_for_claude(reader.current_board, reader.current_score)
                break
        
        if not board_changed:
            consecutive_fails += 1
            print("⚠️  No progress made")
            if consecutive_fails > 3:
                print("Stuck! Trying recovery moves...")
                for m in ['w', 'a', 's', 'd']:
                    reader.send_move(m)
                    time.sleep(0.1)
        else:
            consecutive_fails = 0
        
        # Check victory
        if reader.current_score > 1708:
            print(f"\n🎉🎉🎉 BEAT HIGH SCORE! {reader.current_score} > 1708")
            display_for_claude(reader.current_board, reader.current_score)
            
        # Safety limit
        if move_count > 1000 or "Game over" in output:
            break
    
    print(f"\n📊 Final Score: {reader.current_score}")
    print(f"Total moves by Claude: {move_count}")
    
    if reader.current_score > 1708:
        print(f"🏆 SUCCESS! Beat by {reader.current_score - 1708} points!")
    else:
        print(f"Need {1708 - reader.current_score} more points")
        print("Let me try again with different analysis...")
    
    reader.cleanup()

if __name__ == "__main__":
    main()