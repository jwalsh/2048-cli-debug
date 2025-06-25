#!/usr/bin/env python3
"""
Claude plays strategically from a complicated board state
"""

import time
from tty_manual.tty_reader import TTYReader
from tty_manual.board_analyzer import BoardAnalyzer

def display_board(reader):
    """Show current board state"""
    print(f"\nScore: {reader.current_score} | High: {reader.high_score}")
    print("-" * 29)
    for row in reader.current_board:
        print("|", end="")
        for cell in row:
            if cell == 0:
                print("      |", end="")
            else:
                print(f"{cell:6}|", end="")
        print()
    print("-" * 29)

def main():
    reader = TTYReader()
    
    # First, recreate the board state by running spam
    print("🎮 Setting up complicated board...")
    reader.start_game()
    time.sleep(0.5)
    
    # Run 400 spam moves like before
    moves = ""
    for i in range(400):
        r = i % 10
        if r < 5:
            moves += 's'  # down
        elif r < 8:
            moves += 'd'  # right
        elif r < 9:
            moves += 'a'  # left
        else:
            moves += 'w'  # up
    
    # Send all moves quickly
    for move in moves:
        reader.send_move(move)
        time.sleep(0.01)
    
    # Let it settle and read final state
    time.sleep(0.5)
    output = reader.read_output()
    reader.parse_board_state()
    
    print("\n" + "="*50)
    print("BOARD STATE ACHIEVED - CLAUDE TAKING OVER")
    print("="*50)
    display_board(reader)
    
    # Analyze the board
    analyzer = BoardAnalyzer(reader.current_board)
    scores = analyzer.get_complexity_score()
    print(f"\nComplexity: {scores['complexity']:.1f}")
    print(f"Strategy suggestion: {analyzer.suggest_strategy()}")
    
    # CLAUDE'S STRATEGIC ANALYSIS:
    # Looking at the board, I see two 32s that need consolidation
    # The bottom-left corner is empty - I should use it strategically
    # Multiple merge opportunities exist
    
    print("\n🧠 CLAUDE: Analyzing board...")
    print("I see two 32s that need to be merged")
    print("Strategy: Consolidate tiles, merge 32s, build toward 64")
    
    strategic_moves = [
        # First, try to consolidate bottom row
        ('a', "Left to align bottom row"),
        ('s', "Down to drop tiles"),
        ('d', "Right to merge 8s"),
        ('s', "Down to compact"),
        
        # Try to get 32s together
        ('a', "Left to shift tiles"),
        ('s', "Down to align 32s"),
        ('d', "Right to position for merge"),
        
        # Continue building
        ('s', "Down to compact"),
        ('d', "Right to merge"),
        ('s', "Down again"),
        
        # Recovery moves if needed
        ('a', "Left for space"),
        ('s', "Down to consolidate"),
        ('d', "Right to continue pattern"),
        
        # Push for higher tiles
        ('s', "Down"),
        ('d', "Right"),
        ('s', "Down"),
        ('a', "Left recovery"),
        ('s', "Down"),
        ('d', "Right"),
        ('s', "Down final push"),
    ]
    
    print("\nExecuting strategic sequence...")
    
    for i, (move, reason) in enumerate(strategic_moves):
        print(f"\nMove {i+1}: {move.upper()} - {reason}")
        reader.send_move(move)
        time.sleep(0.3)
        
        output = reader.read_output()
        if reader.parse_board_state():
            display_board(reader)
            
            # Check for achievements
            if reader.current_score > 1708:
                print(f"\n🎉 BEAT HIGH SCORE! New score: {reader.current_score}")
                print(f"Beat it by {reader.current_score - 1708} points!")
                
            # Check if we made a 64 or higher
            max_tile = max(max(row) for row in reader.current_board)
            if max_tile >= 64:
                print(f"✨ Created a {max_tile} tile!")
                
            if "Game over" in output:
                print("\n💀 Game Over!")
                break
    
    print(f"\n📊 Final Score: {reader.current_score}")
    if reader.current_score > 1708:
        print("🏆 SUCCESS! Beat the high score!")
    else:
        print(f"Need {1708 - reader.current_score} more points to beat high score")
    
    reader.cleanup()

if __name__ == "__main__":
    main()