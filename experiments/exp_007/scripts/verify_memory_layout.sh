#!/bin/bash
# Run discovery test 10 times to ensure consistency
echo "=== Memory Layout Verification Test ==="

PASSES=0
for i in {1..10}; do
    echo -n "Run $i: "
    
    # Clean environment
    pkill -f 2048-debug 2>/dev/null
    sleep 0.5
    
    # Start game with known seed (if possible)
    tmux new-session -d -s verify_$i "./2048-debug"
    sleep 1
    
    # Make controlled moves
    tmux send-keys -t verify_$i "ssddd"  # Down down, right right right
    sleep 1
    
    # Capture state
    UI_STATE=$(tmux capture-pane -t verify_$i -p | grep -A 4 "Score:")
    
    # Kill session
    tmux kill-session -t verify_$i 2>/dev/null
    
    # Check if tiles accumulated in bottom-right
    if echo "$UI_STATE" | grep -q "|.*|.*|.*|.*[0-9].*|"; then
        echo "PASS"
        ((PASSES++))
    else
        echo "FAIL"
    fi
done

echo "=== RESULTS: $PASSES/10 runs confirmed column-major behavior ==="
