#!/bin/bash
# Use GNU screen to run 2048 under lldb and control it

SCREEN_SESSION="2048_debug"
SCREENSHOT_DIR="screenshots/game_$(date +%Y%m%d_%H%M%S)"
MOVE_COUNT=0
HIGH_SCORE=932

# Create screenshot directory
mkdir -p "$SCREENSHOT_DIR"

# Kill any existing screen session
screen -S "$SCREEN_SESSION" -X quit 2>/dev/null

# Create LLDB commands file
cat > lldb_commands.txt << 'EOF'
# Load the game
file 2048-cli-0.9.1/2048

# Set breakpoint after board is displayed
b print_board
br command add
script
import lldb
# Continue after hitting breakpoint
lldb.debugger.HandleCommand('c')
DONE

# Set breakpoint at input reading
b getchar
br command add
script
import lldb
import os
import time

# Read the board state from memory
target = lldb.debugger.GetSelectedTarget()
board_var = target.FindGlobalVariables("board", 1)[0]
score_var = target.FindGlobalVariables("score", 1)[0]

# Extract board values
board = []
for i in range(16):
    val = board_var.GetChildAtIndex(i).GetValueAsUnsigned()
    board.append(val)

score = score_var.GetValueAsUnsigned()

# Write state to file for external analysis
with open('/tmp/2048_state.txt', 'w') as f:
    f.write(f"SCORE:{score}\n")
    f.write(f"BOARD:{','.join(str(x) for x in board)}\n")

# Signal that we're ready for input
with open('/tmp/2048_ready', 'w') as f:
    f.write("1")

# Wait for move decision
while not os.path.exists('/tmp/2048_move'):
    time.sleep(0.1)

# Read the move
with open('/tmp/2048_move', 'r') as f:
    move = f.read().strip()

# Clean up
os.remove('/tmp/2048_move')

# Return the move character
thread = lldb.debugger.GetSelectedTarget().GetProcess().GetSelectedThread()
thread.SetSelectedFrame(0)
# Set return value (the character to return from getchar)
frame = thread.GetSelectedFrame()
# Return the move character
return_val = lldb.SBValue()
if move == 'w':
    thread.ReturnFromFrame(frame, lldb.SBValue.CreateValueFromExpression("return", "119"))  # 'w'
elif move == 's':
    thread.ReturnFromFrame(frame, lldb.SBValue.CreateValueFromExpression("return", "115"))  # 's'
elif move == 'a':
    thread.ReturnFromFrame(frame, lldb.SBValue.CreateValueFromExpression("return", "97"))   # 'a'
elif move == 'd':
    thread.ReturnFromFrame(frame, lldb.SBValue.CreateValueFromExpression("return", "100"))  # 'd'

lldb.debugger.HandleCommand('c')
DONE

# Run the game
run
EOF

# Start screen session with lldb
echo "Starting screen session..."
screen -dmS "$SCREEN_SESSION" bash -c "cd $(pwd) && lldb -s lldb_commands.txt"

# Give it time to start
sleep 2

# Function to take screenshot
take_screenshot() {
    local filename="$SCREENSHOT_DIR/move_$(printf "%04d" $1).png"
    # Capture the screen session
    screen -S "$SCREEN_SESSION" -X hardcopy /tmp/screen_capture.txt
    
    # Also take a GUI screenshot
    osascript -e 'tell application "Terminal" to activate'
    sleep 0.1
    screencapture -x "$filename"
    echo "Screenshot saved: $filename"
}

# Function to analyze board and determine move
analyze_board() {
    if [ ! -f /tmp/2048_state.txt ]; then
        echo "s"  # Default move
        return
    fi
    
    # Read board state
    local score=$(grep "SCORE:" /tmp/2048_state.txt | cut -d: -f2)
    local board=$(grep "BOARD:" /tmp/2048_state.txt | cut -d: -f2)
    
    echo "Current score: $score" >&2
    
    # Simple AI: prefer moves that keep high tiles in corners
    # Priority: down > right > left > up
    # This is a simplified version - you could make it smarter
    
    # Convert board to array
    IFS=',' read -ra BOARD_ARRAY <<< "$board"
    
    # Find max tile position
    local max_val=0
    local max_pos=0
    for i in "${!BOARD_ARRAY[@]}"; do
        if [ "${BOARD_ARRAY[$i]}" -gt "$max_val" ]; then
            max_val="${BOARD_ARRAY[$i]}"
            max_pos=$i
        fi
    done
    
    # Prefer keeping max tile in bottom-right corner (position 15)
    # Use weighted random selection
    local rand=$((RANDOM % 10))
    if [ $rand -lt 4 ]; then
        echo "s"  # down - 40%
    elif [ $rand -lt 7 ]; then
        echo "d"  # right - 30%
    elif [ $rand -lt 9 ]; then
        echo "a"  # left - 20%
    else
        echo "w"  # up - 10%
    fi
}

# Main game loop
echo "Starting automated 2048 gameplay..."
echo "Target high score: $HIGH_SCORE"

# Initial screenshot
take_screenshot 0

# Clean up any previous state files
rm -f /tmp/2048_ready /tmp/2048_move /tmp/2048_state.txt

# Game loop
while [ $MOVE_COUNT -lt 1000 ]; do
    # Wait for the game to be ready for input
    if [ -f /tmp/2048_ready ]; then
        rm -f /tmp/2048_ready
        
        MOVE_COUNT=$((MOVE_COUNT + 1))
        
        # Analyze board and determine move
        MOVE=$(analyze_board)
        
        case $MOVE in
            w) MOVE_NAME="UP" ;;
            s) MOVE_NAME="DOWN" ;;
            a) MOVE_NAME="LEFT" ;;
            d) MOVE_NAME="RIGHT" ;;
        esac
        
        echo "Move $MOVE_COUNT: $MOVE_NAME"
        
        # Send move to lldb
        echo "$MOVE" > /tmp/2048_move
        
        # Wait a bit for the move to process
        sleep 0.5
        
        # Take screenshot
        take_screenshot $MOVE_COUNT
        
        # Check if we beat the high score
        if [ -f /tmp/2048_state.txt ]; then
            CURRENT_SCORE=$(grep "SCORE:" /tmp/2048_state.txt | cut -d: -f2)
            if [ "$CURRENT_SCORE" -gt "$HIGH_SCORE" ]; then
                echo "🎉 NEW HIGH SCORE: $CURRENT_SCORE!"
                HIGH_SCORE=$CURRENT_SCORE
            fi
        fi
    fi
    
    # Small delay
    sleep 0.1
    
    # Check if screen session is still running
    if ! screen -list | grep -q "$SCREEN_SESSION"; then
        echo "Game ended!"
        break
    fi
done

# Cleanup
echo "Cleaning up..."
screen -S "$SCREEN_SESSION" -X quit 2>/dev/null
rm -f /tmp/2048_ready /tmp/2048_move /tmp/2048_state.txt lldb_commands.txt

echo "Game finished!"
echo "Screenshots saved to: $SCREENSHOT_DIR"
echo "Final high score: $HIGH_SCORE"