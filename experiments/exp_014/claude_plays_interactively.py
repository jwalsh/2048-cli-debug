#!/usr/bin/env python3
"""
Claude plays 2048 interactively through TTY
"""

import time
import random
from tty_manual.tty_reader import TTYReader
from tty_manual.board_analyzer import BoardAnalyzer

def show_board_state(reader, move_num=0):
    """Display current board for analysis"""
    print(f"\n{'='*50}")
    print(f"Move {move_num} | Score: {reader.current_score}")
    print("="*50)
    
    for row in reader.current_board:
        print("|", end="")
        for cell in row:
            if cell == 0:
                print("      |", end="")
            else:
                print(f"{cell:6}|", end="")
        print()
    print("="*50)

def claude_decide_move(board, score):
    """Claude makes strategic decisions based on current board"""
    # Find important info
    max_tile = max(max(row) for row in board)
    empty_count = sum(1 for row in board for cell in row if cell == 0)
    
    # Find max tile position
    max_pos = None
    for i in range(4):
        for j in range(4):
            if board[i][j] == max_tile:
                max_pos = (i, j)
                break
    
    print(f"\n🧠 Claude thinking...")
    print(f"   Max tile: {max_tile} at {max_pos}")
    print(f"   Empty cells: {empty_count}")
    
    # Critical decisions based on board state
    if empty_count == 0:
        print("   ❗ NO EMPTY CELLS - Emergency!")
        # Try all directions to create space
        return ['a', 'd', 'w', 's']
    
    elif empty_count == 1:
        print("   ⚠️  Only 1 empty - Careful moves")
        # Prioritize merges
        return ['d', 's', 'a', 's']
    
    elif max_pos and max_pos[0] < 3:  # Max not at bottom
        print("   📍 Moving max tile down")
        return ['s', 'd', 's']
    
    else:
        print("   📈 Standard corner strategy")
        return ['s', 'd', 's', 'd', 'a', 's']

def main():
    print("🎮 Claude Plays 2048 Interactively")
    print("Target: Beat 1708!")
    
    reader = TTYReader()
    reader.start_game()
    time.sleep(0.5)
    
    # Initial read
    reader.read_output()
    reader.parse_board_state()
    
    print("\n1️⃣ SPAM PHASE - Building complexity...")
    
    # Spam phase - shorter bursts with checks
    spam_moves = 0
    while spam_moves < 300 and reader.current_score < 400:
        # Send 10 moves at a time
        for _ in range(10):
            r = random.random()
            if r < 0.5:
                move = 's'
            elif r < 0.8:
                move = 'd'
            elif r < 0.9:
                move = 'a'
            else:
                move = 'w'
            
            reader.send_move(move)
            spam_moves += 1
            time.sleep(0.02)
        
        # Check state
        time.sleep(0.1)
        output = reader.read_output()
        reader.parse_board_state()
        
        if spam_moves % 50 == 0:
            print(f"   Spam {spam_moves}: Score {reader.current_score}")
        
        if "Game over" in output:
            print("   Game ended during spam!")
            break
    
    print(f"\n2️⃣ CLAUDE TAKES CONTROL at score {reader.current_score}")
    
    # Show initial state
    show_board_state(reader, spam_moves)
    
    # Claude plays strategically
    total_moves = spam_moves
    stuck_count = 0
    
    while True:
        # Get Claude's decision
        moves = claude_decide_move(reader.current_board, reader.current_score)
        print(f"   Moves: {' '.join(m.upper() for m in moves)}")
        
        # Execute moves
        old_score = reader.current_score
        old_board = [row[:] for row in reader.current_board]
        
        for move in moves:
            reader.send_move(move)
            total_moves += 1
            time.sleep(0.15)  # Slower for strategy
            
            output = reader.read_output()
            reader.parse_board_state()
            
            if "Game over" in output:
                print("\n💀 GAME OVER!")
                show_board_state(reader, total_moves)
                break
        
        # Check progress
        if reader.current_score > old_score:
            print(f"   ✅ Score: {reader.current_score} (+{reader.current_score - old_score})")
            stuck_count = 0
        else:
            # Check if board changed at all
            board_changed = any(
                reader.current_board[i][j] != old_board[i][j]
                for i in range(4) for j in range(4)
            )
            if not board_changed:
                stuck_count += 1
                print(f"   ⚠️  No change (stuck {stuck_count})")
                if stuck_count > 2:
                    print("   Trying emergency moves...")
                    for emergency in ['w', 'a', 's', 'd']:
                        reader.send_move(emergency)
                        time.sleep(0.1)
                    stuck_count = 0
        
        # Show board periodically
        if total_moves % 20 == 0:
            show_board_state(reader, total_moves)
        
        # Check victory
        if reader.current_score > 1708:
            print(f"\n🎉🎉🎉 BEAT HIGH SCORE! {reader.current_score}")
            show_board_state(reader, total_moves)
            break
        
        # Check if game ended
        if "Game over" in output:
            break
        
        # Safety limit
        if total_moves > 1000:
            print("\nReached move limit")
            break
    
    # Final summary
    print(f"\n📊 FINAL RESULTS")
    print(f"   Score: {reader.current_score}")
    print(f"   Total moves: {total_moves}")
    print(f"   Spam moves: {spam_moves}")
    print(f"   Claude moves: {total_moves - spam_moves}")
    
    if reader.current_score > 1708:
        print(f"\n🏆 SUCCESS! Beat 1708 by {reader.current_score - 1708} points!")
    else:
        print(f"\n📈 Progress: {reader.current_score}/1708 ({1708 - reader.current_score} to go)")
    
    reader.cleanup()

if __name__ == "__main__":
    main()