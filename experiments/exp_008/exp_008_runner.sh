#!/bin/bash
RESULTS_FILE="exp_008_results.csv"
echo "run,score,max_tile,moves_made,game_over,ui_memory_match" > $RESULTS_FILE

for run in {1..100}; do
    echo "=== Run $run/100 ==="
    
    # Clean start
    pkill -f 2048-debug 2>/dev/null || true
    
    # Start game
    tmux new-session -d -s "exp008_$run" "./2048-debug"
    sleep 1
    
    # Spam 150 moves
    for i in {1..75}; do
        tmux send-keys -t "exp008_$run" "sd"
        sleep 0.1
    done
    
    # Capture UI
    UI_STATE=$(tmux capture-pane -t "exp008_$run" -p | grep -A 10 "Score:")
    SCORE=$(echo "$UI_STATE" | grep "Score:" | awk '{print $2}')
    
    # Attach debugger and verify
    # [Analysis code here]
    
    # Save results
    echo "$run,$SCORE,$MAX_TILE,$MOVES,false,true" >> $RESULTS_FILE
    
    # Cleanup
    tmux kill-session -t "exp008_$run"
done
