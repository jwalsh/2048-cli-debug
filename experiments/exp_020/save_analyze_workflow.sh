#!/bin/bash
# Workflow: Play → Save → Analyze → Dump → Continue

SESSION="lldb2048"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
SAVE_DIR="saves/${TIMESTAMP}"

echo "=== 2048 Save/Analyze Workflow ==="
echo "Timestamp: ${TIMESTAMP}"

# Create save directory
mkdir -p "${SAVE_DIR}"

# Function to send LLDB command and wait
lldb_cmd() {
    tmux send-keys -t ${SESSION} "$1" Enter
    sleep 0.5
}

# Function to capture game display
capture_display() {
    tmux capture-pane -t ${SESSION} -p | grep -B 2 -A 10 "Score:" > "${SAVE_DIR}/display.txt" 2>/dev/null || \
    tmux capture-pane -t ${SESSION} -p | tail -20 > "${SAVE_DIR}/display.txt"
}

# Step 1: Get current state
echo "1. Capturing current state..."
lldb_cmd "print g->score"
lldb_cmd "print g->blocks_in_play"
capture_display

# Step 2: Save memory dumps
echo "2. Saving memory dumps..."
lldb_cmd "memory read --outfile ${SAVE_DIR}/gamestate.bin --binary --count 200 g"
lldb_cmd "memory read --outfile ${SAVE_DIR}/grid.bin --binary --count 64 g->grid_data_ptr"

# Step 3: Save readable formats
echo "3. Saving readable formats..."
lldb_cmd "memory read --outfile ${SAVE_DIR}/grid.txt --count 16 --format 'int32_t[]' g->grid_data_ptr"
lldb_cmd "print *g" # This will show in capture

# Step 4: Create core dump
echo "4. Creating core dump..."
lldb_cmd "process save-core --style modified-memory ${SAVE_DIR}/core.dump"

# Step 5: Capture full LLDB state
echo "5. Capturing LLDB session..."
tmux capture-pane -t ${SESSION} -p > "${SAVE_DIR}/lldb_session.txt"

# Step 6: Analyze with external tools
echo "6. Analyzing saved data..."

# Hex dump of grid
if [ -f "${SAVE_DIR}/grid.bin" ]; then
    hexdump -C "${SAVE_DIR}/grid.bin" > "${SAVE_DIR}/grid_hex.txt"
    echo "  - Created grid_hex.txt"
fi

# Create analysis script
cat > "${SAVE_DIR}/analyze.py" << 'EOF'
import struct
import sys
import os

save_dir = os.path.dirname(os.path.abspath(__file__))

# Read grid data
with open(os.path.join(save_dir, 'grid.bin'), 'rb') as f:
    grid_data = f.read()

# Decode grid
values = struct.unpack('<16I', grid_data)

# Calculate statistics
non_zero = [v for v in values if v > 0]
tiles = [2**v if v > 0 else 0 for v in values]
max_tile = max(tiles)
total_tiles = len(non_zero)
empty_cells = 16 - total_tiles

print("=== Board Analysis ===")
print(f"Timestamp: {os.path.basename(save_dir)}")
print(f"Non-empty cells: {total_tiles}")
print(f"Empty cells: {empty_cells}")
print(f"Highest tile: {max_tile}")
print(f"\nBoard layout:")

# Print board (accounting for column-major storage)
for row in range(4):
    row_str = "|"
    for col in range(4):
        idx = col * 4 + row  # Column-major
        tile = tiles[idx]
        row_str += f"{str(tile):>5} |"
    print(row_str)

# Save summary
with open(os.path.join(save_dir, 'summary.txt'), 'w') as f:
    f.write(f"Highest tile: {max_tile}\n")
    f.write(f"Empty cells: {empty_cells}\n")
    f.write(f"Board hash: {hash(tuple(values))}\n")
EOF

# Run analysis
python3 "${SAVE_DIR}/analyze.py" > "${SAVE_DIR}/analysis.txt"
cat "${SAVE_DIR}/analysis.txt"

# Step 7: Create metadata
echo "7. Creating metadata..."
cat > "${SAVE_DIR}/metadata.json" << EOF
{
  "timestamp": "${TIMESTAMP}",
  "save_dir": "${SAVE_DIR}",
  "files": {
    "gamestate": "gamestate.bin",
    "grid": "grid.bin",
    "core": "core.dump",
    "display": "display.txt",
    "analysis": "analysis.txt"
  }
}
EOF

echo ""
echo "✅ Workflow complete! Saved to: ${SAVE_DIR}/"
ls -la "${SAVE_DIR}/"