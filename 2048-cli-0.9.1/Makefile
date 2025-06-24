CC             ?= clang
TTF_FONT_PATH  ?= res/Anonymous Pro.ttf
CFLAGS         += -DTTF_FONT_PATH="\"$(TTF_FONT_PATH)\""
CFLAGS         += -Wno-visibility -Wno-incompatible-pointer-types -Wall -Wextra
CFLAGS         += -DINVERT_COLORS -DVT100 -O2
LFLAGS         +=

PROGRAM := 2048
C_FILES := $(wildcard src/*.c)
MERGE_FILE := src/merge_std.c
FILTERED_C_FILES := $(filter-out src/gfx%.c src/merge%.c, $(C_FILES))

all: terminal

curses: $(FILTERED_C_FILES) src/gfx_curses.c
	$(CC) $(CFLAGS) $(FILTERED_C_FILES) $(MERGE_FILE) src/gfx_curses.c -o $(PROGRAM) $(LDFLAGS) -lcurses

terminal: $(FILTERED_C_FILES) src/gfx_terminal.c
	$(CC) $(CFLAGS) $(FILTERED_C_FILES) $(MERGE_FILE) src/gfx_terminal.c -o $(PROGRAM) $(LDFLAGS)

sdl: $(FILTERED_C_FILES) src/gfx_sdl.c
	$(CC) $(CFLAGS) $(FILTERED_C_FILES) $(MERGE_FILE) src/gfx_sdl.c -o $(PROGRAM) $(shell pkg-config --cflags sdl2) $(LDFLAGS) -lSDL2 -lSDL2_ttf

remake: clean all

clean:
	rm -f $(PROGRAM)

archive-source:
	tar -czf 2048-cli-src-backup.tar.gz src/ Makefile README.md LICENSE man/ res/

download-source: 2048-cli-v0.9.1.tar.gz
	tar -xzf 2048-cli-v0.9.1.tar.gz

2048-cli-v0.9.1.tar.gz:
	wget https://codeload.github.com/Tiehuis/2048-cli/tar.gz/v0.9.1?dummy=/Tiehuis-2048-cli-v0.9.1_GH0.tar.gz -O $@

extract-source: 2048-cli-v0.9.1.tar.gz
	@if [ ! -d "2048-cli-0.9.1" ]; then \
		tar -xzf 2048-cli-v0.9.1.tar.gz; \
	else \
		echo "Source already extracted"; \
	fi

# WebAssembly build
wasm: $(FILTERED_C_FILES) src/gfx_web.c
	emcc $(FILTERED_C_FILES) $(MERGE_FILE) src/gfx_web.c \
		-o 2048.js \
		-s WASM=1 \
		-s EXPORTED_FUNCTIONS='["_main", "_game_handle_input", "_game_get_board_ptr", "_game_get_board_size", "_game_get_score"]' \
		-s EXPORTED_RUNTIME_METHODS='["ccall", "cwrap"]' \
		-s MODULARIZE=1 \
		-s EXPORT_NAME='Game2048' \
		-s ALLOW_MEMORY_GROWTH=1 \
		-O2

wasm-debug: $(FILTERED_C_FILES) src/gfx_web.c
	emcc $(FILTERED_C_FILES) $(MERGE_FILE) src/gfx_web.c \
		-o 2048-debug.js \
		-s WASM=1 \
		-s EXPORTED_FUNCTIONS='["_main", "_game_handle_input", "_game_get_board_ptr", "_game_get_board_size", "_game_get_score"]' \
		-s EXPORTED_RUNTIME_METHODS='["ccall", "cwrap"]' \
		-s MODULARIZE=1 \
		-s EXPORT_NAME='Game2048' \
		-s ALLOW_MEMORY_GROWTH=1 \
		-g4 \
		-s ASSERTIONS=2 \
		-s SAFE_HEAP=1

.PHONY: clean remake download-source archive-source extract-source wasm wasm-debug
