#!/bin/bash
# Automated 2048 gameplay with screenshots

# Create screenshot directory
SCREENSHOT_DIR="screenshots/game_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$SCREENSHOT_DIR"

# Build the game
echo "Building 2048..."
make -C 2048-cli-0.9.1 clean
make -C 2048-cli-0.9.1 2048

# Create a named pipe for sending commands
PIPE="/tmp/2048_pipe"
mkfifo "$PIPE" 2>/dev/null || true

# Function to take screenshot
take_screenshot() {
    local move_num=$1
    local filename="$SCREENSHOT_DIR/move_$(printf "%04d" $move_num).png"
    # Take screenshot of terminal window
    osascript -e 'tell application "Terminal" to activate'
    sleep 0.2
    screencapture -x -R "0,0,800,600" "$filename"
    echo "Screenshot saved: $filename"
}

# Function to analyze game state from terminal output
analyze_and_move() {
    # Simple strategy: try moves in order - down, right, left, up
    # This tends to keep high tiles in bottom corners
    local moves=("s" "d" "a" "w")
    local move_names=("down" "right" "left" "up")
    
    # Try each move
    for i in {0..3}; do
        echo "${moves[$i]}"
        echo "Trying move: ${move_names[$i]}"
        return
    done
}

# Start the game in background
echo "Starting 2048..."
2048-cli-0.9.1/2048 < "$PIPE" &
GAME_PID=$!

# Give game time to start
sleep 1

# Game loop
MOVE_COUNT=0
MAX_MOVES=500

# Take initial screenshot
take_screenshot 0

while [ $MOVE_COUNT -lt $MAX_MOVES ]; do
    MOVE_COUNT=$((MOVE_COUNT + 1))
    
    # Determine next move (simple AI strategy)
    # Prefer: down > right > left > up
    # This keeps larger tiles in bottom-right corner
    
    # Random selection weighted towards down and right
    RAND=$((RANDOM % 10))
    if [ $RAND -lt 4 ]; then
        MOVE="s"  # down
        MOVE_NAME="down"
    elif [ $RAND -lt 7 ]; then
        MOVE="d"  # right
        MOVE_NAME="right"
    elif [ $RAND -lt 9 ]; then
        MOVE="a"  # left
        MOVE_NAME="left"
    else
        MOVE="w"  # up
        MOVE_NAME="up"
    fi
    
    echo "Move $MOVE_COUNT: $MOVE_NAME"
    
    # Send move to game
    echo "$MOVE" > "$PIPE"
    
    # Wait for board to update
    sleep 0.3
    
    # Take screenshot
    take_screenshot $MOVE_COUNT
    
    # Check if game is still running
    if ! ps -p $GAME_PID > /dev/null; then
        echo "Game ended!"
        break
    fi
done

# Cleanup
rm -f "$PIPE"
echo "Screenshots saved to: $SCREENSHOT_DIR"