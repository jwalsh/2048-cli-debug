#!/bin/bash
# LLDB down-right spam automation
# Sends 20 moves alternating down and right

echo "Starting 20-move down-right spam sequence..."

for i in {1..10}; do
    echo "Move $((i*2-1)): DOWN"
    tmux send-keys -t lldb2048 "continue" Enter
    sleep 0.5
    tmux send-keys -t lldb2048 "s"
    sleep 0.5
    
    echo "Move $((i*2)): RIGHT"
    tmux send-keys -t lldb2048 "continue" Enter
    sleep 0.5
    tmux send-keys -t lldb2048 "d"
    sleep 0.5
    
    # Quick check of score
    tmux send-keys -t lldb2048 "print g->score" Enter
    sleep 0.3
done

echo "Spam sequence complete!"