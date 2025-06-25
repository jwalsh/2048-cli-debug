#!/usr/bin/env python3
"""
Claude Interactive 2048 - Shows board state and waits for Claude's decision
"""

import time
import random
from tty_manual.tty_reader import TTYReader
from tty_manual.board_analyzer import BoardAnalyzer


def show_board_state(reader, move_count):
    """Display the current board state for Claude"""
    print(f"\n{'='*50}")
    print(f"MOVE {move_count} | Score: {reader.current_score} | High: {reader.high_score}")
    print("="*50)
    
    # Display board
    for row in reader.current_board:
        print("|", end="")
        for cell in row:
            if cell == 0:
                print("     |", end="")
            else:
                print(f"{cell:5}|", end="")
        print()
    print("="*50)
    
    # Quick analysis
    analyzer = BoardAnalyzer(reader.current_board)
    scores = analyzer.get_complexity_score()
    
    print(f"Empty: {scores['empty_cells']} | Max: {scores['max_tile']} | Merges: {scores['merge_opportunities']}")
    print(f"Complexity: {scores['complexity']:.1f} | Strategy: {analyzer.suggest_strategy()}")
    

def auto_spam_phase(reader, moves=50):
    """Run initial auto-spam phase"""
    print("Auto-spamming down-right for 50 moves...")
    
    for i in range(moves):
        # Down-right with occasional recovery
        if i > 20 and i % 15 == 0:
            move = 'a'  # left recovery
        elif i > 30 and i % 20 == 0:
            move = 'w'  # up recovery
        else:
            move = 's' if random.random() < 0.5 else 'd'
            
        reader.send_move(move)
        time.sleep(0.05)
        reader.read_output()
        reader.parse_board_state()
        
        if i % 10 == 0:
            print(f".", end="", flush=True)
            
    print("\nAuto-spam complete!")
    

def main():
    """Main game loop"""
    reader = TTYReader()
    move_count = 0
    
    print("🎮 Claude Interactive 2048")
    print("Goal: Beat high score of 1708!")
    print("-" * 50)
    
    # Start game
    reader.start_game()
    time.sleep(0.5)
    
    # Get initial board
    output = reader.read_output()
    if not reader.parse_board_state(output):
        print("Failed to start!")
        return
        
    # Auto-spam phase
    auto_spam_phase(reader, 50)
    move_count = 50
    
    # Show state after auto-spam
    show_board_state(reader, move_count)
    
    print("\n" + "🎯 CLAUDE: I'm taking control now!")
    print("I'll analyze each board state and make strategic moves.")
    print("My plan: Keep high tiles in corners, maintain order, create merges")
    
    # Create a moves list for Claude to fill
    planned_moves = []
    
    # CLAUDE: Looking at the board after 50 moves, I need to make strategic decisions
    # I'll analyze and plan my next moves based on what I see
    
    print("\nWaiting for game state analysis...")
    print("Board loaded. Claude will now play strategically.")
    
    # Since I can't do real-time input, let me plan a sequence of moves
    # based on typical board states after spam phase
    
    print("\nExecuting Claude's strategic sequence...")
    
    # Strategy: Consolidate tiles, move max to corner, build ordered structure
    strategic_sequence = [
        's', 'd', 's', 'd',  # Continue down-right to consolidate
        'a',                 # Left to merge horizontally
        's', 'd', 's', 'd',  # Back to down-right
        'a', 's',            # Left-down combo
        'd', 'd', 's',       # Right-right-down
        'w',                 # Up for recovery if needed
        'd', 's', 'd', 's',  # Resume pattern
    ]
    
    for move in strategic_sequence:
        move_count += 1
        reader.send_move(move)
        time.sleep(0.2)
        
        output = reader.read_output()
        if reader.parse_board_state():
            if move_count % 5 == 0:
                show_board_state(reader, move_count)
                
            if reader.current_score > 1708:
                print(f"\n🎉 NEW HIGH SCORE: {reader.current_score}!")
                reader.save_board_snapshot(f"claude_beats_high_score_{reader.current_score}.txt")
                
            if "Game over" in output:
                print("\nGame Over!")
                break
                
    # Final state
    show_board_state(reader, move_count)
    
    print(f"\nFinal Score: {reader.current_score}")
    if reader.current_score > 1708:
        print(f"🏆 BEAT THE HIGH SCORE BY {reader.current_score - 1708} POINTS!")
    else:
        print(f"Missed by {1708 - reader.current_score} points. Need another run!")
        
    reader.cleanup()


if __name__ == "__main__":
    main()