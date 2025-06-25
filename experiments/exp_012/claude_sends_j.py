#!/usr/bin/env python3
"""
Claude sends 'j' command directly to the game
"""

import time
from tty_manual.tty_reader import TTYReader

reader = TTYReader()
print("Starting game...")
reader.start_game()
time.sleep(0.5)

# Read initial state
output = reader.read_output()
print("Initial output:")
print(output[-200:] if len(output) > 200 else output)

print("\nSending 'j' command...")
reader.send_move('j')
time.sleep(0.5)

# Read result
output = reader.read_output()
print("\nOutput after 'j':")
print(output[-200:] if len(output) > 200 else output)

reader.cleanup()