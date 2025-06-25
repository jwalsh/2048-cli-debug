CC             ?= clang
TTF_FONT_PATH  ?= 2048-cli-0.9.1/res/Anonymous Pro.ttf
CFLAGS         += -DTTF_FONT_PATH="\"$(TTF_FONT_PATH)\""
CFLAGS         += -Wno-visibility -Wno-incompatible-pointer-types -Wall -Wextra
CFLAGS         += -DINVERT_COLORS -DVT100

# Source code location
SRC_DIR        := 2048-cli-0.9.1/src
PROGRAM        := 2048
C_FILES        := $(wildcard $(SRC_DIR)/*.c)
MERGE_FILE     := $(SRC_DIR)/merge_std.c
FILTERED_C_FILES := $(filter-out $(SRC_DIR)/gfx%.c $(SRC_DIR)/merge%.c, $(C_FILES))

# Debug build settings
DEBUG_CFLAGS   := -g -O0 -DDEBUG
DEBUG_LDFLAGS  :=

# Release build settings
RELEASE_CFLAGS := -O2
RELEASE_LDFLAGS :=

# Default target
all: debug-terminal

# Debug builds
debug-terminal: CFLAGS += $(DEBUG_CFLAGS)
debug-terminal: LDFLAGS += $(DEBUG_LDFLAGS)
debug-terminal: $(FILTERED_C_FILES) $(SRC_DIR)/gfx_terminal.c
	$(CC) $(CFLAGS) $(FILTERED_C_FILES) $(MERGE_FILE) $(SRC_DIR)/gfx_terminal.c -o $(PROGRAM)_debug $(LDFLAGS)
	@echo "Debug build complete: $(PROGRAM)_debug"
	@echo "Run with GDB: gdb ./$(PROGRAM)_debug"

debug-curses: CFLAGS += $(DEBUG_CFLAGS)
debug-curses: LDFLAGS += $(DEBUG_LDFLAGS)
debug-curses: $(FILTERED_C_FILES) $(SRC_DIR)/gfx_curses.c
	$(CC) $(CFLAGS) $(FILTERED_C_FILES) $(MERGE_FILE) $(SRC_DIR)/gfx_curses.c -o $(PROGRAM)_debug $(LDFLAGS) -lcurses
	@echo "Debug build complete: $(PROGRAM)_debug"
	@echo "Run with GDB: gdb ./$(PROGRAM)_debug"

debug-sdl: CFLAGS += $(DEBUG_CFLAGS)
debug-sdl: LDFLAGS += $(DEBUG_LDFLAGS)
debug-sdl: $(FILTERED_C_FILES) $(SRC_DIR)/gfx_sdl.c
	$(CC) $(CFLAGS) $(FILTERED_C_FILES) $(MERGE_FILE) $(SRC_DIR)/gfx_sdl.c -o $(PROGRAM)_debug $(shell pkg-config --cflags sdl2) $(LDFLAGS) -lSDL2 -lSDL2_ttf
	@echo "Debug build complete: $(PROGRAM)_debug"
	@echo "Run with GDB: gdb ./$(PROGRAM)_debug"

# Regular builds
terminal: CFLAGS += $(RELEASE_CFLAGS)
terminal: LDFLAGS += $(RELEASE_LDFLAGS)
terminal: $(FILTERED_C_FILES) $(SRC_DIR)/gfx_terminal.c
	$(CC) $(CFLAGS) $(FILTERED_C_FILES) $(MERGE_FILE) $(SRC_DIR)/gfx_terminal.c -o $(PROGRAM) $(LDFLAGS)

curses: CFLAGS += $(RELEASE_CFLAGS)
curses: LDFLAGS += $(RELEASE_LDFLAGS)
curses: $(FILTERED_C_FILES) $(SRC_DIR)/gfx_curses.c
	$(CC) $(CFLAGS) $(FILTERED_C_FILES) $(MERGE_FILE) $(SRC_DIR)/gfx_curses.c -o $(PROGRAM) $(LDFLAGS) -lcurses

sdl: CFLAGS += $(RELEASE_CFLAGS)
sdl: LDFLAGS += $(RELEASE_LDFLAGS)
sdl: $(FILTERED_C_FILES) $(SRC_DIR)/gfx_sdl.c
	$(CC) $(CFLAGS) $(FILTERED_C_FILES) $(MERGE_FILE) $(SRC_DIR)/gfx_sdl.c -o $(PROGRAM) $(shell pkg-config --cflags sdl2) $(LDFLAGS) -lSDL2 -lSDL2_ttf

# Run with GDB
gdb-run: debug-terminal
	gdb ./$(PROGRAM)_debug

remake: clean all

clean:
	rm -f $(PROGRAM) $(PROGRAM)_debug

experiments/README.txt: experiments/README.org
	## Publish experiments overview to ASCII text
	@echo "Publishing experiments overview to ASCII..."
	@emacs --batch \
		--eval "(require 'org)" \
		--eval "(require 'ox-ascii)" \
		--eval "(find-file \"experiments/README.org\")" \
		--eval "(org-ascii-export-to-ascii)" \
		--eval "(kill-emacs)"
	@mv experiments/README.txt experiments/README.txt 2>/dev/null || true
	@echo "Published to experiments/README.txt"

deps:
	## Install dependencies
	@scripts/deps.sh

.PHONY: clean remake all terminal curses sdl debug-terminal debug-curses debug-sdl gdb-run deps