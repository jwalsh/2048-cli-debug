;;; 2048-lldb.el --- LLDB integration for 2048 debugging -*- lexical-binding: t -*-

;; This file provides enhanced LLDB integration specifically for 2048

;;; Code:

(require 'gud)

(defvar 2048-lldb-breakpoints
  '("main"
    "gamestate_init"
    "gamestate_new_block"
    "engine_move"
    "engine_tick"
    "gfx_draw"
    "ai_move")
  "Common breakpoints for 2048 debugging.")

(defun 2048-lldb-set-breakpoints ()
  "Set common breakpoints for 2048."
  (interactive)
  (dolist (bp 2048-lldb-breakpoints)
    (gud-call (format "b %s" bp))))

(defun 2048-lldb-print-board ()
  "Print the current board state."
  (interactive)
  (gud-call "expression -o -- (void)print_grid(g)"))

(defun 2048-lldb-dump-gamestate ()
  "Dump the entire gamestate."
  (interactive)
  (gud-call "expression -o -- (void)dump_gamestate(g)"))

(defun 2048-lldb-watch-score ()
  "Set a watchpoint on the score."
  (interactive)
  (gud-call "watchpoint set variable g->score"))

(defun 2048-lldb-memory-dump ()
  "Dump the raw board memory."
  (interactive)
  (gud-call "memory read -c 16 -f d g->grid_data_ptr"))

(defun 2048-lldb-init ()
  "Initialize LLDB with 2048-specific helpers."
  (interactive)
  ;; Define helper functions in LLDB
  (gud-call "expression -- void print_grid(struct gamestate *gs) { \
    int i, j; \
    printf(\"\\n\"); \
    for (i = 0; i < gs->opts->grid_height; i++) { \
        printf(\"[ \"); \
        for (j = 0; j < gs->opts->grid_width; j++) { \
            printf(\"%5d \", gs->grid[i][j]); \
        } \
        printf(\"]\\n\"); \
    } \
    printf(\"\\n\"); \
}")
  
  (gud-call "expression -- void dump_gamestate(struct gamestate *gs) { \
    printf(\"=== GAMESTATE DUMP ===\\n\"); \
    printf(\"Grid: %dx%d\\n\", gs->opts->grid_width, gs->opts->grid_height); \
    printf(\"Score: %ld\\n\", gs->score); \
    printf(\"High Score: %ld\\n\", gs->score_high); \
    printf(\"Blocks: %d\\n\", gs->blocks_in_play); \
    print_grid(gs); \
}"))

;; Add to GUD menu
(easy-menu-define 2048-lldb-menu gud-menu-map
  "2048 LLDB commands"
  '("2048"
    ["Set Breakpoints" 2048-lldb-set-breakpoints t]
    ["Print Board" 2048-lldb-print-board t]
    ["Dump Gamestate" 2048-lldb-dump-gamestate t]
    ["Watch Score" 2048-lldb-watch-score t]
    ["Memory Dump" 2048-lldb-memory-dump t]
    "---"
    ["Initialize Helpers" 2048-lldb-init t]))

(provide '2048-lldb)
;;; 2048-lldb.el ends here