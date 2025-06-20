# 2048 Debug Tools

This directory contains debugging and development tools for the 2048 CLI game.

## LLDB Debug Scripts

- `debug.lldb` - Basic debugging with automatic board state dumps
- `debug-interactive.lldb` - Interactive session with custom commands (board, raw, state)
- `debug-automated.lldb` - Automated gameplay with periodic state dumps
- `debug-symbols.lldb` - Symbol and type information dump

### Usage Examples

```bash
# Basic debugging
lldb ./2048 -s debug.lldb

# Interactive debugging with custom commands
lldb ./2048 -s debug-interactive.lldb

# Dump symbols
lldb ./2048 -s debug-symbols.lldb -o quit > symbols.txt
```

## Emacs Integration

### Files

- `2048-mode.el` - Main mode for 2048 development
- `2048-lldb.el` - LLDB integration
- `2048-analysis.el` - Game state analysis tools
- `.dir-locals.el` - Project-specific settings

### Setup

Add to your Emacs config:

```elisp
(add-to-list 'load-path "/path/to/2048-cli-0.9.1/")
(require '2048-mode)
```

### Key Bindings

- `C-c C-c` - Compile
- `C-c C-r` - Run game
- `C-c C-d` - Debug with LLDB
- `C-c C-a` - Run with AI
- `C-c C-f` - Find function
- `C-c C-b` - Go to board struct

## Game Screenshots

See `game-screenshot.txt` for example board output:

```
Score: 28 (+12)
   Hi: 932
-----------------------------
|    2 |      |    4 |    8 |
|      |      |      |    8 |
|      |      |      |      |
|      |      |      |      |
-----------------------------
```

## Build Targets

- `make` - Build standard terminal version
- `make CFLAGS='-g -O0'` - Build with debug symbols
- `make archive-source` - Create source backup
- `make download-source` - Download and extract source