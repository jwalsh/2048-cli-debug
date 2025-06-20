#!/bin/bash
# Debug demonstration script for 2048

echo "=== 2048 Debug Scripts Demo ==="
echo ""
echo "1. Symbol dump (outputs to symbols.txt):"
echo "   lldb ./2048 -s debug-symbols.lldb -o quit > symbols.txt"
echo ""
echo "2. Interactive debugging session:"
echo "   lldb ./2048 -s debug-interactive.lldb"
echo ""
echo "3. Automated game with state dumps:"
echo "   lldb ./2048 -s debug-automated.lldb"
echo ""
echo "4. Basic memory dump at startup:"
echo "   lldb ./2048 -s debug.lldb"
echo ""
echo "Example: Dumping board state on game start"
lldb ./2048 -o "b gamestate_init" -o "r" -o "finish" -o "p *g" -o "memory read -c 16 -f d g->grid_data_ptr" -o "quit" 2>/dev/null | grep -A20 "gamestate"