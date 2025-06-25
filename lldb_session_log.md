# LLDB Manual Session Log
## Date: 2025-06-25

### Initial Setup
- Built with: `clang -g -O0` for debug symbols
- Breakpoints set: gamestate_tick, gamestate_new_block
- Disabled new_block breakpoint after initialization

### Key Discoveries
1. **Grid Memory Layout**: 16 integers (4x4 grid) stored linearly
2. **Value Encoding**: Powers of 2 (1=2, 2=4, 3=8, etc.)
3. **Direction Enum**: 1=down, 2=left, 3=right, 4=up
4. **Game State Structure**:
   - grid_data_ptr: Raw memory for grid
   - gridsize: 16 (for 4x4)
   - score: Current score
   - blocks_in_play: Number of non-zero tiles

### Memory Inspection Commands Used
```lldb
print *g                                    # Full game state
print g->score                              # Current score
memory read -f d -c 16 g->grid_data_ptr    # Read entire grid
print d                                     # Direction of move
```

### Down-Right Spam Phase (20 moves)
Move 1: DOWN (s) - Initial board had 2,2,4
Moves 2-20: Alternating RIGHT and DOWN
Result after spam: Score 76, highest tile 16

### Strategic Manual Phase (5 moves)
Current board state:
```
|      |      |      |      |
|      |      |    2 |    4 |
|      |    2 |    4 |    8 |
|      |    2 |    8 |   16 |
```

Memory layout discovered:
- Grid stored as 16 integers row-by-row
- Values are powers of 2: 1=2, 2=4, 3=8, 4=16

**Move 21 (Strategic 1): DOWN**
- Reasoning: Merge the three 2s in column 2 to create a 4
- Result: Success, score 80

**Move 22 (Strategic 2): RIGHT**
- Reasoning: Continue building corner pattern
- Result: Minor reorganization

**Move 23 (Strategic 3): DOWN**
- Reasoning: Attempt to merge 4s
- Result: No valid moves

**Move 24 (Strategic 4): RIGHT**
- Reasoning: Try to continue pattern
- Result: Board stuck

**Move 25 (Strategic 5): LEFT**
- Reasoning: Create movement opportunities
- Result: Board opened up, maintained 16 as highest tile

### Final Board State
```
|    4 |    2 |      |      |
|    2 |    4 |    2 |      |
|    4 |    8 |      |      |
|    2 |    4 |    8 |   16 |
```
Score: 80

### Key LLDB Learning Outcomes
1. Successfully attached debugger to running game
2. Set breakpoints on game logic functions
3. Inspected memory layout of grid (row-major order)
4. Discovered internal value encoding (powers of 2)
5. Monitored game state changes in real-time
6. Used memory inspection to understand data structures

This manual LLDB session provides the foundation for automating game control via debugger in Phase 2.