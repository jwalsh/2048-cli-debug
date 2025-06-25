#!/bin/bash
#!/bin/bash
# Reproduce the column-major discovery

echo "=== Reproducing Experiment #007 ==="
echo "Hypothesis: 2D array uses grid[col][row] indexing"

# 1. Clean environment
echo "Step 1: Cleaning environment..."
pkill -f 2048 2>/dev/null
tmux kill-server 2>/dev/null || true

# 2. Build debug version
echo "Step 2: Building debug binary..."
cd ../../2048-cli-0.9.1
make clean && make CFLAGS="-g -O0" 2048-debug

# 3. Start game in debugger
echo "Step 3: Starting game in LLDB..."
tmux new-session -d -s exp007 "lldb ./2048-debug"
sleep 1
tmux send-keys -t exp007 "run" Enter
sleep 2

# 4. Make specific moves
echo "Step 4: Making controlled moves..."
tmux send-keys -t exp007 "sd"  # Down, Right
sleep 1

# 5. Break and examine
echo "Step 5: Breaking and examining memory..."
tmux send-keys -t exp007 C-c
sleep 0.5
tmux send-keys -t exp007 "frame select 7" Enter
sleep 0.5

# 6. Test the key positions
echo "Step 6: Testing grid access patterns..."
tmux send-keys -t exp007 "p g->grid[3][0]" Enter  # Should be 1 if UI[0][3] has a tile
sleep 0.5

# 7. Capture results
echo "Step 7: Capturing results..."
tmux capture-pane -t exp007 -p > exp007_reproduction.log

# 8. Cleanup
tmux kill-session -t exp007

echo "=== Reproduction complete. Check exp007_reproduction.log ==="
