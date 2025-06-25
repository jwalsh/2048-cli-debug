#!/bin/bash
# Show Claude the board state directly

echo "Starting 2048 and showing initial board..."
echo ""

# Start game, make no moves, just quit to see initial state
echo "q" | 2048-cli-0.9.1/2048 | tail -10

echo ""
echo "Claude: Looking at this board, I would make move: _____"