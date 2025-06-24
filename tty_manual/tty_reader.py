#!/usr/bin/env python3
"""
TTY Reader for 2048 - Captures and parses game output
Part of Issue #5: TTY-based 2048 controller implementation
"""

import os
import pty
import select
import subprocess
import sys
import time
import re
import json
from datetime import datetime

class TTYReader:
    """Reads 2048 game output from a pseudo-terminal"""
    
    def __init__(self, game_binary="2048-cli-0.9.1/2048"):
        self.game_binary = game_binary
        self.master_fd = None
        self.slave_fd = None
        self.process = None
        self.current_board = None
        self.current_score = 0
        self.high_score = 0
        self.output_buffer = ""
        
    def start_game(self):
        """Start 2048 in a pseudo-terminal"""
        # Create pseudo-terminal
        self.master_fd, self.slave_fd = pty.openpty()
        
        # Start game process
        self.process = subprocess.Popen(
            [self.game_binary],
            stdin=self.slave_fd,
            stdout=self.slave_fd,
            stderr=self.slave_fd,
            close_fds=True
        )
        
        # Close slave in parent
        os.close(self.slave_fd)
        
        # Make master non-blocking
        import fcntl
        flags = fcntl.fcntl(self.master_fd, fcntl.F_GETFL)
        fcntl.fcntl(self.master_fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)
        
        print(f"Started game with PID {self.process.pid}")
        
    def read_output(self, timeout=0.1):
        """Read available output from the game"""
        try:
            r, _, _ = select.select([self.master_fd], [], [], timeout)
            if r:
                data = os.read(self.master_fd, 4096)
                if data:
                    decoded = data.decode('utf-8', errors='ignore')
                    self.output_buffer += decoded
                    return decoded
        except OSError:
            pass
        return ""
    
    def send_move(self, move):
        """Send a move to the game (w/a/s/d)"""
        if self.master_fd and move in ['w', 'a', 's', 'd']:
            os.write(self.master_fd, move.encode())
            return True
        return False
    
    def parse_board_state(self, output=None):
        """Parse the board state from terminal output"""
        if output is None:
            output = self.output_buffer
            
        # Look for the board pattern
        # Score: XXX
        #    Hi: XXX
        # -----------------------------
        # |    2 |      |    4 |    8 |
        # |      |      |      |    8 |
        # |      |      |      |      |
        # |      |      |      |      |
        # -----------------------------
        
        # Extract score
        score_match = re.search(r'Score:\s*(\d+)', output)
        if score_match:
            self.current_score = int(score_match.group(1))
            
        # Extract high score
        hi_match = re.search(r'Hi:\s*(\d+)', output)
        if hi_match:
            self.high_score = int(hi_match.group(1))
            
        # Extract board
        board_lines = []
        lines = output.split('\n')
        
        in_board = False
        for line in lines:
            if '----' in line:
                if not in_board:
                    in_board = True
                    board_lines = []
                else:
                    # End of board
                    break
            elif in_board and '|' in line:
                board_lines.append(line)
        
        if len(board_lines) == 4:
            board = []
            for line in board_lines:
                # Parse cells from line like: |    2 |      |    4 |    8 |
                cells = line.split('|')[1:-1]  # Remove first and last empty
                row = []
                for cell in cells:
                    cell = cell.strip()
                    if cell:
                        row.append(int(cell))
                    else:
                        row.append(0)
                board.append(row)
            
            self.current_board = board
            return True
            
        return False
    
    def get_board_dict(self):
        """Get current board state as a dictionary"""
        return {
            'board': self.current_board,
            'score': self.current_score,
            'high_score': self.high_score,
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }
    
    def save_board_snapshot(self, filepath):
        """Save current board state to file"""
        if self.current_board:
            with open(filepath, 'w') as f:
                f.write(f"Score: {self.current_score}\n")
                f.write(f"Hi: {self.high_score}\n")
                f.write("-" * 29 + "\n")
                
                for row in self.current_board:
                    f.write("|")
                    for cell in row:
                        if cell == 0:
                            f.write("      |")
                        else:
                            f.write(f"{cell:5} |")
                    f.write("\n")
                    
                f.write("-" * 29 + "\n")
                
    def cleanup(self):
        """Clean up resources"""
        if self.master_fd:
            os.close(self.master_fd)
        if self.process:
            self.process.terminate()
            self.process.wait()


# Test function
if __name__ == "__main__":
    print("Testing TTY Reader...")
    
    reader = TTYReader()
    reader.start_game()
    
    # Wait for initial board
    time.sleep(0.5)
    output = reader.read_output()
    print("Initial output length:", len(output))
    
    if reader.parse_board_state(output):
        print(f"Score: {reader.current_score}")
        print(f"High Score: {reader.high_score}")
        print("Board:")
        for row in reader.current_board:
            print(row)
            
        # Save snapshot
        reader.save_board_snapshot("test_board.txt")
        print("Saved board to test_board.txt")
    else:
        print("Failed to parse board")
        print("Raw output:")
        print(output[:500])
    
    # Test a move
    print("\nSending move: down")
    reader.send_move('s')
    time.sleep(0.5)
    
    output = reader.read_output()
    if reader.parse_board_state():
        print(f"New score: {reader.current_score}")
    
    reader.cleanup()
    print("Test complete!")