# Contributing to 2048 CLI Debug

Thank you for your interest in contributing to the 2048 CLI Debug project! This guide will help you understand the codebase, debugging tools, and development workflow.

## 🎯 Getting Started

### Prerequisites

1. **C Development Environment**
   - C99-compatible compiler (gcc/clang)
   - Make build system
   - Basic understanding of pointers and memory management

2. **Debugging Tools**
   - LLDB (required) - Primary debugger for macOS/Linux
   - GDB (optional) - Alternative debugger
   - Valgrind (optional) - Memory leak detection

3. **Emacs Setup** (optional but recommended)
   - Emacs 25.1 or higher
   - Basic Emacs knowledge (buffers, modes, key bindings)

## 🏗️ Understanding the Codebase

### Core Components

#### 1. Game Engine (`src/engine.c`)
```c
struct gamestate {
    int *grid_data_ptr;    // Raw grid data (1D array)
    int **grid;            // 2D view of grid data
    int gridsize;          // Total cells
    int moved;             // Movement flag
    long score;            // Current score
    // ... more fields
};
```

Key functions:
- `gamestate_init()` - Initialize game state
- `engine_move()` - Process player moves
- `engine_tick()` - Update game state

#### 2. Graphics Interface (`src/gfx_*.c`)
- `gfx_terminal.c` - Terminal/TTY rendering
- `gfx_curses.c` - NCurses interface
- `gfx_sdl.c` - SDL graphics (optional)

#### 3. AI System (`src/ai.c`)
- Implements expectimax algorithm
- Evaluates board positions
- Suggests optimal moves

### Memory Layout

The game uses an efficient memory layout:
```
grid_data_ptr -> [0][1][2][3][4][5][6][7][8][9][10][11][12][13][14][15]
                  ^           ^           ^            ^
grid[0] ---------+           |           |            |
grid[1] ---------------------+           |            |
grid[2] ---------------------------------+            |
grid[3] ----------------------------------------------+
```

## 🔍 Debugging Techniques

### LLDB Workflow

1. **Basic Debugging**
   ```bash
   lldb ./2048
   (lldb) b main                    # Set breakpoint
   (lldb) r                         # Run
   (lldb) p *g                      # Print game state
   (lldb) memory read g->grid_data_ptr -c 16
   ```

2. **Using Debug Scripts**
   ```bash
   lldb ./2048 -s debug-interactive.lldb
   (lldb) board                     # Custom command
   (lldb) state                     # Dump full state
   ```

3. **Memory Inspection**
   ```lldb
   # Watch score changes
   (lldb) watchpoint set variable g->score
   
   # Examine board memory
   (lldb) x/16dw g->grid_data_ptr
   ```

### GDB Alternative

If using GDB on Linux:
```bash
gdb ./2048
(gdb) set print pretty on
(gdb) break gamestate_new_block
(gdb) run
(gdb) print *g
(gdb) x/16d g->grid_data_ptr
```

### Memory Debugging

Using Valgrind:
```bash
valgrind --leak-check=full --show-leak-kinds=all ./2048
```

Using AddressSanitizer:
```bash
make CFLAGS="-g -O0 -fsanitize=address"
./2048
```

## 💻 Emacs Development Workflow

### Setup

1. Load the 2048 mode:
   ```elisp
   (load-file "/path/to/2048-mode.el")
   ```

2. Open a source file in the project

3. Enable 2048-mode: `M-x 2048-mode`

### Key Features

#### Compilation
- `C-c C-c` - Compile with debug flags
- `C-c C-r` - Run the game
- View errors in `*compilation*` buffer

#### Debugging
- `C-c C-d` - Start LLDB session
- Use `M-x gud-break` to set breakpoints
- Navigate with `M-x gud-next`, `M-x gud-step`

#### Code Navigation
- `M-.` - Jump to definition (requires TAGS)
- `M-,` - Jump back
- `C-c C-f` - Find specific game functions

#### Board Visualization
```elisp
;; Visualize a board state
M-x 2048-visualize-board
Board string: 2 0 4 0 0 2 0 0 8 0 0 0 0 0 0 0
```

### Custom Commands

Add to your Emacs config:
```elisp
(defun my-2048-test-ai ()
  "Run AI test with custom parameters."
  (interactive)
  (compile "./2048 --ai --size 5"))

(define-key 2048-mode-map (kbd "C-c t") 'my-2048-test-ai)
```

## 🧪 Testing Changes

### Manual Testing
1. Build with debug symbols: `make CFLAGS="-g -O0"`
2. Test basic gameplay
3. Test with AI: `./2048 --ai`
4. Test edge cases (full board, large scores)

### Debug Script Testing
```bash
# Test each debug script
for script in debug*.lldb; do
    echo "Testing $script"
    lldb ./2048 -s $script -b -o "quit" > /dev/null 2>&1
    echo "Exit code: $?"
done
```

### Performance Testing
```bash
# Benchmark AI performance
time ./2048 --ai --size 5 < /dev/null

# Profile with instruments (macOS)
instruments -t "Time Profiler" ./2048 --ai
```

## 📝 Code Style Guidelines

### C Code
- Use 4 spaces for indentation (no tabs)
- K&R style braces
- Descriptive variable names
- Comment complex algorithms

Example:
```c
int engine_move(struct gamestate *g, int direction) {
    if (direction < 0 || direction > 3) {
        return -1;  // Invalid direction
    }
    
    // Perform move logic
    gravitate(g, direction);
    merge(g, direction);
    gravitate(g, direction);
    
    return 0;
}
```

### LLDB Scripts
- Comment each breakpoint's purpose
- Use descriptive command aliases
- Group related commands

### Emacs Lisp
- Follow Emacs Lisp conventions
- Use `defcustom` for user options
- Provide docstrings for all functions

## 🚀 Submitting Changes

### Process

1. **Fork and Clone**
   ```bash
   gh repo fork jwalsh/2048-cli-debug --clone
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Changes**
   - Write clean, documented code
   - Test thoroughly
   - Update documentation if needed

4. **Commit with Conventional Commits**
   ```bash
   git commit -m "feat: add board state export function"
   ```

5. **Push and Create PR**
   ```bash
   git push origin feature/your-feature-name
   gh pr create
   ```

### Commit Message Format
```
type(scope): description

[optional body]

[optional footer]
```

Types: feat, fix, docs, style, refactor, test, chore

### Pull Request Guidelines
- Describe what changes you made and why
- Reference any related issues
- Include testing steps
- Add screenshots for UI changes

## 📚 Resources

### C Programming
- [C Programming Language (K&R)](https://en.wikipedia.org/wiki/The_C_Programming_Language)
- [Modern C](https://modernc.gforge.inria.fr/)

### Debugging
- [LLDB Tutorial](https://lldb.llvm.org/use/tutorial.html)
- [GDB Documentation](https://www.gnu.org/software/gdb/documentation/)

### Emacs
- [Emacs Manual](https://www.gnu.org/software/emacs/manual/)
- [GUD Mode Documentation](https://www.gnu.org/software/emacs/manual/html_node/emacs/Debuggers.html)

### 2048 Algorithm
- [2048 AI Strategies](https://stackoverflow.com/questions/22342854/what-is-the-optimal-algorithm-for-the-game-2048)
- [Expectimax Algorithm](https://en.wikipedia.org/wiki/Expectiminimax)

## ❓ Questions?

- Open an issue for bugs or feature requests
- Start a discussion for general questions
- Tag @jwalsh for code review

Happy debugging! 🎮🔍