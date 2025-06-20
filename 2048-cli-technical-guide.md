# 2048-CLI: Comprehensive Technical Guide

## Table of Contents

1. [Introduction](#introduction)
2. [Architecture Overview](#architecture-overview)
3. [Core Components](#core-components)
   - [Game Engine](#game-engine)
   - [Graphics Frontends](#graphics-frontends)
   - [Merge Algorithms](#merge-algorithms)
   - [AI Implementation](#ai-implementation)
   - [Highscore Management](#highscore-management)
   - [Command-line Options](#command-line-options)
4. [API Documentation](#api-documentation)
   - [Engine API](#engine-api)
   - [Graphics API](#graphics-api)
   - [Merge API](#merge-api)
   - [AI API](#ai-api)
   - [Highscore API](#highscore-api)
5. [Building and Compilation](#building-and-compilation)
   - [Build Requirements](#build-requirements)
   - [Build Options](#build-options)
   - [Makefile Targets](#makefile-targets)
6. [Extending the Project](#extending-the-project)
   - [Adding a New Graphics Frontend](#adding-a-new-graphics-frontend)
   - [Implementing a Custom Merge Algorithm](#implementing-a-custom-merge-algorithm)
   - [Enhancing the AI](#enhancing-the-ai)
7. [Deployment Guide](#deployment-guide)
   - [Linux Deployment](#linux-deployment)
   - [Package Management](#package-management)
8. [Troubleshooting](#troubleshooting)
   - [Common Issues](#common-issues)
   - [Terminal Compatibility](#terminal-compatibility)
   - [Graphic Frontend Issues](#graphic-frontend-issues)
9. [FAQ](#faq)
10. [Advanced Topics](#advanced-topics)
    - [Custom Game Rules](#custom-game-rules)
    - [Improving Performance](#improving-performance)
    - [Porting to Other Platforms](#porting-to-other-platforms)

## Introduction

2048-CLI is a command-line implementation of the popular 2048 game for Unix-like systems. The game provides a highly modular architecture that supports multiple display backends (terminal, ncurses, and SDL) and allows for custom game rules through its merge algorithm interface.

The original 2048 game was created by Gabriele Cirulli as a web-based sliding block puzzle. This CLI version brings the same addictive gameplay to the terminal, offering various configuration options and even an AI capability.

Unlike many command-line games, 2048-CLI offers three distinct graphical frontends:
1. A simple terminal-based renderer using ANSI escape sequences
2. An ncurses interface with color support
3. An SDL interface with font rendering capabilities

This technical guide provides comprehensive documentation for understanding, using, extending, and troubleshooting the 2048-CLI application.

## Architecture Overview

The 2048-CLI project follows a well-structured modular architecture, separating the core game logic from the display and input handling. This separation enables easy extension and customization of the game.

The architecture consists of several key components:

1. **Game Engine** (`engine.c`, `engine.h`): Contains the core game mechanics, including block movement, merging, scoring, and game state management.

2. **Graphics Interface** (`gfx.h`): Defines a common interface for all graphical frontends, allowing the engine to remain agnostic about how the game is displayed.

3. **Graphics Implementations**:
   - `gfx_terminal.c`: Renders the game using simple ANSI escape sequences
   - `gfx_curses.c`: Renders the game using the ncurses library
   - `gfx_sdl.c`: Renders the game using SDL (Simple DirectMedia Layer)

4. **Merge Rules** (`merge.h`, `merge_std.c`, `merge_fib.c`): Implements the rules for merging blocks, allowing for customization of game mechanics.

5. **AI System** (`ai.c`, `ai.h`): Provides a simple AI that can play the game automatically.

6. **Options Parser** (`options.c`, `options.h`): Handles command-line arguments and configures the game.

7. **Highscore System** (`highscore.c`, `highscore.h`): Manages persistent storage of high scores.

8. **Main Program** (`main.c`): Coordinates all components and implements the main game loop.

The modular design allows for easy extension and customization. For example, adding a new graphical frontend only requires implementing the functions defined in `gfx.h`, and new game rules can be created by implementing the functions in `merge.h`.

## Core Components

### Game Engine

The game engine is implemented in `engine.c` and `engine.h`. It handles the core game mechanics and maintains the game state.

#### Key Data Structures

```c
struct gamestate {
    /* Game state */
    int *grid_data_ptr;
    int **grid;
    int gridsize;
    int moved;
    long score;
    long score_high;
    long score_last;
    int print_width;
    int blocks_in_play;
    /* Variable command line options */
    struct gameoptions *opts;
};
```

The `gamestate` structure holds all the information about the current game state, including:
- The game grid (a 2D array of integers)
- The current score
- The high score
- Various metadata for game management

#### Key Functions

```c
/* Initialize a new game state */
struct gamestate* gamestate_init(int argc, char **argv);

/* Process one game tick (move in a direction) */
int gamestate_tick(struct gfx_state*, struct gamestate*, int, void (*callback)(struct gfx_state*, struct gamestate*));

/* Place a new random block on the grid */
void gamestate_new_block(struct gamestate*);

/* Check if the game is over */
int gamestate_end_condition(struct gamestate*);

/* Clean up the game state */
void gamestate_clear(struct gamestate*);
```

The core game logic is implemented in the `gravitate` and `merge` functions, which handle the movement and merging of blocks respectively.

#### Movement Logic

The `gravitate` function moves all blocks in a specified direction as far as they can go without merging. It uses a macro `swap_if_space` to swap a block with an empty space in the direction of movement.

```c
static void gravitate(struct gfx_state *s, struct gamestate *g, int d, void (*callback)(struct gfx_state *s, struct gamestate *g))
{
    /* Implementation details */
}
```

#### Merging Logic

The `merge` function combines adjacent blocks with the same value according to the rules defined in the merge algorithm. It uses a macro `merge_if_equal` to merge two blocks if they can be merged according to the current rule set.

```c
static void merge(struct gfx_state *s, struct gamestate *g, int d, void (*callback)(struct gfx_state *s, struct gamestate *g))
{
    /* Implementation details */
}
```

#### Game Tick

The `gamestate_tick` function represents one complete move in the game. It first gravitates blocks in the specified direction, then merges adjacent blocks, and finally gravitates again to fill any gaps created by merging.

```c
int gamestate_tick(struct gfx_state *s, struct gamestate *g, int d, void (*callback)(struct gfx_state*, struct gamestate*))
{
    g->moved = 0;
    gravitate(s, g, d, callback);
    merge(s, g, d, callback);
    gravitate(s, g, d, callback);
    return g->moved;
}
```

### Graphics Frontends

The game supports three different graphics frontends, all implementing the interface defined in `gfx.h`.

#### Graphics Interface

```c
/* Initialization of a graphics context */
struct gfx_state* gfx_init(struct gamestate *);

/* Drawing of a game_state onto a graphics context */
void gfx_draw(struct gfx_state *, struct gamestate *);

/* Blocking get character. Should not be buffered for best results */
int gfx_getch(struct gfx_state *);

/* Destruction of a graphics context */
void gfx_destroy(struct gfx_state *);

/* Sleep for a specifed millisecond period */
void gfx_sleep(int ms);
```

Each frontend implements these functions to provide a consistent interface to the game engine.

#### Terminal Frontend

The terminal frontend (`gfx_terminal.c`) is the simplest implementation, using ANSI escape sequences to draw the game grid in a standard terminal.

```c
struct gfx_state {
    struct termios oldt, newt;
};
```

It uses the `termios` library to configure the terminal for non-blocking input and ANSI escape sequences for positioning the cursor and clearing the screen.

```c
void gfx_draw(struct gfx_state *s, struct gamestate *g)
{
#ifdef VT100
    printf("\033[2J\033[H");
#endif

    /* Draw the game grid */
}
```

#### Ncurses Frontend

The ncurses frontend (`gfx_curses.c`) provides a more sophisticated terminal interface with support for colors and improved input handling.

```c
struct gfx_state {
    WINDOW *window;
    size_t window_height, window_width;
};
```

It creates an ncurses window for drawing the game grid and handles keyboard input through the ncurses API.

```c
void gfx_draw(struct gfx_state *s, struct gamestate *g)
{
    /* Use ncurses functions to draw the game grid */
}
```

#### SDL Frontend

The SDL frontend (`gfx_sdl.c`) provides a full graphical interface using the Simple DirectMedia Layer library.

```c
struct gfx_state {
    SDL_Window *window;
    SDL_Surface *surface;
    TTF_Font *font;
    int side_length;
    int window_height;
    int window_width;
};
```

It creates an SDL window and renders the game grid using SDL's graphics functions and TTF fonts.

```c
void gfx_draw(struct gfx_state *s, struct gamestate *g)
{
    /* Use SDL functions to draw the game grid */
}
```

### Merge Algorithms

The game supports different merge algorithms through the interface defined in `merge.h`. This allows for customization of the game rules.

#### Merge Interface

```c
/* Get the value of a block from its index */
long merge_value(const int v1);

/* Get the goal value (when the game is won) */
long merge_goal(void);

/* Check if two blocks can be merged */
int merge_possible(const int v1, const int v2);

/* Get the result of merging two blocks */
int merge_result(const int v1, const int v2);
```

#### Standard Merge Algorithm

The standard merge algorithm (`merge_std.c`) implements the original 2048 game rules: two blocks can be merged if they have the same value, and the result is a block with twice the value.

```c
const long merge_values[] = {
    0, 2, 4, 8, 16, 32, 64, 128, 256, 512,
    1024, 2048
};

inline int merge_possible(const int v1, const int v2)
{
    return v1 == v2;
}

inline int merge_result(const int v1, const int v2)
{
    return merge_possible(v1, v2) ? v1 + 1 : -1;
}
```

#### Fibonacci Merge Algorithm

The Fibonacci merge algorithm (`merge_fib.c`) implements an alternative rule set where blocks represent Fibonacci numbers.

```c
const long merge_values[] = {
    0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144,
    233, 377, 610, 987, 1597
};

inline int merge_possible(const int v1, const int v2)
{
    return v1 == v2 - 1 || v2 == v1 - 1 ||
        ((v1 == 1 || v1 == 2) && (v2 == 1 || v2 == 2));
}

inline int merge_result(const int v1, const int v2)
{
    int max = v1 > v2 ? v1 : v2;
    return merge_possible(v1, v2) ? max + 1 : -1;
}
```

### AI Implementation

The AI system is implemented in `ai.c` and `ai.h`. It provides a simple interface for automating gameplay.

```c
int ai_move(struct gamestate *g)
{
    /* Ensure srand is called somewhere prior */
    if (g->opts->interactive) gfx_sleep(50);
    return moves[rand() % 4];
}
```

The current implementation is a simple random move generator, but the interface allows for more sophisticated AI algorithms to be implemented.

### Highscore Management

The highscore system is implemented in `highscore.c` and `highscore.h`. It provides functions for loading, saving, and resetting highscores.

```c
void highscore_reset(void);
long highscore_load(struct gamestate *g);
void highscore_save(struct gamestate *g);
```

Highscores are stored in a plain text file in the user's data directory, with the location determined based on XDG standards.

### Command-line Options

The options parser is implemented in `options.c` and `options.h`. It handles command-line arguments and configures the game accordingly.

```c
struct gameoptions {
    int grid_height;
    int grid_width;
    long spawn_value;
    int spawn_rate;
    bool enable_color;
    bool animate;
    bool ai;
    bool interactive;
};
```

The `parse_options` function processes command-line arguments and updates the game options accordingly.

```c
struct gameoptions* parse_options(struct gameoptions *opt, int argc, char **argv);
```

## API Documentation

### Engine API

#### `struct gamestate* gamestate_init(int argc, char **argv)`

Initializes a new game state based on the provided command-line arguments.

**Parameters:**
- `argc`: The number of command-line arguments
- `argv`: The command-line arguments

**Returns:**
- A pointer to the initialized game state, or NULL if initialization failed

#### `int gamestate_tick(struct gfx_state *s, struct gamestate *g, int d, void (*callback)(struct gfx_state*, struct gamestate*))`

Processes one game tick (move in a direction).

**Parameters:**
- `s`: The graphics state
- `g`: The game state
- `d`: The direction to move (dir_up, dir_down, dir_left, dir_right)
- `callback`: A function to call after each step of the movement animation

**Returns:**
- 1 if the move was valid and changed the game state, 0 otherwise

#### `void gamestate_new_block(struct gamestate *g)`

Places a new random block on the grid.

**Parameters:**
- `g`: The game state

#### `int gamestate_end_condition(struct gamestate *g)`

Checks if the game is over.

**Parameters:**
- `g`: The game state

**Returns:**
- 1 if the game is won, -1 if the game is lost, 0 if the game is still in progress

#### `void gamestate_clear(struct gamestate *g)`

Cleans up the game state.

**Parameters:**
- `g`: The game state

### Graphics API

#### `struct gfx_state* gfx_init(struct gamestate *g)`

Initializes a graphics context.

**Parameters:**
- `g`: The game state

**Returns:**
- A pointer to the initialized graphics state, or NULL if initialization failed

#### `void gfx_draw(struct gfx_state *s, struct gamestate *g)`

Draws the game state on the graphics context.

**Parameters:**
- `s`: The graphics state
- `g`: The game state

#### `int gfx_getch(struct gfx_state *s)`

Gets a character from the input.

**Parameters:**
- `s`: The graphics state

**Returns:**
- The character read from the input

#### `void gfx_destroy(struct gfx_state *s)`

Cleans up the graphics context.

**Parameters:**
- `s`: The graphics state

#### `void gfx_sleep(int ms)`

Sleeps for the specified number of milliseconds.

**Parameters:**
- `ms`: The number of milliseconds to sleep

### Merge API

#### `long merge_value(const int v1)`

Gets the value of a block from its index.

**Parameters:**
- `v1`: The block index

**Returns:**
- The value of the block

#### `long merge_goal(void)`

Gets the goal value (when the game is won).

**Returns:**
- The index of the goal value

#### `int merge_possible(const int v1, const int v2)`

Checks if two blocks can be merged.

**Parameters:**
- `v1`: The first block index
- `v2`: The second block index

**Returns:**
- 1 if the blocks can be merged, 0 otherwise

#### `int merge_result(const int v1, const int v2)`

Gets the result of merging two blocks.

**Parameters:**
- `v1`: The first block index
- `v2`: The second block index

**Returns:**
- The index of the merged block, or -1 if the blocks cannot be merged

### AI API

#### `int ai_move(struct gamestate *g)`

Gets the next move from the AI.

**Parameters:**
- `g`: The game state

**Returns:**
- The direction to move (as a character: 'w', 'a', 's', 'd')

### Highscore API

#### `void highscore_reset(void)`

Resets the highscore file.

#### `long highscore_load(struct gamestate *g)`

Loads the highscore from the file.

**Parameters:**
- `g`: The game state (can be NULL if just querying the highscore)

**Returns:**
- The highscore value

#### `void highscore_save(struct gamestate *g)`

Saves the current score as the highscore if it's higher than the existing highscore.

**Parameters:**
- `g`: The game state

## Building and Compilation

### Build Requirements

To build the 2048-CLI project, you need the following dependencies:

- A C compiler (clang or gcc)
- For the terminal version:
  - A VT100-compatible terminal
  - termios.h
- For the ncurses version:
  - ncurses development libraries
- For the SDL version:
  - SDL2 development libraries
  - SDL2_ttf development libraries

On Debian/Ubuntu systems, you can install these dependencies with:

```sh
apt-get install build-essential
apt-get install libncurses5-dev
apt-get install libsdl2-dev libsdl2-ttf-dev
```

On RHEL/CentOS/Fedora systems:

```sh
yum install gcc make
yum install ncurses-devel
yum install SDL2-devel SDL2_ttf-devel
```

### Build Options

The project's Makefile provides several options for customizing the build:

- `CC`: The C compiler to use (default: clang)
- `TTF_FONT_PATH`: The path to the TTF font to use for the SDL version (default: res/Anonymous Pro.ttf)
- `CFLAGS`: Additional flags to pass to the compiler

### Makefile Targets

The Makefile defines several targets for building different versions of the game:

- `make` or `make terminal`: Build the terminal version
- `make curses`: Build the ncurses version
- `make sdl`: Build the SDL version
- `make clean`: Remove the compiled binary
- `make remake`: Clean and rebuild the default target

Example:

```sh
# Build the terminal version
make

# Build the ncurses version
make curses

# Build the SDL version
make sdl

# Clean up
make clean

# Clean and rebuild
make remake
```

## Extending the Project

### Adding a New Graphics Frontend

To add a new graphics frontend, you need to create a new C file that implements all the functions defined in `gfx.h`. Then, add a new target to the Makefile to compile your frontend.

Here's a template for a new graphics frontend:

```c
#include "gfx.h"

struct gfx_state {
    // Your frontend-specific state
};

struct gfx_state* gfx_init(struct gamestate *g)
{
    // Initialize your frontend
}

void gfx_draw(struct gfx_state *s, struct gamestate *g)
{
    // Draw the game state using your frontend
}

int gfx_getch(struct gfx_state *s)
{
    // Get input from your frontend
}

void gfx_destroy(struct gfx_state *s)
{
    // Clean up your frontend
}

void gfx_sleep(int ms)
{
    // Sleep for the specified number of milliseconds
}
```

And add to the Makefile:

```makefile
myfrontend: $(FILTERED_C_FILES) src/gfx_myfrontend.c
    $(CC) $(CFLAGS) $(FILTERED_C_FILES) $(MERGE_FILE) src/gfx_myfrontend.c -o $(PROGRAM) $(LDFLAGS) -lmyfrontendlib
```

### Implementing a Custom Merge Algorithm

To implement a custom merge algorithm, create a new C file that implements all the functions defined in `merge.h`. Then, update the Makefile to use your merge algorithm.

Here's a template for a custom merge algorithm:

```c
#include "merge.h"

#define MERGE_GOAL (int)((sizeof(merge_values)/sizeof(merge_values[0]))-1)

const long merge_values[] = {
    // Your custom values
};

inline long merge_value(const int v1)
{
    return v1 <= MERGE_GOAL ? merge_values[v1] : -1;
}

inline long merge_goal(void)
{
    return MERGE_GOAL;
}

inline int merge_possible(const int v1, const int v2)
{
    // Your custom merge condition
}

inline int merge_result(const int v1, const int v2)
{
    // Your custom merge result
}
```

And update the Makefile:

```makefile
MERGE_FILE := src/merge_custom.c
```

### Enhancing the AI

The current AI implementation is very simple, just making random moves. To enhance the AI, you can modify the `ai_move` function in `ai.c` to implement more sophisticated strategies.

Here's a template for an enhanced AI:

```c
int ai_move(struct gamestate *g)
{
    // Evaluate each possible move
    int best_move = -1;
    int best_score = -1;

    for (int i = 0; i < 4; i++) {
        // Clone the game state
        struct gamestate *clone = clone_gamestate(g);
        
        // Apply the move
        int direction = dir_map[i];
        int moved = gamestate_tick(NULL, clone, direction, NULL);
        
        if (moved) {
            // Evaluate the resulting state
            int score = evaluate_state(clone);
            
            if (score > best_score) {
                best_score = score;
                best_move = i;
            }
        }
        
        // Clean up
        gamestate_clear(clone);
    }
    
    // Return the best move
    return best_move >= 0 ? moves[best_move] : moves[rand() % 4];
}
```

Note that this would require implementing additional functions like `clone_gamestate` and `evaluate_state`.

## Deployment Guide

### Linux Deployment

To deploy the 2048-CLI game on a Linux system, follow these steps:

1. Clone the repository:
   ```sh
   git clone https://github.com/Tiehuis/2048-cli.git
   cd 2048-cli
   ```

2. Install the required dependencies (see [Build Requirements](#build-requirements)).

3. Build the desired version:
   ```sh
   make        # Terminal version
   # or
   make curses # Ncurses version
   # or
   make sdl    # SDL version
   ```

4. Install the binary to a system directory (optional):
   ```sh
   sudo cp 2048 /usr/local/bin/
   ```

### Package Management

On RHEL/CentOS/Fedora systems, you can install the game using the package manager:

```sh
sudo yum install 2048-cli       # Standard version
sudo yum install 2048-cli-nocurses # Version without ncurses
```

For other distributions, you might need to create a package manually.

## Troubleshooting

### Common Issues

#### Terminal version displays incorrectly

If the terminal version doesn't display correctly, it might be due to your terminal not supporting VT100 escape sequences. You can disable this by modifying the Makefile:

```makefile
# Before
CFLAGS         += -DINVERT_COLORS -DVT100 -O2

# After
CFLAGS         += -DINVERT_COLORS -O2
```

Then rebuild the game with `make remake`.

#### Game crashes on startup

This could be due to missing dependencies. Make sure you have installed all the required libraries for the version you're trying to run.

#### Ncurses version doesn't display colors

If the ncurses version doesn't display colors, make sure your terminal supports colors and that you're running the game with the `-c` option:

```sh
./2048 -c
```

#### SDL version can't find font

If the SDL version fails to start with a font-related error, make sure the font file exists in the expected location. You can specify a different font path when building:

```sh
make sdl TTF_FONT_PATH="/path/to/your/font.ttf"
```

### Terminal Compatibility

The terminal version of the game requires a VT100-compatible terminal to display correctly. Most modern terminal emulators support VT100 escape sequences, but if you encounter display issues, you can try:

1. Using a different terminal emulator
2. Disabling VT100 mode (see [Common Issues](#common-issues))
3. Using the ncurses version instead

### Graphic Frontend Issues

#### Ncurses Frontend

- **Display issues**: Make sure your terminal supports at least 16 colors and that the TERM environment variable is set correctly.
- **Input issues**: The ncurses frontend might not capture all key presses correctly. Try using the specified movement keys (hjkl or wasd).

#### SDL Frontend

- **Font issues**: Make sure the specified TTF font file exists and is readable.
- **Window issues**: If the SDL window doesn't display correctly, try adjusting your display settings or using a different frontend.

## FAQ

### General Questions

#### Q: What is 2048-CLI?

A: 2048-CLI is a command-line implementation of the popular 2048 game, offering multiple display backends (terminal, ncurses, and SDL) and customizable game rules.

#### Q: What platforms does 2048-CLI support?

A: 2048-CLI is designed for Unix-like systems, including Linux, macOS, and other POSIX-compliant systems. It may also work on Windows with appropriate Unix-like environments such as Cygwin or WSL.

#### Q: How do I install 2048-CLI?

A: You can build 2048-CLI from source (see [Building and Compilation](#building-and-compilation)) or install it via package managers on some Linux distributions.

### Gameplay Questions

#### Q: How do I play the game?

A: Use the hjkl or wasd keys to move the blocks in different directions. The goal is to merge blocks to create a block with the value 2048.

#### Q: How does scoring work?

A: Each time you merge two blocks, you earn points equal to the value of the resulting block. For example, merging two 2s gives you 4 points.

#### Q: Can I customize the game?

A: Yes, you can customize various aspects of the game through command-line options, such as the grid size, the spawn rate of new blocks, and whether to enable animations or colors.

### Technical Questions

#### Q: How do I add a new graphics frontend?

A: See [Adding a New Graphics Frontend](#adding-a-new-graphics-frontend) for details.

#### Q: How do I implement custom game rules?

A: See [Implementing a Custom Merge Algorithm](#implementing-a-custom-merge-algorithm) for details.

#### Q: How does the AI work?

A: The current AI implementation simply makes random moves. See [Enhancing the AI](#enhancing-the-ai) for details on how to implement a more sophisticated AI.

## Advanced Topics

### Custom Game Rules

The merge algorithm interface allows for creating custom game rules beyond the standard 2048 rules. Here are some ideas for custom rule sets:

#### Threes-Style Rules

Inspired by the game "Threes", where only 1 and 2 can merge to form 3, and then only like numbers can merge (3+3=6, 6+6=12, etc.).

```c
const long merge_values[] = {
    0, 1, 2, 3, 6, 12, 24, 48, 96, 192, 384, 768, 1536, 3072
};

inline int merge_possible(const int v1, const int v2)
{
    return (v1 == 1 && v2 == 2) || (v1 == 2 && v2 == 1) || (v1 == v2 && v1 > 2);
}

inline int merge_result(const int v1, const int v2)
{
    if (v1 == 1 && v2 == 2) return 3;
    if (v1 == 2 && v2 == 1) return 3;
    if (v1 == v2 && v1 > 2) return v1 + 1;
    return -1;
}
```

#### Modulo Rules

A rule set where numbers combine based on modular arithmetic.

```c
const long merge_values[] = {
    0, 1, 2, 3, 4, 5, 6, 7, 8, 9
};

inline int merge_possible(const int v1, const int v2)
{
    return (v1 + v2) % 10 == 0 || v1 == v2;
}

inline int merge_result(const int v1, const int v2)
{
    if ((v1 + v2) % 10 == 0) return 1;
    if (v1 == v2) return (v1 + 1) % 10;
    return -1;
}
```

### Improving Performance

While the game is already quite efficient for most use cases, here are some tips for improving performance in specific scenarios:

#### Optimizing Memory Usage

The game currently allocates memory for the grid as a 2D array with pointers to rows. For very large grids, this could be optimized to use a single contiguous block of memory:

```c
// Instead of:
g->grid = malloc(opt->grid_height * sizeof(int*));
int **iterator = g->grid;
for (i = 0; i < g->gridsize; i += opt->grid_width)
    *iterator++ = &g->grid_data_ptr[i];

// Use:
g->grid_data_ptr = calloc(g->gridsize, sizeof(int));
// Access elements directly with:
// g->grid_data_ptr[y * g->opts->grid_width + x]
```

#### Optimizing Rendering

For very large grids, rendering can become a bottleneck. Consider optimizing the rendering code to only redraw cells that have changed:

```c
void gfx_draw(struct gfx_state *s, struct gamestate *g)
{
    static int **last_grid = NULL;
    
    // Allocate last_grid if not already allocated
    if (!last_grid) {
        last_grid = malloc(g->opts->grid_height * sizeof(int*));
        for (int i = 0; i < g->opts->grid_height; i++) {
            last_grid[i] = malloc(g->opts->grid_width * sizeof(int));
            memset(last_grid[i], 0, g->opts->grid_width * sizeof(int));
        }
    }
    
    // Only redraw cells that have changed
    for (int y = 0; y < g->opts->grid_height; y++) {
        for (int x = 0; x < g->opts->grid_width; x++) {
            if (last_grid[y][x] != g->grid[x][y]) {
                // Redraw this cell
                last_grid[y][x] = g->grid[x][y];
            }
        }
    }
}
```

### Porting to Other Platforms

The game is designed for Unix-like systems, but it could be ported to other platforms with some modifications.

#### Windows Port

To port the game to Windows, you would need to:

1. Replace the Unix-specific terminal handling with Windows Console API calls
2. Replace the use of `termios.h` with Windows equivalents
3. Adapt the file paths in the highscore system to use Windows conventions
4. Use appropriate libraries for the ncurses and SDL frontends on Windows

#### Mobile Port

Porting to mobile platforms would require more significant changes:

1. Replace the keyboard input with touch gestures
2. Adapt the rendering to work with mobile screen sizes and orientations
3. Implement a mobile-friendly UI
4. Package the application for the target mobile platform

The modular architecture of the game makes these ports feasible, as you could maintain the core game logic while replacing only the platform-specific components.