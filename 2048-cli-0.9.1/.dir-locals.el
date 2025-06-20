;;; Directory Local Variables
;;; For more information see (info "(emacs) Directory Variables")

((nil . ((compile-command . "make")
         (tags-file-name . "./TAGS")))
 (c-mode . ((c-file-style . "linux")
            (c-basic-offset . 4)
            (indent-tabs-mode . nil)
            (eval . (progn
                      (require '2048-mode nil t)
                      (2048-mode 1))))))