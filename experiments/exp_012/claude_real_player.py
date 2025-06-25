#!/usr/bin/env python3
"""
Claude plays 2048 by analyzing real board states and making strategic decisions
"""

import time
import random
from tty_manual.tty_reader import TTYReader
from tty_manual.board_analyzer import BoardAnalyzer

def spam_phase(reader, moves=400):
    """Run initial spam phase"""
    print("🎮 Running spam phase...")
    for i in range(moves):
        r = random.random()
        if r < 0.5:
            move = 's'  # down
        elif r < 0.8:
            move = 'd'  # right
        elif r < 0.9:
            move = 'a'  # left
        else:
            move = 'w'  # up
        
        reader.send_move(move)
        time.sleep(0.02)
        
        if i % 50 == 0:
            print(f"Spam move {i}...")
    
    # Let it settle
    time.sleep(0.5)
    reader.read_output()
    reader.parse_board_state()
    
    print(f"Spam complete! Score: {reader.current_score}")
    return reader.current_score

def show_board(board, score):
    """Display board for Claude to analyze"""
    print(f"\nScore: {score}")
    print("-" * 29)
    for row in board:
        print("|", end="")
        for cell in row:
            if cell == 0:
                print("      |", end="")
            else:
                print(f"{cell:6}|", end="")
        print()
    print("-" * 29)

def claude_analyze_board(board):
    """Claude's strategic analysis of the board"""
    # Find key metrics
    max_tile = max(max(row) for row in board)
    empty_cells = sum(1 for row in board for cell in row if cell == 0)
    
    # Find tile positions
    tiles_32_plus = []
    for i in range(4):
        for j in range(4):
            if board[i][j] >= 32:
                tiles_32_plus.append((board[i][j], i, j))
    
    # Determine strategy based on board state
    if empty_cells == 0:
        return "CRITICAL", ['a', 'd', 's']  # Try to create space
    elif empty_cells == 1:
        return "URGENT", ['d', 's', 'a', 's', 'd']  # Careful consolidation
    elif max_tile >= 64 and tiles_32_plus:
        return "BUILD", ['s', 'd', 's', 'd', 'a', 's', 'd']  # Focus on merging big tiles
    else:
        return "CONSOLIDATE", ['s', 'd', 's', 'a', 's', 'd', 'd', 's']  # General play

def main():
    reader = TTYReader()
    print("🎮 Claude's 2048 Challenge: Beat 1708!")
    
    # Start game
    reader.start_game()
    time.sleep(0.5)
    
    # Run spam phase
    spam_score = spam_phase(reader, 400)
    
    # Show initial state for Claude
    print("\n" + "="*50)
    print("CLAUDE TAKING CONTROL")
    print("="*50)
    show_board(reader.current_board, reader.current_score)
    
    # Claude analyzes
    analyzer = BoardAnalyzer(reader.current_board)
    complexity = analyzer.get_complexity_score()
    print(f"\nComplexity: {complexity['complexity']:.1f}")
    
    # Main game loop
    move_count = 0
    while True:
        # Claude analyzes current board
        strategy, moves = claude_analyze_board(reader.current_board)
        print(f"\nStrategy: {strategy}")
        
        # Execute move sequence
        for move in moves:
            move_count += 1
            reader.send_move(move)
            time.sleep(0.2)
            
            output = reader.read_output()
            if not reader.parse_board_state():
                print("Failed to read board!")
                break
                
            # Check for game over
            if "Game over" in output:
                print("\n💀 Game Over!")
                break
        
        # Show board every few moves
        if move_count % 10 == 0:
            show_board(reader.current_board, reader.current_score)
            
        # Check if we beat high score
        if reader.current_score > 1708:
            print(f"\n🎉 BEAT HIGH SCORE! Score: {reader.current_score}")
            show_board(reader.current_board, reader.current_score)
            
        # Check for game over in output
        if "Game over" in output:
            break
            
        # Safety check
        if move_count > 1000:
            print("Reached move limit")
            break
    
    # Final results
    print(f"\n📊 Final Score: {reader.current_score}")
    if reader.current_score > 1708:
        print(f"🏆 SUCCESS! Beat high score by {reader.current_score - 1708} points!")
    else:
        print(f"Need {1708 - reader.current_score} more points")
    
    reader.cleanup()

if __name__ == "__main__":
    main()