#!/usr/bin/env python3
"""Automated 2048 gameplay with screenshot capture and LLDB integration"""

import subprocess
import time
import os
import re
from datetime import datetime

class Game2048Debugger:
    def __init__(self):
        self.move_count = 0
        self.screenshot_dir = f"screenshots/game_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(self.screenshot_dir, exist_ok=True)
        self.lldb_commands_file = "automated_play.lldb"
        self.current_score = 0
        self.high_score = 932
        
    def create_lldb_script(self):
        """Create LLDB script for automated gameplay"""
        script = """# Automated 2048 gameplay script
file 2048-cli-0.9.1/2048

# Set breakpoints
b game_loop
b print_board
b sleep_animation

# Commands to run when print_board is hit
breakpoint command add 2
continue
end

# Commands to run when sleep_animation is hit (skip animations)
breakpoint command add 3
thread return
continue
end

# Start the game
run

# Function to capture board state
script
import lldb
import os

def capture_board_state(debugger, move_num):
    # Get board array
    board = debugger.GetSelectedTarget().FindGlobalVariables("board", 1)[0]
    
    # Extract score
    score_var = debugger.GetSelectedTarget().FindGlobalVariables("score", 1)
    if score_var:
        score = score_var[0].GetValue()
    else:
        score = "0"
    
    # Save state to file
    state_file = f"screenshots/game_{datetime.now().strftime('%Y%m%d_%H%M%S')}/state_{move_num:04d}.txt"
    with open(state_file, 'w') as f:
        f.write(f"Move: {move_num}\\n")
        f.write(f"Score: {score}\\n")
        f.write("Board:\\n")
        
        # Read board values
        for i in range(4):
            row = []
            for j in range(4):
                val = board.GetChildAtIndex(i * 4 + j).GetValue()
                row.append(val if val else "0")
            f.write(" ".join(row) + "\\n")
    
    return int(score) if score else 0

def make_move(direction):
    # Send keystroke to the process
    process = lldb.debugger.GetSelectedTarget().GetProcess()
    if direction == 'up':
        process.PutSTDIN(b'w\\n')
    elif direction == 'down':
        process.PutSTDIN(b's\\n')
    elif direction == 'left':
        process.PutSTDIN(b'a\\n')
    elif direction == 'right':
        process.PutSTDIN(b'd\\n')
"""
        
        with open(self.lldb_commands_file, 'w') as f:
            f.write(script)
    
    def analyze_board_state(self, state_file):
        """Analyze current board state and determine best move"""
        with open(state_file, 'r') as f:
            lines = f.readlines()
        
        # Extract board values
        board = []
        for i in range(4, 8):  # Board lines are at indices 4-7
            row = [int(x) for x in lines[i].strip().split()]
            board.append(row)
        
        # Simple strategy: prefer moves that keep larger tiles in corners
        # and create merging opportunities
        scores = {'up': 0, 'down': 0, 'left': 0, 'right': 0}
        
        # Check each direction
        for direction in ['up', 'down', 'left', 'right']:
            test_board = [row[:] for row in board]  # Deep copy
            if self.simulate_move(test_board, direction):
                # Move is valid
                scores[direction] = self.evaluate_board(test_board)
        
        # Choose move with highest score
        best_move = max(scores, key=scores.get)
        return best_move if scores[best_move] > 0 else None
    
    def simulate_move(self, board, direction):
        """Simulate a move and return True if board changed"""
        original = [row[:] for row in board]
        
        if direction == 'left':
            for row in board:
                self.merge_line(row)
        elif direction == 'right':
            for row in board:
                row.reverse()
                self.merge_line(row)
                row.reverse()
        elif direction == 'up':
            for col in range(4):
                line = [board[row][col] for row in range(4)]
                self.merge_line(line)
                for row in range(4):
                    board[row][col] = line[row]
        elif direction == 'down':
            for col in range(4):
                line = [board[row][col] for row in range(3, -1, -1)]
                self.merge_line(line)
                for row in range(4):
                    board[3-row][col] = line[row]
        
        return board != original
    
    def merge_line(self, line):
        """Merge a line according to 2048 rules"""
        # Remove zeros
        non_zero = [x for x in line if x != 0]
        
        # Merge adjacent equal values
        merged = []
        i = 0
        while i < len(non_zero):
            if i + 1 < len(non_zero) and non_zero[i] == non_zero[i + 1]:
                merged.append(non_zero[i] * 2)
                i += 2
            else:
                merged.append(non_zero[i])
                i += 1
        
        # Fill with zeros
        while len(merged) < 4:
            merged.append(0)
        
        # Update line
        for i in range(4):
            line[i] = merged[i]
    
    def evaluate_board(self, board):
        """Evaluate board position (higher is better)"""
        score = 0
        
        # Prefer keeping highest tile in corner
        max_tile = max(max(row) for row in board)
        if board[0][0] == max_tile:
            score += max_tile * 10
        
        # Prefer monotonic rows/columns
        for row in board:
            if all(row[i] >= row[i+1] for i in range(3)) or \
               all(row[i] <= row[i+1] for i in range(3)):
                score += 100
        
        # Prefer empty spaces
        empty_count = sum(1 for row in board for val in row if val == 0)
        score += empty_count * 50
        
        # Penalize scattered high values
        high_values = [(i, j) for i in range(4) for j in range(4) if board[i][j] >= 64]
        if len(high_values) > 1:
            distances = []
            for i in range(len(high_values)):
                for j in range(i + 1, len(high_values)):
                    dist = abs(high_values[i][0] - high_values[j][0]) + \
                           abs(high_values[i][1] - high_values[j][1])
                    distances.append(dist)
            if distances:
                score -= sum(distances) * 10
        
        return score
    
    def play_game(self):
        """Main game loop"""
        print(f"Starting automated 2048 gameplay. Target high score: {self.high_score}")
        print(f"Screenshots will be saved to: {self.screenshot_dir}")
        
        # Create LLDB script
        self.create_lldb_script()
        
        # Build the game first
        print("Building game...")
        subprocess.run(["make", "-C", "2048-cli-0.9.1", "clean"], check=True)
        subprocess.run(["make", "-C", "2048-cli-0.9.1", "2048"], check=True)
        
        # Start LLDB process
        lldb_process = subprocess.Popen(
            ["lldb", "-s", self.lldb_commands_file],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Game loop
        while self.move_count < 1000:  # Safety limit
            self.move_count += 1
            
            # Capture current state
            state_file = f"{self.screenshot_dir}/state_{self.move_count:04d}.txt"
            
            # Wait for board to be printed
            time.sleep(0.1)
            
            # Capture screenshot using screencapture
            screenshot_file = f"{self.screenshot_dir}/move_{self.move_count:04d}.png"
            subprocess.run(["screencapture", "-x", screenshot_file])
            
            # Analyze board and determine next move
            if os.path.exists(state_file):
                next_move = self.analyze_board_state(state_file)
                
                if next_move:
                    print(f"Move {self.move_count}: {next_move} (Score: {self.current_score})")
                    
                    # Send move to game
                    move_key = {'up': 'w', 'down': 's', 'left': 'a', 'right': 'd'}[next_move]
                    lldb_process.stdin.write(f"expr (void)putchar('{move_key}')\n")
                    lldb_process.stdin.flush()
                    
                    # Check if we beat high score
                    if self.current_score > self.high_score:
                        print(f"NEW HIGH SCORE: {self.current_score}!")
                else:
                    print("Game Over!")
                    break
            
            # Small delay between moves
            time.sleep(0.5)
        
        # Cleanup
        lldb_process.terminate()
        print(f"Game ended. Final score: {self.current_score}")
        print(f"Screenshots saved to: {self.screenshot_dir}")

if __name__ == "__main__":
    game = Game2048Debugger()
    game.play_game()