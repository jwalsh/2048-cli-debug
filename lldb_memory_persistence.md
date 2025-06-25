# LLDB Memory Persistence: Save/Load Game State

## Core Dump Approach (Full Process Snapshot)

### Save Complete Process State
```lldb
# Save full core dump (entire process memory)
process save-core --style full game_state_full.core

# Save only modified memory (more efficient)
process save-core --style modified-memory game_state_modified.core

# Save just the stack
process save-core --style stack game_state_stack.core
```

### Restore from Core Dump
```bash
# Load the core file in LLDB
lldb -c game_state_full.core ./2048-debug

# The process will be restored to exact state
# All memory, registers, and execution point preserved
```

## Targeted Memory Dump (Game State Only)

### Method 1: Binary Memory Dump
```lldb
# Dump the game state structure
memory read --outfile game_state.bin --binary --count 200 g

# Dump just the grid (16 integers = 64 bytes)
memory read --outfile grid.bin --binary --count 64 g->grid_data_ptr

# Dump with specific format
memory read --outfile grid.txt --count 16 --format "int32_t[]" g->grid_data_ptr
```

### Method 2: Python Scripting for Pickle-like Save
```python
# save_game_state.py - LLDB Python script
import lldb
import pickle
import struct

def save_game_state(debugger, command, result, internal_dict):
    target = debugger.GetSelectedTarget()
    process = target.GetProcess()
    thread = process.GetSelectedThread()
    frame = thread.GetSelectedFrame()
    
    # Get game state pointer
    g = frame.FindVariable("g")
    
    # Extract all relevant data
    game_data = {
        'score': g.GetChildMemberWithName('score').GetValueAsSigned(),
        'score_high': g.GetChildMemberWithName('score_high').GetValueAsSigned(),
        'gridsize': g.GetChildMemberWithName('gridsize').GetValueAsSigned(),
        'grid': []
    }
    
    # Read grid data
    grid_ptr = g.GetChildMemberWithName('grid_data_ptr').GetValueAsUnsigned()
    error = lldb.SBError()
    
    for i in range(16):
        addr = grid_ptr + (i * 4)
        data = process.ReadMemory(addr, 4, error)
        value = struct.unpack('<I', data)[0]
        game_data['grid'].append(value)
    
    # Save to pickle file
    with open('game_state.pickle', 'wb') as f:
        pickle.dump(game_data, f)
    
    print(f"Game state saved! Score: {game_data['score']}")

# Register command
def __lldb_init_module(debugger, internal_dict):
    debugger.HandleCommand('command script add -f save_game_state.save_game_state save_game')
```

### Method 3: Memory Checkpoint/Restore
```lldb
# Create a memory checkpoint (macOS specific)
process save-checkpoint checkpoint1

# Continue playing...
# Later, restore to checkpoint
process restore-checkpoint checkpoint1
```

## Manual Memory Restoration

### Write Memory Back
```lldb
# Restore grid from binary file
memory write g->grid_data_ptr --infile grid.bin

# Write individual values
memory write g->score 1234
memory write g->grid_data_ptr[0] 0x00000001

# Write multiple values at once
memory write g->grid_data_ptr '0 0 1 2 0 1 2 3 1 2 3 4 2 3 4 5'
```

## Complete Save/Load Implementation

### Save Script
```bash
#!/bin/bash
# save_2048_state.sh

# Get process ID
PID=$(pgrep 2048-debug)

# Attach LLDB and save state
lldb -p $PID <<EOF
# Save core
process save-core --style modified-memory state_$(date +%s).core

# Save specific memory regions
memory read --outfile grid_$(date +%s).bin --binary --count 64 g->grid_data_ptr
memory read --outfile gamestate_$(date +%s).bin --binary --count 100 g

# Print state for verification
print g->score
print g->grid[0][0]

detach
quit
EOF
```

### Load Script
```bash
#!/bin/bash
# load_2048_state.sh

# Start new game with restored state
lldb ./2048-debug <<EOF
# Set breakpoint after initialization
breakpoint set -n gamestate_new_block
run

# Restore memory from file
memory write g->grid_data_ptr --infile grid_saved.bin
memory write g->score 376

# Clear breakpoint and continue
breakpoint delete 1
continue
EOF
```

## Advanced: Process Migration

### Snapshot Running Game
```bash
# On macOS, create process snapshot
sudo dtrace -n 'BEGIN { stop(); }' -p $(pgrep 2048)
lldb -p $(pgrep 2048)
process save-core full_snapshot.core
detach
```

### Restore on Different Machine
```bash
# Copy core file and binary to new machine
scp full_snapshot.core 2048-debug user@other-machine:

# On other machine
lldb -c full_snapshot.core ./2048-debug
# Process restored with exact state!
```

## Practical Example: Quick Save/Load

### Quick Save Current Game
```lldb
# In active LLDB session
memory read --outfile quicksave.bin --binary --count 200 g
print "Game saved!"
```

### Quick Load
```lldb
# Restore from quicksave
memory write g --infile quicksave.bin
# Refresh display
continue
```

## Limitations & Considerations

1. **File Descriptors**: Network connections, file handles won't persist
2. **ASLR**: Address Space Layout Randomization may affect restoration
3. **System Resources**: PIDs, thread IDs will differ
4. **External State**: Terminal state, random seed may not match

## Creative Uses

1. **Save Scumming**: Save before risky moves, restore if failed
2. **State Sharing**: Share interesting board positions
3. **Replay System**: Save state at each move for perfect replay
4. **AI Training**: Generate thousands of board states for analysis

The answer is YES - LLDB can absolutely dump and restore memory like Python's pickle, with even more power since it can snapshot the entire process state!