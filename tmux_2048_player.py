#!/usr/bin/env python3

import subprocess
import re
import time

def get_board_state():
    """Capture the current board state from tmux"""
    result = subprocess.run(['tmux', 'capture-pane', '-t', 'game2048', '-p'], 
                          capture_output=True, text=True)
    return result.stdout

def parse_board(board_text):
    """Parse the board state into a 4x4 matrix"""
    lines = board_text.strip().split('\n')
    board = []
    
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
    
    return board

def send_move(move):
    """Send a move to the game"""
    subprocess.run(['tmux', 'send-keys', '-t', 'game2048', move])
    time.sleep(0.1)  # Give game time to process

def main():
    # First spam some moves
    print("Spamming 100 down-right moves...")
    moves = "df" * 50
    subprocess.run(['tmux', 'send-keys', '-t', 'game2048', moves])
    time.sleep(1)
    
    # Read the board
    board_text = get_board_state()
    print("\nCurrent board state:")
    print(board_text)
    
    # Parse and analyze
    board = parse_board(board_text)
    if board:
        print("\nParsed board:")
        for row in board:
            print(row)
        
        # Simple strategy: if stuck, try left or up
        print("\nTrying strategic moves...")
        send_move('a')  # left
        time.sleep(0.2)
        send_move('w')  # up
        time.sleep(0.2)
        
        # Get new state
        new_board_text = get_board_state()
        print("\nNew board state:")
        print(new_board_text)

if __name__ == "__main__":
    main()