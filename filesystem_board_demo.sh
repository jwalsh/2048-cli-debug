#!/bin/bash
# Filesystem-based 2048 board representation
# Each tile is represented by a file in a directory structure

# Initialize board directory
init_board() {
    rm -rf board_state
    for row in {0..3}; do
        for col in {0..3}; do
            mkdir -p board_state/$row/$col
        done
    done
}

# Set a tile value
set_tile() {
    local row=$1
    local col=$2
    local value=$3
    
    # Clear existing tile
    rm -f board_state/$row/$col/*
    
    # Set new tile (if not empty)
    if [ "$value" != "0" ]; then
        touch "board_state/$row/$col/$value"
    fi
}

# Get tile value
get_tile() {
    local row=$1
    local col=$2
    
    local tile=$(ls board_state/$row/$col/ 2>/dev/null | head -1)
    echo "${tile:-0}"
}

# Display board
display_board() {
    echo "-----------------------------"
    for row in {0..3}; do
        echo -n "|"
        for col in {0..3}; do
            local value=$(get_tile $row $col)
            printf "%5s |" "$value"
        done
        echo
    done
    echo "-----------------------------"
}

# Save board state to file
save_state() {
    local filename=$1
    > "$filename"
    for row in {0..3}; do
        for col in {0..3}; do
            local value=$(get_tile $row $col)
            echo "$row,$col,$value" >> "$filename"
        done
    done
    echo "Board saved to $filename"
}

# Load board state from file
load_state() {
    local filename=$1
    init_board
    while IFS=',' read -r row col value; do
        set_tile "$row" "$col" "$value"
    done < "$filename"
    echo "Board loaded from $filename"
}

# Demo: Create the board from our LLDB session
echo "=== Filesystem-based 2048 Board Demo ==="
echo "Creating board state from LLDB session..."

init_board

# Final board state from LLDB session:
# |    4 |    2 |      |      |
# |    2 |    4 |    2 |      |
# |    4 |    8 |      |      |
# |    2 |    4 |    8 |   16 |

set_tile 0 0 4
set_tile 0 1 2
set_tile 1 0 2
set_tile 1 1 4
set_tile 1 2 2
set_tile 2 0 4
set_tile 2 1 8
set_tile 3 0 2
set_tile 3 1 4
set_tile 3 2 8
set_tile 3 3 16

echo "Current board state:"
display_board

echo -e "\nFilesystem representation:"
echo "$ tree board_state/"
tree board_state/ 2>/dev/null || find board_state -type f | sort

echo -e "\nSaving state..."
save_state "game_state_score_80.sav"

echo -e "\nClearing board..."
init_board
display_board

echo -e "\nRestoring state..."
load_state "game_state_score_80.sav"
display_board

echo -e "\n=== Creative Ideas ==="
echo "1. Each file's modification time could encode move number"
echo "2. File permissions could encode tile properties (locked tiles?)"
echo "3. Symlinks could represent tile relationships"
echo "4. Extended attributes (xattr) for metadata"
echo "5. Git commits for move history!"