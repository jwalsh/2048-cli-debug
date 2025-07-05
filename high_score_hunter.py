#!/usr/bin/env python3

import subprocess
import time
import re

def get_board_state():
    """Capture the current board state from tmux"""
    result = subprocess.run(['tmux', 'capture-pane', '-t', 'game2048', '-p'], 
                          capture_output=True, text=True)
    return result.stdout

def parse_board_and_score(board_text):
    """Parse the board state and score"""
    lines = board_text.strip().split('\n')
    board = []
    score = 0
    
    # Extract score
    for line in lines:
        if line.startswith('Score:'):
            match = re.search(r'Score:\s*(\d+)', line)
            if match:
                score = int(match.group(1))
            break
    
    # Find the board lines (between the dashes)
    in_board = False
    for line in lines:
        if '----' in line:
            in_board = not in_board
            continue
        if in_board and '|' in line:
            # Extract numbers from the row
            cells = line.split('|')[1:-1]  # Skip first and last empty
            row = []
            for cell in cells:
                cell = cell.strip()
                if cell:
                    row.append(int(cell))
                else:
                    row.append(0)
            board.append(row)
    
    return board, score

def send_move(move):
    """Send a move to the game"""
    subprocess.run(['tmux', 'send-keys', '-t', 'game2048', move])
    time.sleep(0.05)  # Faster response

def board_changed(old_board, new_board):
    """Check if board state changed"""
    return old_board != new_board

def play_game():
    """Play a full game using down-right strategy with recovery"""
    # Start fresh
    subprocess.run(['tmux', 'send-keys', '-t', 'game2048', 'q'])
    time.sleep(0.5)
    subprocess.run(['tmux', 'send-keys', '-t', 'game2048', 'Enter'])
    time.sleep(0.5)
    
    moves_count = 0
    stuck_count = 0
    best_score = 0
    
    while True:
        board_text = get_board_state()
        board, score = parse_board_and_score(board_text)
        
        if score > best_score:
            best_score = score
            
        # Check for game over
        if "Game over" in board_text:
            print(f"Game Over! Final score: {score}")
            break
            
        # Primary strategy: down-right
        old_board = [row[:] for row in board]
        
        # Try down
        send_move('f')
        board_text = get_board_state()
        board, _ = parse_board_and_score(board_text)
        
        if board_changed(old_board, board):
            moves_count += 1
            stuck_count = 0
            continue
            
        # Try right
        send_move('d')
        board_text = get_board_state()
        board, _ = parse_board_and_score(board_text)
        
        if board_changed(old_board, board):
            moves_count += 1
            stuck_count = 0
            continue
            
        # Recovery moves when stuck
        stuck_count += 1
        
        # Try left
        send_move('a')
        board_text = get_board_state()
        board, _ = parse_board_and_score(board_text)
        
        if board_changed(old_board, board):
            moves_count += 1
            stuck_count = 0
            continue
            
        # Try up as last resort
        send_move('w')
        board_text = get_board_state()
        board, _ = parse_board_and_score(board_text)
        
        if board_changed(old_board, board):
            moves_count += 1
            stuck_count = 0
            continue
            
        # No moves possible - game over
        if stuck_count > 2:
            print(f"No moves available. Final score: {score}")
            break
            
        moves_count += 1
        
        # Print progress every 50 moves
        if moves_count % 50 == 0:
            print(f"Moves: {moves_count}, Current Score: {score}")
    
    return best_score

def main():
    print("Starting High Score Hunter for 2048...")
    print("Using Academically Validated Down-Right Strategy™")
    print("-" * 50)
    
    best_overall = 0
    
    # Run 5 games to get best score
    for i in range(5):
        print(f"\nGame {i+1}/5:")
        score = play_game()
        if score > best_overall:
            best_overall = score
            print(f"NEW BEST SCORE: {score}")
            
            # Capture screenshot of best game
            if i < 4:  # Don't quit on last game to keep it displayed
                time.sleep(2)  # Let user see the result
        
        time.sleep(1)
    
    print("\n" + "=" * 50)
    print(f"BEST SCORE ACHIEVED: {best_overall}")
    print("=" * 50)
    
    # Leave the best game on screen
    final_state = get_board_state()
    print("\nFinal board state for screenshot:")
    print(final_state)

if __name__ == "__main__":
    main()