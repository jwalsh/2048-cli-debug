#!/bin/bash
# Script to capture game screenshots

echo "=== 2048 Game Demo ==="
echo ""
echo "1. Normal game (press 'q' to quit):"
echo "./2048"
echo ""

# Run with AI for a few moves to capture board states
echo "2. AI gameplay demonstration:"
timeout 5 ./2048 --ai 2>&1 | tee game-ai-output.txt

echo ""
echo "3. Game with custom size:"
./2048 --size 3 < /dev/null 2>&1 | head -20

echo ""
echo "4. Show help:"
./2048 -h