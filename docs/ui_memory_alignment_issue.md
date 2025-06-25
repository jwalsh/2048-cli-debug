# UI/Memory Alignment Investigation

## The Problem: Board Appears "Flipped"

User observation: When spamming down-right, the board representation doesn't match expected behavior.

### Expected Down-Right Spam Pattern
```
|      |      |      |    2 |
|      |      |      |    4 |
|      |      |    2 |    8 |
|      |    2 |    4 |   64 |  <-- Heavy tiles in bottom-right
```

### What We're Seeing from Memory
```
|    8 |    0 |    0 |    0 |
|    2 |    8 |    2 |    0 |
|    8 |   16 |    0 |    0 |
|    2 |    8 |   64 |    4 |
```
Heavy tiles spread across bottom row and left side - not typical for down-right spam!

## Hypothesis: We're Interpreting the Grid Wrong

### Current Decoding (Column-Major)
```python
idx = col * 4 + row  # We assume column-major storage
```

### Alternative 1: Row-Major
```python
idx = row * 4 + col  # Standard C array layout
```

### Alternative 2: Transposed
The visual board might be transposed from memory representation.

### Alternative 3: Different Coordinate System
- Memory: (0,0) might be bottom-left
- Display: (0,0) might be top-left

## Testing Different Interpretations

Let me decode the same memory with different assumptions:

Memory values: [3,1,3,1, 0,3,4,3, 0,1,0,6, 0,0,0,2]

### Row-Major Interpretation
```python
# If memory is row-major (standard C arrays)
for row in range(4):
    for col in range(4):
        idx = row * 4 + col
        # Row 0: [3,1,3,1] = [8,2,8,2]
        # Row 1: [0,3,4,3] = [0,8,16,8]
        # Row 2: [0,1,0,6] = [0,2,0,64]
        # Row 3: [0,0,0,2] = [0,0,0,4]
```

This gives:
```
|    8 |    2 |    8 |    2 |
|    0 |    8 |   16 |    8 |
|    0 |    2 |    0 |   64 |
|    0 |    0 |    0 |    4 |
```

This looks MORE like a down-right spam result! The 64 is in position (2,3) moving toward bottom-right.

## Key Insight
We've been using column-major indexing when the game likely uses row-major (standard C array layout).

## Impact on Our Analysis
- All our board interpretations may be transposed
- Save/restore might work but display wrong
- Our "stuck" boards might not actually be stuck
- Strategic decisions based on wrong board view

## Next Steps
1. Verify actual UI display vs memory
2. Fix decoding in all analysis scripts
3. Re-analyze saved game states
4. Update documentation with correct interpretation

## Testing Chaos Documentation

### Attempt 1: Wrong PID Attachment
- Multiple 2048 processes running from previous sessions
- Attached to zombie process (PID 7218) instead of active game
- Lesson: Always verify correct PID with `ps aux | grep 2048`

### Attempt 2: tmux Window Confusion
- Created game in one window, LLDB in another
- Lost track of which window had which process
- Commands sent to wrong panes
- Lesson: Use clear naming for tmux sessions/windows

### Attempt 3: Over-eager Automation
```bash
# Tried to send 100 moves as "sd" repeated 50 times
for i in {1..50}; do
    tmux send-keys -t clean2048 "sd"
done
# Result: Sent "sdsdsdsd..." as one long string!
```
Lesson: Need delays between moves or individual key sends

### The Right Way
1. Start fresh with clear session names
2. Verify process PIDs before attaching
3. Use proper delays between moves
4. Check UI matches memory interpretation
5. Document everything (including failures!)

As the user said: "lol, such is testing :D"