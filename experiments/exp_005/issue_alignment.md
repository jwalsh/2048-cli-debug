# Memory representation vs UI display alignment issues

## Problem
We're seeing potential misalignment between:
1. Raw memory values from LLDB
2. Python decoded board representation  
3. Actual UI display shown to user

## Observed Issue
- Memory shows grid values: [3,1,3,1, 0,3,4,3, 0,1,0,6, 0,0,0,2]
- Python decodes this as:
  ```
  |    8 |    0 |    0 |    0 |
  |    2 |    8 |    2 |    0 |
  |    8 |   16 |    0 |    0 |
  |    2 |    8 |   64 |    4 |
  ```
- But we cannot see the actual UI to confirm this matches what the user sees

## Root Causes
1. Column-major vs row-major storage assumptions
2. LLDB attached process may not be updating terminal display
3. Breakpoints may be preventing UI refresh
4. tmux capture may be missing game output

## Testing Applied
- Direct memory read from grid_data_ptr
- Python decoding with column-major indexing
- Attempted to trigger UI update with moves
- Process continuation to allow display refresh

## Impact
Without UI verification, we cannot trust that our memory interpretation is correct. This affects:
- Save/restore functionality
- Board state analysis
- AI decision making
- Game state sharing