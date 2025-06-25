#!/bin/bash
# cleanup_2048.sh - Emergency cleanup for 2048 processes and sessions
# Promoted from exp_006 after proving essential for process hygiene

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== 2048 Process Cleanup ===${NC}"

# Function to cleanup processes
cleanup_processes() {
    echo -n "Checking for 2048 processes... "
    
    if pgrep -f "2048" > /dev/null 2>&1; then
        echo -e "${RED}Found!${NC}"
        echo "Active 2048 processes:"
        ps aux | grep -E "(2048|2048-debug)" | grep -v grep || true
        
        echo -e "\nKilling processes..."
        pkill -f "2048" || true
        sleep 1
        
        # Force kill if needed
        if pgrep -f "2048" > /dev/null 2>&1; then
            echo -e "${YELLOW}Force killing stubborn processes...${NC}"
            pkill -9 -f "2048" || true
        fi
        
        echo -e "${GREEN}Processes cleaned!${NC}"
    else
        echo -e "${GREEN}None found!${NC}"
    fi
}

# Function to cleanup tmux sessions
cleanup_tmux() {
    echo -n "Checking for game-related tmux sessions... "
    
    local sessions=$(tmux list-sessions 2>/dev/null | grep -E "(game|2048|lldb|debug)" | cut -d: -f1 || true)
    
    if [ -n "$sessions" ]; then
        echo -e "${RED}Found!${NC}"
        echo "Active sessions:"
        echo "$sessions"
        
        echo -e "\nKilling tmux sessions..."
        echo "$sessions" | xargs -I {} tmux kill-session -t {} 2>/dev/null || true
        
        echo -e "${GREEN}Sessions cleaned!${NC}"
    else
        echo -e "${GREEN}None found!${NC}"
    fi
}

# Function to verify cleanup
verify_cleanup() {
    echo -e "\n${YELLOW}=== Verification ===${NC}"
    
    echo "Remaining 2048 processes:"
    ps aux | grep -E "(2048|2048-debug)" | grep -v grep || echo "  None!"
    
    echo -e "\nRemaining tmux sessions:"
    tmux list-sessions 2>/dev/null | grep -E "(game|2048|lldb|debug)" || echo "  None!"
    
    echo -e "\n${GREEN}✓ Cleanup complete!${NC}"
}

# Main execution
main() {
    cleanup_processes
    cleanup_tmux
    verify_cleanup
}

# Handle arguments
case "${1:-}" in
    -h|--help)
        echo "Usage: $0 [-h|--help] [-f|--force]"
        echo ""
        echo "Emergency cleanup for 2048 processes and tmux sessions."
        echo ""
        echo "Options:"
        echo "  -h, --help   Show this help message"
        echo "  -f, --force  Skip confirmation (not implemented yet)"
        exit 0
        ;;
    *)
        main
        ;;
esac