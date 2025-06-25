#!/bin/bash
# Fixed mini pilot: 3 runs with proper tmux handling

# Get the directory where the game is located
GAME_DIR="/Users/jasonwalsh/projects/jwalsh/2048/2048-cli-0.9.1"
GAME_EXEC="$GAME_DIR/2048-debug"

# Verify game exists
if [ ! -f "$GAME_EXEC" ]; then
    echo "ERROR: Game executable not found at $GAME_EXEC"
    exit 1
fi

echo "=== 2048 Mini-Pilot: 3 runs of 150 moves ==="
echo "run,score,max_tile,final_board,timestamp" > pilot_results.csv

for run in {1..3}; do
    START_TIME=$(date +%s)
    echo -e "\n=== Run $run/3 starting at $(date) ==="
    
    # Clean environment
    pkill -f 2048-debug 2>/dev/null || true
    sleep 0.5
    
    # Start game with full path and verify it started
    echo "Starting game session pilot_$run..."
    tmux new-session -d -s "pilot_$run" -c "$GAME_DIR" "$GAME_EXEC"
    sleep 1
    
    # Verify session exists
    if ! tmux has-session -t "pilot_$run" 2>/dev/null; then
        echo "ERROR: Failed to start tmux session pilot_$run"
        continue
    fi
    
    # Initial board
    echo "Initial board:"
    tmux capture-pane -t "pilot_$run" -p | grep -A 6 "Score:" || echo "No board found yet"
    
    # Spam 150 moves (75 pairs)
    echo "Sending 150 moves..."
    for i in {1..75}; do
        tmux send-keys -t "pilot_$run" "s"
        sleep 0.05
        tmux send-keys -t "pilot_$run" "d"
        sleep 0.05
        
        # Progress indicator every 25 pairs
        if (( i % 25 == 0 )); then
            echo "Progress: $((i*2))/150 moves"
        fi
    done
    
    # Wait for final state
    sleep 1
    
    # Capture final UI
    echo -e "\nFinal board:"
    FINAL_STATE=$(tmux capture-pane -t "pilot_$run" -p)
    echo "$FINAL_STATE" | grep -A 6 "Score:" || echo "Could not find score"
    
    # Extract score (more robust extraction)
    SCORE=$(echo "$FINAL_STATE" | grep "Score:" | head -1 | awk '{print $2}')
    if [ -z "$SCORE" ]; then
        echo "Warning: Could not extract score"
        SCORE="0"
    fi
    
    # Find max tile (look for highest number in the board)
    MAX_TILE=$(echo "$FINAL_STATE" | grep -E "^\|" | grep -oE "[0-9]+" | sort -nr | head -1)
    if [ -z "$MAX_TILE" ]; then
        echo "Warning: Could not find max tile"
        MAX_TILE="0"
    fi
    
    # Save full board state
    echo "$FINAL_STATE" > "pilot_run_${run}_board.txt"
    
    # Calculate elapsed time
    END_TIME=$(date +%s)
    ELAPSED=$((END_TIME - START_TIME))
    
    # Save results
    echo "$run,$SCORE,$MAX_TILE,pilot_run_${run}_board.txt,$ELAPSED" >> pilot_results.csv
    echo "Run $run complete in ${ELAPSED}s - Score: $SCORE, Max tile: $MAX_TILE"
    
    # Cleanup
    tmux kill-session -t "pilot_$run" 2>/dev/null || true
done

echo -e "\n=== PILOT SUMMARY ==="
cat pilot_results.csv | column -t -s','
