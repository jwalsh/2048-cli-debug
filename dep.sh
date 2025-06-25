#!/bin/bash
# Dependency checker for 2048 LLDB debugging project

echo "=== 2048 LLDB Debugging Dependencies Check ==="
echo ""

# Track if all dependencies are met
ALL_GOOD=true

# Function to check if command exists
check_command() {
    local cmd=$1
    local description=$2
    local install_hint=$3
    
    if command -v "$cmd" &> /dev/null; then
        echo "✓ $cmd: $(command -v "$cmd")"
        # Get version info if possible
        case "$cmd" in
            lldb)
                lldb --version 2>&1 | head -1 | sed 's/^/  /'
                ;;
            hexdump)
                echo "  Part of BSD utilities"
                ;;
            tmux)
                tmux -V | sed 's/^/  /'
                ;;
            tree)
                tree --version 2>&1 | head -1 | sed 's/^/  /'
                ;;
            python3)
                python3 --version | sed 's/^/  /'
                ;;
        esac
    else
        echo "✗ $cmd: NOT FOUND"
        echo "  $description"
        if [ -n "$install_hint" ]; then
            echo "  Install: $install_hint"
        fi
        ALL_GOOD=false
    fi
    echo ""
}

# Core requirements
echo "=== Core Requirements ==="
check_command "lldb" "LLVM debugger for memory inspection" "xcode-select --install"
check_command "hexdump" "Binary file viewer" "Should be pre-installed on macOS"
check_command "clang" "C compiler for debug builds" "xcode-select --install"

# Session management
echo "=== Session Management ==="
check_command "tmux" "Terminal multiplexer for persistent sessions" "brew install tmux"

# Analysis tools
echo "=== Analysis Tools ==="
check_command "hexdump" "Hexadecimal dump utility" "Pre-installed on macOS"
check_command "xxd" "Alternative hex viewer" "Pre-installed on macOS"
check_command "tree" "Directory structure viewer" "brew install tree"
check_command "md5sum" "Checksum calculator" "brew install coreutils"

# Optional but useful
echo "=== Optional Tools ==="
check_command "python3" "For analysis scripts" "brew install python3"
check_command "jq" "JSON processor" "brew install jq"
check_command "watch" "Command repeater" "brew install watch"

# Emacs hexl-mode check
echo "=== Emacs Integration ==="
if command -v emacs &> /dev/null; then
    echo "✓ emacs: $(command -v emacs)"
    emacs --version | head -1 | sed 's/^/  /'
    echo "  hexl-mode: Built-in for hex editing"
    echo "  To use: M-x hexl-find-file"
else
    echo "✗ emacs: NOT FOUND"
    echo "  Install: brew install emacs"
fi
echo ""

# Summary
if [ "$ALL_GOOD" = true ]; then
    echo "✅ All core dependencies are satisfied!"
else
    echo "❌ Some dependencies are missing. Please install them."
fi

echo ""
echo "=== Quick Start ==="
echo "1. Build with debug symbols: make clean && clang -g -O0 ..."
echo "2. Start LLDB session: tmux new -s lldb2048 'lldb ./2048-debug'"
echo "3. Set breakpoints: breakpoint set -n gamestate_tick"
echo "4. Save states: memory read --outfile state.bin --binary g"
echo "5. View hex: hexdump -C state.bin"
echo "6. Emacs hex edit: emacs -nw --eval '(hexl-find-file \"state.bin\")'"