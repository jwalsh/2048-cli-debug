/* gfx_web.c - WebAssembly/Browser graphics implementation */

#ifdef __EMSCRIPTEN__

#include <emscripten.h>
#include <emscripten/html5.h>
#include <stdlib.h>
#include <stdio.h>
#include "gfx.h"
#include "engine.h"

/* JavaScript interface functions */
EM_JS(void, js_update_board, (int* grid, int size, int width, int height), {
    // Call JavaScript function to update the visual board
    if (window.updateGameBoard) {
        const board = [];
        for (let i = 0; i < height; i++) {
            const row = [];
            for (let j = 0; j < width; j++) {
                row.push(HEAP32[(grid >> 2) + (i * width + j)]);
            }
            board.push(row);
        }
        window.updateGameBoard(board);
    }
});

EM_JS(void, js_update_score, (int score, int highscore), {
    if (window.updateScore) {
        window.updateScore(score, highscore);
    }
});

EM_JS(void, js_game_over, (), {
    if (window.onGameOver) {
        window.onGameOver();
    }
});

struct gfx_state {
    struct gamestate *game;
    int last_score;
};

struct gfx_state* gfx_init(struct gamestate *g) {
    struct gfx_state *s = malloc(sizeof(struct gfx_state));
    if (!s) return NULL;
    
    s->game = g;
    s->last_score = 0;
    
    // Initialize the board
    gfx_draw(s, g);
    
    return s;
}

void gfx_draw(struct gfx_state *s, struct gamestate *g) {
    // Update the board display
    js_update_board(g->grid_data_ptr, g->gridsize, 
                    g->opts->grid_width, g->opts->grid_height);
    
    // Update score if changed
    if (g->score != s->last_score) {
        js_update_score(g->score, g->score_high);
        s->last_score = g->score;
    }
}

int gfx_getch(struct gfx_state *s) {
    // Input is handled via JavaScript event callbacks
    // This function blocks until input is available
    emscripten_sleep(0); // Yield to browser
    
    // Return the input from JavaScript
    // This requires setting up a communication mechanism
    return EM_ASM_INT({
        if (window.lastKeyPressed) {
            const key = window.lastKeyPressed;
            window.lastKeyPressed = null;
            return key;
        }
        return -1; // No input
    });
}

void gfx_sleep(int ms) {
    emscripten_sleep(ms);
}

void gfx_destroy(struct gfx_state *s) {
    free(s);
}

/* Exported functions for JavaScript */
EMSCRIPTEN_KEEPALIVE
void game_handle_input(struct gamestate *g, int key) {
    // Process input from JavaScript
    // This will be called by JavaScript event handlers
}

EMSCRIPTEN_KEEPALIVE
int* game_get_board_ptr(struct gamestate *g) {
    return g->grid_data_ptr;
}

EMSCRIPTEN_KEEPALIVE
int game_get_board_size(struct gamestate *g) {
    return g->gridsize;
}

EMSCRIPTEN_KEEPALIVE
int game_get_score(struct gamestate *g) {
    return g->score;
}

#endif /* __EMSCRIPTEN__ */