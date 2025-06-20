;;; 2048-analysis.el --- Analysis tools for 2048 game states -*- lexical-binding: t -*-

;; Tools for analyzing 2048 game states and AI behavior

;;; Code:

(require 'cl-lib)

(defun 2048-analyze-board-from-string (board-str)
  "Analyze a board state from a string of numbers."
  (interactive "sBoard values (space-separated): ")
  (let* ((values (mapcar #'string-to-number (split-string board-str)))
         (non-zero (cl-remove 0 values))
         (max-tile (if non-zero (apply #'max non-zero) 0))
         (sum (apply #'+ non-zero))
         (empty-cells (cl-count 0 values))
         (buffer (get-buffer-create "*2048 Analysis*")))
    (with-current-buffer buffer
      (erase-buffer)
      (insert "=== 2048 Board Analysis ===\n\n")
      (insert (format "Board size: %dx%d\n" 
                      (truncate (sqrt (length values)))
                      (truncate (sqrt (length values)))))
      (insert (format "Empty cells: %d/%d (%.1f%%)\n"
                      empty-cells 
                      (length values)
                      (* 100.0 (/ (float empty-cells) (length values)))))
      (insert (format "Tiles on board: %d\n" (length non-zero)))
      (insert (format "Maximum tile: %d\n" max-tile))
      (insert (format "Sum of tiles: %d\n" sum))
      (insert "\nTile distribution:\n")
      (let ((tile-counts (make-hash-table)))
        (dolist (val non-zero)
          (puthash val (1+ (gethash val tile-counts 0)) tile-counts))
        (let ((sorted-tiles (sort (hash-table-keys tile-counts) #'<)))
          (dolist (tile sorted-tiles)
            (insert (format "  %4d: %d\n" tile (gethash tile tile-counts))))))
      (insert "\nBoard layout:\n")
      (2048-format-board values))
    (display-buffer buffer)))

(defun 2048-format-board (values)
  "Format a board from a list of values."
  (let ((size (truncate (sqrt (length values)))))
    (dotimes (row size)
      (insert "  ")
      (dotimes (col size)
        (let* ((idx (+ (* row size) col))
               (val (nth idx values)))
          (insert (if (= val 0) "   ." (format "%4d" val)))
          (unless (= col (1- size))
            (insert " "))))
      (insert "\n"))))

(defun 2048-parse-game-output ()
  "Parse 2048 game output from current buffer."
  (interactive)
  (save-excursion
    (goto-char (point-min))
    (let ((states '())
          (scores '()))
      (while (re-search-forward "Score: \\([0-9]+\\)" nil t)
        (push (string-to-number (match-string 1)) scores))
      (goto-char (point-min))
      (while (re-search-forward "^|\\s-*\\([0-9 |]+\\)|$" nil t)
        ;; Extract board state
        (let ((board-lines '()))
          (save-excursion
            (beginning-of-line)
            (dotimes (i 4)
              (when (looking-at "|\\s-*\\([0-9 |]+\\)|")
                (push (match-string 1) board-lines))
              (forward-line)))
          (when (= (length board-lines) 4)
            (push (nreverse board-lines) states))))
      (with-current-buffer (get-buffer-create "*2048 Game Analysis*")
        (erase-buffer)
        (insert "=== Game Analysis ===\n\n")
        (insert (format "Total moves: %d\n" (length states)))
        (insert (format "Final score: %d\n" (car scores)))
        (insert (format "Score progression: %s\n" 
                        (mapconcat #'number-to-string (nreverse scores) " -> ")))
        (display-buffer (current-buffer))))))

(defun 2048-simulate-ai-moves (n)
  "Simulate N moves with AI and analyze."
  (interactive "nNumber of moves: ")
  (compile (format "./2048 --ai --size 4 2>&1 | head -%d" (* n 15))))

(defun 2048-benchmark ()
  "Run performance benchmark."
  (interactive)
  (compile "time ./2048 --ai --size 5 2>&1 | tail -1"))

(provide '2048-analysis)
;;; 2048-analysis.el ends here