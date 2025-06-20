;;; 2048-mode.el --- Emacs support for 2048 CLI game development -*- lexical-binding: t -*-

;; Author: Claude Assistant
;; Keywords: games, c, debugging
;; Version: 1.0.0
;; Package-Requires: ((emacs "25.1"))

;;; Commentary:

;; This package provides tools for developing and debugging the 2048 CLI game in Emacs.
;; Features include:
;; - Compilation support with error parsing
;; - LLDB integration for debugging
;; - Board visualization
;; - Code navigation helpers

;;; Code:

(require 'compile)
(require 'gdb-mi)

(defgroup 2048-mode nil
  "Support for 2048 CLI game development."
  :group 'programming)

(defcustom 2048-source-dir default-directory
  "Directory containing 2048 source code."
  :type 'directory
  :group '2048-mode)

(defcustom 2048-executable "2048"
  "Path to 2048 executable."
  :type 'string
  :group '2048-mode)

;;;; Compilation support

(defvar 2048-compilation-error-regexp-alist
  '(("^\\([^:]+\\):\\([0-9]+\\):\\([0-9]+\\): \\(error\\|warning\\): \\(.*\\)$"
     1 2 3 (4 . 5)))
  "Regexp for parsing 2048 compilation errors.")

(defun 2048-compile ()
  "Compile 2048 with appropriate flags."
  (interactive)
  (compile "make clean && make CFLAGS='-g -O0 -Wall -Wextra'"))

(defun 2048-compile-release ()
  "Compile 2048 in release mode."
  (interactive)
  (compile "make clean && make"))

;;;; Debugging support

(defun 2048-debug ()
  "Start debugging 2048 with LLDB."
  (interactive)
  (let ((gdb-command "lldb")
        (gud-gdb-command-name "lldb"))
    (gdb (format "%s %s" gdb-command 2048-executable))))

(defun 2048-debug-with-script (script)
  "Start debugging with a specific LLDB script."
  (interactive
   (list (completing-read "Debug script: "
                         '("debug.lldb"
                           "debug-interactive.lldb"
                           "debug-automated.lldb"
                           "debug-symbols.lldb"))))
  (let ((default-directory 2048-source-dir))
    (compile (format "lldb %s -s %s" 2048-executable script))))

;;;; Board visualization

(defface 2048-tile-2 '((t :background "#eee4da" :foreground "#776e65"))
  "Face for tile value 2.")
(defface 2048-tile-4 '((t :background "#ede0c8" :foreground "#776e65"))
  "Face for tile value 4.")
(defface 2048-tile-8 '((t :background "#f2b179" :foreground "#f9f6f2"))
  "Face for tile value 8.")
(defface 2048-tile-16 '((t :background "#f59563" :foreground "#f9f6f2"))
  "Face for tile value 16.")
(defface 2048-tile-32 '((t :background "#f67c5f" :foreground "#f9f6f2"))
  "Face for tile value 32.")
(defface 2048-tile-64 '((t :background "#f65e3b" :foreground "#f9f6f2"))
  "Face for tile value 64.")
(defface 2048-tile-128 '((t :background "#edcf72" :foreground "#f9f6f2"))
  "Face for tile value 128.")
(defface 2048-tile-256 '((t :background "#edcc61" :foreground "#f9f6f2"))
  "Face for tile value 256.")
(defface 2048-tile-512 '((t :background "#edc850" :foreground "#f9f6f2"))
  "Face for tile value 512.")
(defface 2048-tile-1024 '((t :background "#edc53f" :foreground "#f9f6f2"))
  "Face for tile value 1024.")
(defface 2048-tile-2048 '((t :background "#edc22e" :foreground "#f9f6f2"))
  "Face for tile value 2048.")

(defun 2048-visualize-board (board-string)
  "Visualize a 2048 board from its string representation."
  (interactive "sBoard string (space-separated values): ")
  (let* ((values (mapcar #'string-to-number (split-string board-string)))
         (size (truncate (sqrt (length values))))
         (buffer (get-buffer-create "*2048 Board*")))
    (with-current-buffer buffer
      (erase-buffer)
      (dotimes (row size)
        (dotimes (col size)
          (let* ((idx (+ (* row size) col))
                 (val (nth idx values))
                 (str (if (= val 0) "    " (format "%4d" val)))
                 (face (intern (format "2048-tile-%d" val))))
            (insert (if (facep face)
                       (propertize str 'face face)
                     str))
            (unless (= col (1- size))
              (insert " | "))))
        (insert "\n")
        (unless (= row (1- size))
          (insert (make-string (1- (* size 7)) ?-) "\n"))))
    (display-buffer buffer)))

;;;; Running the game

(defun 2048-run ()
  "Run 2048 in a terminal."
  (interactive)
  (let ((default-directory 2048-source-dir))
    (ansi-term 2048-executable "2048")))

(defun 2048-run-ai ()
  "Run 2048 with AI mode."
  (interactive)
  (let ((default-directory 2048-source-dir))
    (compile (format "%s --ai" 2048-executable))))

;;;; Code navigation

(defun 2048-find-function (function)
  "Find definition of FUNCTION in 2048 source."
  (interactive
   (list (completing-read "Function: "
                         '("main" "gamestate_init" "gamestate_tick"
                           "engine_move" "engine_tick" "gfx_draw"
                           "ai_move" "merge_std" "highscore_load"))))
  (let ((default-directory 2048-source-dir))
    (xref-find-definitions function)))

(defun 2048-goto-board-struct ()
  "Jump to gamestate struct definition."
  (interactive)
  (find-file (expand-file-name "src/engine.h" 2048-source-dir))
  (goto-char (point-min))
  (search-forward "struct gamestate"))

;;;; Keybindings

(defvar 2048-mode-map
  (let ((map (make-sparse-keymap)))
    (define-key map (kbd "C-c C-c") #'2048-compile)
    (define-key map (kbd "C-c C-r") #'2048-run)
    (define-key map (kbd "C-c C-d") #'2048-debug)
    (define-key map (kbd "C-c C-a") #'2048-run-ai)
    (define-key map (kbd "C-c C-f") #'2048-find-function)
    (define-key map (kbd "C-c C-b") #'2048-goto-board-struct)
    map)
  "Keymap for 2048-mode.")

;;;; Minor mode

(define-minor-mode 2048-mode
  "Minor mode for 2048 development."
  :lighter " 2048"
  :keymap 2048-mode-map
  (when 2048-mode
    (add-to-list 'compilation-error-regexp-alist-alist
                 (cons '2048 2048-compilation-error-regexp-alist))
    (add-to-list 'compilation-error-regexp-alist '2048)))

;;;; Project configuration

(defun 2048-setup-project ()
  "Set up project-specific settings for 2048."
  (interactive)
  (setq-local compile-command "make")
  (setq-local tags-file-name (expand-file-name "TAGS" 2048-source-dir))
  (setq-local c-basic-offset 4)
  (setq-local indent-tabs-mode nil)
  (2048-mode 1))

;; Auto-enable in C files within project
(add-hook 'c-mode-hook
          (lambda ()
            (when (string-match-p "2048" default-directory)
              (2048-setup-project))))

(provide '2048-mode)
;;; 2048-mode.el ends here