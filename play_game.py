#!/usr/bin/env python3
"""Play 2048 with intelligent moves and screenshot capture"""

import subprocess
import time
import os
import sys
import select
import termios
import tty
from datetime import datetime
import pty
import re

class Game2048Player:
    def __init__(self):
        self.screenshot_dir = f"screenshots/game_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(self.screenshot_dir, exist_ok=True)
        self.move_count = 0
        self.current_score = 0
        self.high_score_target = 932
        self.game_over = False
        
    def take_screenshot(self):
        """Take a screenshot of the game"""
        filename = f"{self.screenshot_dir}/move_{self.move_count:04d}.png"
        # Focus on Terminal app
        subprocess.run(["osascript", "-e", 'tell application "Terminal" to activate'])
        time.sleep(0.2)
        # Take screenshot
        subprocess.run(["screencapture", "-x", filename])
        print(f"Screenshot saved: {filename}")
        
    def parse_board_output(self, output):
        """Parse the game output to extract board state and score"""
        lines = output.split('\n')
        
        # Look for score
        for line in lines:
            if "Score:" in line:
                match = re.search(r'Score:\s*(\d+)', line)
                if match:
                    self.current_score = int(match.group(1))
                    
        # Check for game over
        if "Game over" in output:
            self.game_over = True
            
    def get_smart_move(self):
        """Determine the next move using a smart strategy"""
        # Strategy: Keep high tiles in corners, prefer down and right
        # This creates a "snake" pattern that tends to produce high scores
        
        import random
        
        # Weighted move selection
        moves = ['s', 'd', 'a', 'w']  # down, right, left, up
        weights = [0.4, 0.3, 0.2, 0.1]  # Prefer down and right
        
        return random.choices(moves, weights=weights)[0]
        
    def play(self):
        """Main game loop"""
        print(f"Starting 2048 game. Target score: {self.high_score_target}")
        print(f"Screenshots will be saved to: {self.screenshot_dir}")
        
        # Build the game
        print("Building game...")
        subprocess.run(["make", "-C", "2048-cli-0.9.1", "clean"], capture_output=True)
        subprocess.run(["make", "-C", "2048-cli-0.9.1", "2048"], capture_output=True)
        
        # Start the game using pty for better interaction
        master, slave = pty.openpty()
        
        process = subprocess.Popen(
            ["2048-cli-0.9.1/2048"],
            stdin=slave,
            stdout=slave,
            stderr=slave,
            close_fds=True
        )
        
        os.close(slave)
        
        # Make the master fd non-blocking
        import fcntl
        flags = fcntl.fcntl(master, fcntl.F_GETFL)
        fcntl.fcntl(master, fcntl.F_SETFL, flags | os.O_NONBLOCK)
        
        # Initial screenshot
        time.sleep(0.5)
        self.take_screenshot()
        
        # Game loop
        output_buffer = ""
        last_move_time = time.time()
        
        while not self.game_over and self.move_count < 2000:
            try:
                # Read any available output
                try:
                    chunk = os.read(master, 1024).decode('utf-8', errors='ignore')
                    output_buffer += chunk
                    
                    # Process complete screens
                    if '\n' in output_buffer:
                        self.parse_board_output(output_buffer)
                        sys.stdout.write(chunk)
                        sys.stdout.flush()
                        output_buffer = ""
                        
                except OSError:
                    pass
                
                # Make a move every 0.5 seconds
                if time.time() - last_move_time > 0.5:
                    self.move_count += 1
                    move = self.get_smart_move()
                    move_name = {'s': 'down', 'd': 'right', 'a': 'left', 'w': 'up'}[move]
                    
                    print(f"\nMove {self.move_count}: {move_name} (Score: {self.current_score})")
                    
                    # Send move
                    os.write(master, move.encode())
                    
                    # Wait for board update
                    time.sleep(0.3)
                    
                    # Take screenshot
                    self.take_screenshot()
                    
                    # Check high score
                    if self.current_score > self.high_score_target:
                        print(f"\n🎉 NEW HIGH SCORE: {self.current_score}!")
                    
                    last_move_time = time.time()
                
                # Check if process is still running
                if process.poll() is not None:
                    break
                    
            except KeyboardInterrupt:
                print("\nGame interrupted by user")
                break
        
        # Cleanup
        process.terminate()
        os.close(master)
        
        print(f"\nGame ended!")
        print(f"Final score: {self.current_score}")
        print(f"Total moves: {self.move_count}")
        print(f"Screenshots saved to: {self.screenshot_dir}")
        
        # Create a summary file
        with open(f"{self.screenshot_dir}/summary.txt", 'w') as f:
            f.write(f"2048 Game Summary\n")
            f.write(f"================\n")
            f.write(f"Date: {datetime.now()}\n")
            f.write(f"Final Score: {self.current_score}\n")
            f.write(f"High Score Target: {self.high_score_target}\n")
            f.write(f"Total Moves: {self.move_count}\n")
            f.write(f"High Score Beaten: {'Yes' if self.current_score > self.high_score_target else 'No'}\n")

if __name__ == "__main__":
    player = Game2048Player()
    player.play()