#!/bin/bash
# Manual TTY test runner with GUID-based logging
# Part of Issue #5: TTY-based 2048 controller implementation

set -euo pipefail

# Default parameters
SPAM_MOVES=${1:-50}
CHECK_INTERVAL=${2:-10}
TEST_GUID=$(uuidgen | tr '[:upper:]' '[:lower:]')
LOG_DIR="logs/manual_test_${TEST_GUID}"

# Create logging structure
mkdir -p "$LOG_DIR"/{boards,checkpoints}

# Initialize config
cat > "$LOG_DIR/config.json" << EOF
{
  "test_guid": "$TEST_GUID",
  "start_time": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "spam_moves": $SPAM_MOVES,
  "check_interval": $CHECK_INTERVAL,
  "strategy": "down_right_spam"
}
EOF

# Initialize move log
echo "# Move log for test $TEST_GUID" > "$LOG_DIR/moves.log"
echo "# Format: move_number,direction,timestamp" >> "$LOG_DIR/moves.log"

echo "🎮 Starting Manual TTY Test"
echo "Test ID: $TEST_GUID"
echo "Spam moves: $SPAM_MOVES"
echo "Check interval: $CHECK_INTERVAL"
echo ""

# Counter for moves
MOVE_COUNT=0

# Function to log a move
log_move() {
    local direction=$1
    echo "$MOVE_COUNT,$direction,$(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$LOG_DIR/moves.log"
}

# Function to save board snapshot
save_board() {
    local board_file="$LOG_DIR/boards/move_$(printf "%04d" $MOVE_COUNT).txt"
    # TODO: Capture actual board state from TTY
    echo "Board snapshot at move $MOVE_COUNT" > "$board_file"
    date >> "$board_file"
}

# Function to check complexity
check_complexity() {
    # TODO: Implement actual complexity check
    # For now, just return a random decision
    if [ $((RANDOM % 3)) -eq 0 ] && [ $MOVE_COUNT -gt 50 ]; then
        return 1  # Complex
    fi
    return 0  # Not complex
}

# Function to handle manual inspection
manual_inspection() {
    local checkpoint_file="$LOG_DIR/checkpoints/check_$(printf "%04d" $MOVE_COUNT).txt"
    
    echo "=== MANUAL INSPECTION REQUIRED ===" | tee "$checkpoint_file"
    echo "Test: $TEST_GUID" | tee -a "$checkpoint_file"
    echo "Move: $MOVE_COUNT" | tee -a "$checkpoint_file"
    echo "" | tee -a "$checkpoint_file"
    
    # TODO: Display actual board state
    echo "[Board state would be shown here]" | tee -a "$checkpoint_file"
    
    echo ""
    echo "Options:"
    echo "  [c] Continue auto-spam"
    echo "  [m] Manual move"
    echo "  [s] Switch strategy"
    echo "  [q] Quit and analyze"
    
    read -p "Choice: " choice
    echo "User chose: $choice" >> "$checkpoint_file"
    
    case $choice in
        c) echo "Continuing auto-spam..." ;;
        m) 
            read -p "Enter move [w/a/s/d]: " move
            echo "Manual move: $move" >> "$checkpoint_file"
            log_move "manual_$move"
            ;;
        s) echo "Strategy switching not implemented yet" ;;
        q) finish_test; exit 0 ;;
        *) echo "Invalid choice, continuing..." ;;
    esac
}

# Function to finish test
finish_test() {
    cat > "$LOG_DIR/summary.json" << EOF
{
  "test_guid": "$TEST_GUID",
  "end_time": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "total_moves": $MOVE_COUNT,
  "status": "completed"
}
EOF
    
    echo ""
    echo "Test completed!"
    echo "Results saved to: $LOG_DIR"
}

# Main test loop
echo "Starting auto-spam phase..."

while [ $MOVE_COUNT -lt 200 ]; do  # Safety limit
    MOVE_COUNT=$((MOVE_COUNT + 1))
    
    # Save board every 10 moves
    if [ $((MOVE_COUNT % 10)) -eq 0 ]; then
        save_board
    fi
    
    # Auto-spam phase
    if [ $MOVE_COUNT -le $SPAM_MOVES ]; then
        # Weighted random: 40% down, 30% right, 20% left, 10% up
        RAND=$((RANDOM % 10))
        if [ $RAND -lt 4 ]; then
            MOVE="s"  # down
        elif [ $RAND -lt 7 ]; then
            MOVE="d"  # right
        elif [ $RAND -lt 9 ]; then
            MOVE="a"  # left
        else
            MOVE="w"  # up
        fi
        
        log_move "$MOVE"
        echo -n "."  # Progress indicator
        
    else
        # Check complexity every CHECK_INTERVAL moves
        if [ $((MOVE_COUNT % CHECK_INTERVAL)) -eq 0 ]; then
            echo ""
            echo "Move $MOVE_COUNT: Checking complexity..."
            
            if ! check_complexity; then
                manual_inspection
            else
                echo "Board still simple, continuing auto-spam..."
            fi
        fi
    fi
    
    # TODO: Actually send move to game
    sleep 0.1  # Simulate move delay
done

finish_test