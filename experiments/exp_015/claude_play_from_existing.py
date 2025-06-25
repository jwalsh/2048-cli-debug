#!/usr/bin/env python3
"""
Claude analyzes the existing board state and provides strategic moves
"""

# Based on the board we saw with score 332:
# |    4 |    2 |    4 |    2 |
# |    2 |   16 |    8 |    4 |
# |    4 |   32 |    4 |    2 |
# |      |    8 |   32 |    8 |

print("🧠 CLAUDE STRATEGIC ANALYSIS")
print("="*50)
print("\nCurrent Board (Score: 332):")
print("-" * 29)
print("|    4 |    2 |    4 |    2 |")
print("|    2 |   16 |    8 |    4 |")  
print("|    4 |   32 |    4 |    2 |")
print("|      |    8 |   32 |    8 |")
print("-" * 29)

print("\n📊 Board Analysis:")
print("- Two 32 tiles (not in corners!)")
print("- Only 1 empty cell (bottom-left)")
print("- Multiple merge opportunities")
print("- Board is scattered, needs consolidation")

print("\n🎯 Strategic Plan:")
print("1. IMMEDIATE: Merge the 8-8 pair in bottom row")
print("2. Work to align the two 32s")
print("3. Clear small tiles to create space")
print("4. Build toward 64+ tiles")

print("\n🎮 Move Sequence:")
moves = [
    ("RIGHT", "Merge bottom 8s → creates 16"),
    ("DOWN", "Drop tiles to fill empty spaces"),
    ("LEFT", "Shift tiles left, prepare for merges"),
    ("DOWN", "Consolidate downward"),
    ("RIGHT", "Try to align 32s horizontally"),
    ("DOWN", "Keep largest tiles at bottom"),
    ("LEFT", "Create space and merge opportunities"),
    ("DOWN", "Continue consolidation"),
    ("RIGHT", "Build rightward"),
    ("DOWN", "Final consolidation")
]

print("\nRecommended moves in order:")
for i, (direction, reason) in enumerate(moves, 1):
    print(f"{i}. {direction} - {reason}")

print("\n💡 Key Insights:")
print("- The 32s must be merged to progress")
print("- Empty space is critical - don't waste it")
print("- Focus on bottom-right corner strategy")
print("- Merge small tiles opportunistically")

print("\n🎯 Target: Beat 1708!")
print("Current: 332 | Need: 1376 more points")
print("\nTo beat 1708, we need at least a 256 tile!")

# Now let me create the actual commands to send
print("\n📝 Command sequence for game:")
cmd_map = {'DOWN': 's', 'RIGHT': 'd', 'LEFT': 'a', 'UP': 'w'}
cmd_sequence = ''.join(cmd_map[move[0]] for move in moves)
print(f"Send these keys: {cmd_sequence}")
print("\nThen continue with adaptive strategy based on board state.")