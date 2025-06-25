# 2048 LLDB Debugging: Experimental Journal

## Day 1: Initial Hypotheses

### Hypothesis 1: "We can control 2048 through TTY without modifying source"
**Method**: Python TTY reader, expect scripts, tmux automation
**Result**: ✅ Confirmed - Multiple approaches work
**Learning**: tmux provides most reliable interaction

### Hypothesis 2: "Down-right spam is optimal strategy"
**Method**: Implemented weighted random (40% down, 30% right, 20% left, 10% up)
**Result**: ✅ Achieved high score 1708
**Learning**: Academic heuristic validated

## Day 2: Memory Inspection

### Hypothesis 3: "LLDB can read game state from memory"
**Method**: Attach debugger, set breakpoints, inspect gamestate struct
**Result**: ✅ Successfully read grid, score, and game state
**Learning**: Memory layout discovered, internal value encoding (powers of 2)

### Hypothesis 4: "Grid is stored in row-major order"
**Method**: Memory inspection of grid_data_ptr
**Initial Result**: ❌ Board appeared "flipped" 
**Revised Hypothesis**: "Grid uses column-major storage"
**Second Result**: ❌ Still incorrect after down-right spam
**Final Discovery**: ✅ Grid IS row-major, our decoding was wrong!

## Day 3: State Persistence

### Hypothesis 5: "We can save/restore game state like Python pickle"
**Method**: LLDB memory dumps and core files
**Result**: ✅ Created binary dumps, core files successfully
**Challenge**: Restoring to live process proved complex

### Hypothesis 6: "Command concatenation is a timing issue"
**Observation**: "scontinue" errors when sending rapid commands
**Method**: Added delays between tmux send-keys
**Result**: ✅ 0.2-0.3s delays prevent concatenation

## Today's Experiments

### Hypothesis 7: "Multiple 2048 processes cause attachment confusion"
**Observation**: Attached to wrong PID, zombie processes
**Method**: Clean slate approach with process management
**Result**: ✅ Proper cleanup essential for reliable testing

### Hypothesis 8: "150 moves of down-right spam creates predictable pattern"
**Method**: Fresh game, automated spam, memory inspection
**Result**: ✅ Score 180, highest tile 32 in bottom-right
**Discovery**: Pattern confirmed as expected

### Hypothesis 9: "UI and Memory are perfectly aligned"
**Method**: Compare tmux capture (UI) with LLDB memory read
**Result**: ❌ MISMATCH FOUND!
**Observation**: 
- UI shows: Row 2 has 8 at position [2][3], Row 3 has 16 at position [3][2]
- Memory shows: Row 2 has 16 at position [2][3], Row 3 has 8 at position [3][2]
**Possible Causes**:
1. Race condition between debugger read and display update
2. UI rendering lag
3. Different coordinate systems
4. Memory caching issues

## Failed Experiments Log

1. **Shell Script Automation**: Timed out after 2 minutes
2. **Python PTY Module**: OSError [Errno 5] after ~100 moves  
3. **Direct Memory Write**: Board state restoration incomplete
4. **Rapid Command Sending**: Created "sdsdsdsd" concatenation

## Key Scientific Discoveries

1. **Memory Layout**: 16 integers, row-major, powers of 2 encoding
2. **Timing Constants**: 0.05s between moves, 0.2s between commands
3. **Process Management**: Must verify PIDs before attachment
4. **Board Interpretation**: Row-major, not column-major as initially assumed

## Reproducibility Notes

To reproduce our results:
```bash
# Clean environment
pkill -f 2048; tmux kill-server

# Start fresh
tmux new-session -d -s game2048 "./2048-debug"

# Spam pattern (verified working)
for i in {1..75}; do
    tmux send-keys -t game2048 "s"
    sleep 0.05
    tmux send-keys -t game2048 "d"
    sleep 0.05
done
```

## Open Questions

1. Can we restore from core dump to continue play?
2. Is the UI truly aligned with our memory interpretation?
3. What's the theoretical maximum score with down-right only?
4. Can we predict RNG for new tile placement?

## Next Experiments

1. Verify UI matches memory after 150 moves
2. Test core dump restoration workflow
3. Measure score progression rate
4. Document tile doubling patterns

---
*"In science, failure is just data" - Every debugging session ever*