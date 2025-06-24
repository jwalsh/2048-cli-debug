#!/usr/bin/env python3
"""LLDB script to play 2048 intelligently by reading terminal state"""

import lldb
import re
import time
import subprocess
import os
from datetime import datetime

# Global variables
move_count = 0
screenshot_dir = f"screenshots/game_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
os.makedirs(screenshot_dir, exist_ok=True)

def extract_board_from_terminal(debugger):
    """Extract the current board state by reading from terminal buffer"""
    # Get the process
    target = debugger.GetSelectedTarget()
    process = target.GetProcess()
    
    if not process:
        return None, None
    
    # Try to read the terminal output by examining stdout buffer
    # This is the hard part - we need to capture what's displayed
    
    # One approach: set a breakpoint after printf/write calls
    # and examine the buffer that was written
    
    board = [[0 for _ in range(4)] for _ in range(4)]
    score = 0
    
    # Read memory where the board is stored
    board_var = target.FindGlobalVariables("board", 1)
    if board_var:
        board_array = board_var[0]
        # The board is typically a 1D array of 16 integers
        for i in range(16):
            cell = board_array.GetChildAtIndex(i)
            if cell:
                value = cell.GetValueAsUnsigned()
                board[i // 4][i % 4] = value
    
    # Get the score
    score_var = target.FindGlobalVariables("score", 1)
    if score_var:
        score = score_var[0].GetValueAsUnsigned()
    
    return board, score

def analyze_board(board):
    """Analyze the board and determine the best move"""
    if not board:
        return 's'  # Default to down
    
    # Calculate scores for each possible move
    moves = ['w', 's', 'a', 'd']  # up, down, left, right
    move_scores = {}
    
    for move in moves:
        # Simulate the move
        simulated_board = simulate_move(board, move)
        if simulated_board != board:  # Valid move
            score = evaluate_position(simulated_board)
            move_scores[move] = score
    
    if not move_scores:
        return 's'  # No valid moves
    
    # Choose the move with the highest score
    best_move = max(move_scores, key=move_scores.get)
    return best_move

def simulate_move(board, direction):
    """Simulate a move and return the resulting board"""
    # Create a copy of the board
    new_board = [row[:] for row in board]
    
    if direction == 'a':  # left
        for row in new_board:
            compress_line(row)
    elif direction == 'd':  # right
        for row in new_board:
            row.reverse()
            compress_line(row)
            row.reverse()
    elif direction == 'w':  # up
        for col in range(4):
            line = [new_board[row][col] for row in range(4)]
            compress_line(line)
            for row in range(4):
                new_board[row][col] = line[row]
    elif direction == 's':  # down
        for col in range(4):
            line = [new_board[row][col] for row in range(3, -1, -1)]
            compress_line(line)
            for row in range(4):
                new_board[3-row][col] = line[row]
    
    return new_board

def compress_line(line):
    """Compress a line according to 2048 rules"""
    # Remove zeros
    non_zero = [x for x in line if x != 0]
    
    # Merge adjacent equal tiles
    i = 0
    while i < len(non_zero) - 1:
        if non_zero[i] == non_zero[i + 1]:
            non_zero[i] *= 2
            non_zero.pop(i + 1)
        i += 1
    
    # Pad with zeros
    while len(non_zero) < 4:
        non_zero.append(0)
    
    # Update the line
    for i in range(4):
        line[i] = non_zero[i]

def evaluate_position(board):
    """Evaluate how good a board position is"""
    score = 0
    
    # Prefer keeping the highest tile in a corner
    max_tile = max(max(row) for row in board)
    corner_positions = [(0, 0), (0, 3), (3, 0), (3, 3)]
    for r, c in corner_positions:
        if board[r][c] == max_tile:
            score += max_tile * 100
            break
    
    # Prefer monotonic rows and columns
    for row in board:
        if all(row[i] >= row[i+1] for i in range(3)):
            score += 50
        elif all(row[i] <= row[i+1] for i in range(3)):
            score += 50
    
    for col in range(4):
        column = [board[row][col] for row in range(4)]
        if all(column[i] >= column[i+1] for i in range(3)):
            score += 50
        elif all(column[i] <= column[i+1] for i in range(3)):
            score += 50
    
    # Prefer empty cells
    empty_cells = sum(1 for row in board for cell in row if cell == 0)
    score += empty_cells * 20
    
    # Penalize having large tiles scattered
    large_tiles = [(r, c) for r in range(4) for c in range(4) if board[r][c] >= 128]
    if len(large_tiles) > 1:
        # Calculate Manhattan distance between large tiles
        total_distance = 0
        for i in range(len(large_tiles)):
            for j in range(i + 1, len(large_tiles)):
                r1, c1 = large_tiles[i]
                r2, c2 = large_tiles[j]
                total_distance += abs(r1 - r2) + abs(c1 - c2)
        score -= total_distance * 10
    
    return score

def take_screenshot(move_num):
    """Take a screenshot of the terminal"""
    filename = f"{screenshot_dir}/move_{move_num:04d}.png"
    # Use screencapture to capture the Terminal window
    subprocess.run(["osascript", "-e", 'tell application "Terminal" to activate'])
    time.sleep(0.1)
    subprocess.run(["screencapture", "-x", "-R", "0,0,800,600", filename])
    print(f"Screenshot saved: {filename}")

def play_move(debugger, command, result, internal_dict):
    """LLDB command to play a single move"""
    global move_count
    
    # Extract board state
    board, score = extract_board_from_terminal(debugger)
    
    if board:
        print(f"\nMove {move_count} - Score: {score}")
        print_board(board)
        
        # Take screenshot
        take_screenshot(move_count)
        
        # Determine best move
        best_move = analyze_board(board)
        move_names = {'w': 'UP', 's': 'DOWN', 'a': 'LEFT', 'd': 'RIGHT'}
        print(f"Best move: {move_names.get(best_move, best_move)}")
        
        # Send the move to the process
        process = debugger.GetSelectedTarget().GetProcess()
        if process:
            # Write to stdin
            process.PutSTDIN(best_move.encode())
            
        move_count += 1
        
        # Check if we beat the high score
        if score > 932:
            print(f"🎉 NEW HIGH SCORE: {score}!")
    else:
        print("Could not read board state")

def print_board(board):
    """Print the board in a nice format"""
    print("-" * 25)
    for row in board:
        print("|", end="")
        for cell in row:
            if cell == 0:
                print("     |", end="")
            else:
                print(f"{cell:5}|", end="")
        print("\n" + "-" * 25)

def auto_play(debugger, command, result, internal_dict):
    """LLDB command to play automatically"""
    print(f"Starting auto-play. Screenshots will be saved to: {screenshot_dir}")
    
    # Set breakpoints at key locations
    target = debugger.GetSelectedTarget()
    
    # Breakpoint after board is printed
    print_bp = target.BreakpointCreateByName("print_board")
    
    # Breakpoint at game loop
    loop_bp = target.BreakpointCreateByName("game_loop")
    
    # Add commands to breakpoints
    if print_bp.GetNumLocations() > 0:
        print_bp.SetScriptCallbackFunction("play_with_lldb.play_move")
        print("Set breakpoint on print_board")
    
    # Continue execution
    process = target.GetProcess()
    if process:
        process.Continue()
    else:
        # Launch the process
        error = lldb.SBError()
        process = target.Launch(
            debugger.GetListener(),
            None,  # argv
            None,  # envp
            "/dev/stdin",  # stdin_path
            "/dev/stdout",  # stdout_path
            "/dev/stderr",  # stderr_path
            None,  # working directory
            0,     # launch flags
            False, # stop at entry
            error
        )
        
        if error.Success():
            print("Launched 2048 successfully")
        else:
            print(f"Failed to launch: {error}")

def __lldb_init_module(debugger, internal_dict):
    """Initialize the LLDB commands"""
    debugger.HandleCommand('command script add -f play_with_lldb.play_move play_move')
    debugger.HandleCommand('command script add -f play_with_lldb.auto_play auto_play')
    print("2048 LLDB commands loaded. Use 'auto_play' to start playing.")