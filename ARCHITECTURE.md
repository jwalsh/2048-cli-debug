# 2048 CLI Architecture

## Overview

The 2048 CLI game is built with a modular architecture that separates game logic, rendering, and user input. This document describes the system design, memory layout, and debugging infrastructure.

## System Architecture

```
┌─────────────────┐     ┌──────────────┐     ┌─────────────┐
│   User Input    │────▶│  Game Engine │────▶│   Display   │
│  (keyboard/AI)  │     │   (engine.c) │     │  (gfx_*.c)  │
└─────────────────┘     └──────────────┘     └─────────────┘
         │                      │                     │
         │                      ▼                     │
         │              ┌──────────────┐             │
         └─────────────▶│  Game State  │◀────────────┘
                        │ (gamestate)  │
                        └──────────────┘
```

## Core Components

### 1. Main Loop (`main.c`)

The main game loop follows a simple pattern:

```c
while (game_running) {
    if (g->opts->interactive) {
        input = gfx_getch(s);    // Get user input
    } else if (g->opts->ai) {
        input = ai_move(g);      // Get AI decision
    }
    
    engine_tick(g, s, input);    // Update game state
    
    if (g->opts->interactive) {
        gfx_draw(s, g);          // Render display
    }
}
```

### 2. Game State (`engine.h`)

The central data structure that holds all game information:

```c
struct gamestate {
    // Board data
    int *grid_data_ptr;      // 1D array of tile values
    int **grid;              // 2D pointer array for row access
    int gridsize;            // Total number of cells
    
    // Game status
    int moved;               // Flag: did last action cause movement?
    long score;              // Current score
    long score_high;         // Highest score achieved
    long score_last;         // Previous score (for display)
    int blocks_in_play;      // Number of non-zero tiles
    
    // Configuration
    struct gameoptions *opts;
    int print_width;         // Width for number formatting
};
```

### 3. Memory Layout

The game uses an efficient dual-array system for the board:

```
Memory Layout Example (4x4 grid):

grid_data_ptr (contiguous memory):
[2][0][4][8][0][2][0][0][16][32][0][0][4][0][0][2]
 0  1  2  3  4  5  6  7   8   9 10 11 12 13 14 15

grid (row pointers):
grid[0] → &grid_data_ptr[0]  → [2][0][4][8]
grid[1] → &grid_data_ptr[4]  → [0][2][0][0]
grid[2] → &grid_data_ptr[8]  → [16][32][0][0]
grid[3] → &grid_data_ptr[12] → [4][0][0][2]
```

Benefits:
- Cache-friendly sequential access
- Easy 2D indexing: `grid[row][col]`
- Single allocation/deallocation
- Efficient for both row and column operations

## Game Engine (`engine.c`)

### Move Processing

Each move involves three steps:

1. **Gravitate**: Slide all tiles in the move direction
2. **Merge**: Combine adjacent identical tiles
3. **Gravitate**: Slide again to fill gaps after merging

```c
void engine_move(struct gamestate *g, int direction) {
    gravitate(g, direction);
    merge(g, direction);
    gravitate(g, direction);
}
```

### Direction Encoding

Directions are encoded as integers:
- 0: UP
- 1: DOWN  
- 2: LEFT
- 3: RIGHT

## Graphics System

The game supports multiple rendering backends:

### Terminal (`gfx_terminal.c`)
- Uses ANSI escape codes
- VT100 compatible
- Minimal dependencies

### Curses (`gfx_curses.c`)
- NCurses library
- Better terminal handling
- Color support

### SDL (`gfx_sdl.c`)
- Graphical window
- Font rendering
- Future expansion

## AI System (`ai.c`)

The AI uses the expectimax algorithm:

```
┌─────────────┐
│ Current State│
└──────┬──────┘
       │
   ┌───▼───┐
   │Evaluate│ (for each possible move)
   └───┬───┘
       │
┌──────▼──────┐
│ Expected    │ (probability of tile spawns)
│   Value     │
└──────┬──────┘
       │
   ┌───▼───┐
   │ Choose │ (best expected value)
   └───────┘
```

Key metrics:
- Monotonicity: Tiles arranged in increasing order
- Smoothness: Adjacent tiles have similar values
- Free tiles: Number of empty spaces
- Max tile value: Progress toward 2048

## Debug Infrastructure

### LLDB Integration

Custom LLDB scripts provide:

1. **Board Visualization**
   ```lldb
   (lldb) board
   [    2     0     4     8 ]
   [    0     2     0     0 ]
   [   16    32     0     0 ]
   [    4     0     0     2 ]
   ```

2. **Memory Inspection**
   ```lldb
   (lldb) memory read -c 16 -f d g->grid_data_ptr
   ```

3. **State Tracking**
   - Breakpoints on key functions
   - Watchpoints on score changes
   - Automated state dumps

### Emacs Integration

The Emacs mode provides:

```
┌─────────────────┐
│   Source Code   │
│   (C files)     │
└────────┬────────┘
         │
    ┌────▼────┐
    │ 2048-mode│
    └────┬────┘
         │
    ┌────▼────────────┐
    │ Features:       │
    │ - Compilation   │
    │ - Debugging     │
    │ - Navigation    │
    │ - Visualization │
    └─────────────────┘
```

## Performance Considerations

### Memory Efficiency
- Single allocation for board data
- Minimal pointer chasing
- Stack-allocated temporary arrays

### CPU Efficiency
- Branch-free tile merging where possible
- Early exit conditions
- Efficient random number generation

### Optimization Opportunities
- SIMD operations for parallel tile processing
- Bitboard representation for faster operations
- Transposition tables for AI

## Build System

The Makefile supports multiple configurations:

```makefile
# Debug build
CFLAGS = -g -O0 -DDEBUG

# Release build  
CFLAGS = -O2 -DNDEBUG

# Sanitizer build
CFLAGS = -g -fsanitize=address,undefined
```

## Testing Architecture

### Unit Testing
- Individual function testing
- Mock game states
- Edge case validation

### Integration Testing
- Full game scenarios
- AI behavior verification
- Memory leak detection

### Debug Scripts
- Automated gameplay analysis
- State transition verification
- Performance profiling

## Future Enhancements

### Planned Features
1. Network multiplayer support
2. Replay system for game analysis
3. Statistics tracking
4. Custom board sizes and rules

### Architecture Extensions
1. Plugin system for new algorithms
2. Scripting interface (Lua/Python)
3. Web assembly compilation
4. Mobile platform support

## Security Considerations

### Input Validation
- Bounds checking on all array access
- Command line argument validation
- File path sanitization

### Memory Safety
- No dynamic format strings
- Careful pointer arithmetic
- Proper cleanup on exit

## Conclusion

The 2048 CLI architecture prioritizes:
- **Simplicity**: Clean separation of concerns
- **Efficiency**: Optimal memory layout and algorithms
- **Debuggability**: Comprehensive tooling support
- **Extensibility**: Modular design for easy enhancement

This architecture enables both casual play and deep analysis of the 2048 game mechanics.