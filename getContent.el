#!/bin/sh
"true" ; exec emacs --script "$0" "$@"
(require 'ox-publish)

(defun eob-get-content(context_str)
  (interactive)
  (with-temp-buffer
    (insert context_str)
    (org-html-export-as-html nil nil nil t nil)
    (setq org-html (substring-no-properties (buffer-string)))
    (kill-buffer "*Org HTML Export*")
    (setq content org-html)
    (message "%s" content)
   )
)
(eob-get-content (elt argv 0))
